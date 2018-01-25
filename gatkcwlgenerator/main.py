#!/bin/python

import argparse
import json
import logging
import os
import shutil
import time
from typing import *
from collections import namedtuple
import sys
import functools

import coloredlogs
import requests
from bs4 import BeautifulSoup
from ruamel import yaml

from .GATK_classes import *
from .helpers import is_gatk_3
from .json2cwl import json2cwl

_logger = logging.getLogger("gatkcwlgenerator")  # type: logging.Logger
_logger.addHandler(logging.StreamHandler())


class OutputWriter:
    def __init__(self, cmd_line_options):
        # Get current directory and make folders for files
        json_dir = os.path.join(cmd_line_options.output_dir, "json")
        cwl_dir = os.path.join(cmd_line_options.output_dir, "cwl")

        try:
            os.makedirs(json_dir)
            os.makedirs(cwl_dir)
        except OSError:
            if cmd_line_options.dev:
                # Removing existing generated files if the folder already exists, for testing
                shutil.rmtree(json_dir)
                shutil.rmtree(cwl_dir)
                os.makedirs(json_dir)
                os.makedirs(cwl_dir)
            else:
                raise

        self._json_dir = json_dir
        self._cwl_dir = cwl_dir

    def write_cwl_file(self, cwl_dict: Dict, tool_name: str):
        cwl_path = os.path.join(self._cwl_dir, tool_name + ".cwl")

        _logger.info(f"Writing cwl file to {cwl_path}")

        with open(cwl_path, "w") as file:
            yaml.round_trip_dump(cwl_dict, file)

    def write_gatk_json_file(self, gatk_json_dict: Dict, tool_name: str):
        gatk_json_path = os.path.join(self._json_dir, tool_name + ".json")

        _logger.info(f"Writing gatk json file to {gatk_json_path}")

        with open(gatk_json_path, "w") as file:
            json.dump(gatk_json_dict, file)


def find_index(lst, func):
    for i, item in enumerate(lst):
        if func(item):
            return i

    raise ValueError("Item not found")

"""
GATKLinks: A class to store info from the leading GATK page
"""
GATKLinks = namedtuple("GATKLinks", [
    "tool_urls",
    "annotator_urls",
    "readfilter_urls",
    "resourcefile_urls",
    "command_line_gatk_url"
])


def get_gatk_links(gatk_version) -> GATKLinks:
    """
    Parses the tool docs HTML page to get links to the json resources
    """
    base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" % gatk_version

    base_webpage_request = requests.get(base_url)
    base_webpage_request.raise_for_status()

    data = base_webpage_request.text
    soup = BeautifulSoup(data, "html.parser")

    tool_urls = []

    annotator_urls = []
    readfilter_urls = []
    resourcefile_urls = []

    starting_str = "org_broadinstitute_gatk" if is_gatk_3(gatk_version) else "org_broadinstitute_hellbender"

    # Parse the html to obtain all json file links
    for link in soup.select("tr > td > a"):
        href = link['href']
        if href.startswith(starting_str) and "Exception" not in href:
            if is_gatk_3(gatk_version):
                full_url = base_url + href + ".json"  # v3 files end in .php.json
            else:
                full_url = base_url + href[:-4] + ".json"  # strip off .php as v4 files end in .json
            rest_text = href[len(starting_str + "_"):]

            # Need to process these separately
            if rest_text.startswith("tools_walkers_annotator") \
                    and "VariantAnnotator" not in rest_text:
                    # VariantAnnotator is wrongly categorized in it's url (it's a tool)
                annotator_urls.append(full_url)
            elif rest_text.startswith("engine_filters"):
                readfilter_urls.append(full_url)
            elif rest_text.startswith("utils_codecs"):
                resourcefile_urls.append(full_url)
            else:
                tool_urls.append(full_url)

    # Remove duplicates
    tool_urls = list(set(tool_urls))

    cmd_line_gatk = None

    # Move CommandLine to the front of the list
    if is_gatk_3(gatk_version):
        cmd_line_gatk = next((x for x in tool_urls if "CommandLineGATK" in x))

    return GATKLinks(
        tool_urls=tool_urls,
        annotator_urls=annotator_urls,
        readfilter_urls=readfilter_urls,
        resourcefile_urls=resourcefile_urls,
        command_line_gatk_url=cmd_line_gatk
    )


def should_generate_file(tool_url, cmd_line_options):
    no_ext_url = tool_url[:-len(".php.json" if is_gatk_3(cmd_line_options.version) else ".json")]

    return cmd_line_options.include is None or no_ext_url.endswith(cmd_line_options.include)

def fetch_json_from(gatk_tool_url: str) -> Dict:
    _logger.info(f"Fetching {gatk_tool_url}")
    gatk_info_request = requests.get(gatk_tool_url)
    gatk_info_request.raise_for_status()

    try:
        gatk_info_dict = gatk_info_request.json()
    except ValueError as error:
        raise Exception("Could not decode json retrieved from " + gatk_tool_url) from error

    return gatk_info_dict

def get_extra_readfilter_arguments(readfilter_urls: List[str]) -> List[Dict]:
    arguments = [] # type: List[Dict]

    for readfilter_url in readfilter_urls:
        readfilter_dict = fetch_json_from(readfilter_url)

        if "arguments" in readfilter_dict:
            args = readfilter_dict["arguments"]

            for arg in args:
                # This argument is not necessarily valid, so we shouldn't set the default
                arg["defaultValue"] = "NA"
                arg["required"] = "no"

            arguments.extend(args)

    return arguments

def get_gatk_tools(
        gatk_version: str,
        tool_urls: Iterable[str],
        readfilter_urls: Iterable[str],
        command_line_gatk_url: str = None
    ) -> Iterable[GATKTool]:
    """
    Gets gatk tools from the specified tool_urls.
    NOTE: command_line_gatk_url should be specified for gatk 3, and leave
    as None in gatk 4
    """
    if is_gatk_3(gatk_version):
        if command_line_gatk_url is None:
            raise Exception("command_line_gatk_url needs to be specified in gatk 3 in get_gatk_tools")

        cmd_line_gatk_dict = fetch_json_from(command_line_gatk_url)
    read_filter_arguments = get_extra_readfilter_arguments(readfilter_urls)

    for tool_url in tool_urls:
        tool_dict = fetch_json_from(tool_url)
        tool_name = tool_dict["name"]

        if tool_name not in ("CommandLineGATK", "CatVariants"):
            if is_gatk_3(gatk_version):
                extra_arguments = cmd_line_gatk_dict["arguments"] + read_filter_arguments
            else:
                extra_arguments = read_filter_arguments
        else:
            extra_arguments = []

        yield GATKTool(
            tool_dict,
            extra_arguments
        )

def gatk_tool_to_cwl(
        gatk_tool: GATKTool,
        cmd_line_options: Dict
    ) -> Dict:
    return json2cwl(gatk_tool, cmd_line_options)

def main(cmd_line_options: SimpleNamespace):
    start = time.time()

    output_writer = OutputWriter(cmd_line_options)
    gatk_links = get_gatk_links(cmd_line_options.version)
    tool_urls = filter(functools.partial(should_generate_file, cmd_line_options=cmd_line_options), gatk_links.tool_urls) # mypy: ignore
    gatk_tools = get_gatk_tools(
        cmd_line_options.version,
        tool_urls,
        gatk_links.readfilter_urls,
        gatk_links.command_line_gatk_url
    )

    for gatk_tool in gatk_tools:
        output_writer.write_gatk_json_file(gatk_tool.original_dict, gatk_tool.name)
        cwl = gatk_tool_to_cwl(gatk_tool, cmd_line_options)
        output_writer.write_cwl_file(cwl, gatk_tool.name)

    end = time.time()
    _logger.info(f"Completed in {end - start:.2f} seconds")


def gatk_cwl_generator(**cmd_line_options):
    """
    Programmic entry to gatk_cwl_generator.

    This converts the object to cmd line flags and
    passes it though the command line interface, to apply defaults
    """
    args = []
    for key, value in cmd_line_options.items():
        if isinstance(value, bool):
            if value:
                args.append("--" + key)
        else:
            args.append("--" + key)
            args.append(str(value))

    cmdline_main(args)

def cmdline_main(args=None):
    """
    Function to be called when this is invoked on the command line.
    """
    if args is None:
        args = sys.argv[1:]

    default_cache_location = "cache"

    parser = argparse.ArgumentParser(description='Generates CWL files from the GATK documentation')
    parser.add_argument("--version", "-v", dest='version', default="3.5-0",
        help="Sets the version of GATK to parse documentation for. Default is 3.5-0")
    parser.add_argument("--verbose", dest='verbose', action="store_true",
        help="Set the logging to be verbose. Default is False.")
    parser.add_argument('--out', "-o", dest='output_dir',
        help="Sets the output directory for generated files. Default is ./gatk_cmdline_tools/<VERSION>/")
    parser.add_argument('--include', dest='include',
        help="Only generate this file (note, CommandLinkGATK has to be generated for v3.x)")
    parser.add_argument("--dev", dest="dev", action="store_true",
        help="Enable --use_cache and overwriting of the generated files (for development purposes). " +
        "Requires requests_cache to be installed")
    parser.add_argument("--use_cache", dest="use_cache", nargs="?", const=default_cache_location, metavar="CACHE_LOCATION",
        help="Use requests_cache, using the cache at CACHE_LOCATION, or 'cache' if not specified. Default is False.")
    parser.add_argument("--no_docker", dest="no_docker", action="store_true",
        help="Make the generated CWL files not use docker containers. Default is False.")
    parser.add_argument("--docker_image_name", "-c", dest="docker_image_name",
        help="Docker image name for generated cwl files. Default is 'broadinstitute/gatk3:<VERSION>' " +
        "for version 3.x and 'broadinstitute/gatk:<VERSION>' for 4.x")
    parser.add_argument("--gatk_command", "-l", dest="gatk_command",
        help="Command to launch GATK. Default is 'java -jar /usr/GenomeAnalysisTK.jar' for gatk 3.x and 'java -jar /gatk/gatk.jar' for gatk 4.x")
    cmd_line_options = parser.parse_args(args)

    log_format = "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"

    if cmd_line_options.verbose:
        coloredlogs.install(level='DEBUG', logger=_logger, fmt=log_format)
    else:
        coloredlogs.install(level='WARNING', logger=_logger, fmt=log_format)

    if not cmd_line_options.output_dir:
        cmd_line_options.output_dir = os.getcwd() + '/gatk_cmdline_tools/' + cmd_line_options.version

    if not cmd_line_options.docker_image_name:
        if is_gatk_3(cmd_line_options.version):
            cmd_line_options.docker_image_name = "broadinstitute/gatk3:" + cmd_line_options.version
        else:
            cmd_line_options.docker_image_name = "broadinstitute/gatk:" + cmd_line_options.version

    if not cmd_line_options.gatk_command:
        if is_gatk_3(cmd_line_options.version):
            cmd_line_options.gatk_command = "java -jar /usr/GenomeAnalysisTK.jar"
        else:
            cmd_line_options.gatk_command = "java -jar /gatk/gatk.jar"

    if cmd_line_options.dev:
        cmd_line_options.use_cache = default_cache_location

    if cmd_line_options.use_cache:
        import requests_cache
        requests_cache.install_cache(cmd_line_options.use_cache) # Decreases the time to run dramatically

    main(cmd_line_options)


if __name__ == '__main__':
    cmdline_main()
