#!/bin/python

import os
import argparse
import shutil
import itertools
import json
import sys
import logging

from bs4 import BeautifulSoup
import requests
import coloredlogs

from .json2cwl import json2cwl
from .helpers import is_gatk_3

_logger = logging.getLogger("gatkcwlgenerator") # type: logging.Logger
_logger.addHandler(logging.StreamHandler())


def find_index(lst, func):
    for i, item in enumerate(lst):
        if func(item):
            return i

    raise ValueError("Item not found")

class JSONLinks:
    def __init__(self, tool_urls, annotator_urls, readfilter_urls, resourcefile_urls):
        self.tool_urls = tool_urls
        self.annotator_urls = annotator_urls
        self.readfilter_urls = readfilter_urls
        self.resourcefile_urls = resourcefile_urls

def get_json_links(version):
    """
    Parses the tool docs HTML page to get links to the json resources
    """
    base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" % version

    base_webpage_request = requests.get(base_url)
    base_webpage_request.raise_for_status()

    data = base_webpage_request.text
    soup = BeautifulSoup(data, "html.parser")

    tool_urls = []

    annotator_urls = []
    readfile_urls = []
    resourcefile_urls = []

    starting_str = "org_broadinstitute_gatk" if is_gatk_3(version) else "org_broadinstitute_hellbender"

    # Parse the html to obtain all json file links
    for link in soup.select("tr > td > a"):
        href = link['href']
        if href.startswith(starting_str) and "Exception" not in href:
            if is_gatk_3(version):
                full_url = base_url + href + ".json" # v3 files end in .php.json
            else:
                full_url = base_url + href[:-4] + ".json" # strip off .php as v4 files end in .json
            rest_text = href[len(starting_str + "_"):]

            # Need to process these separately
            if rest_text.startswith("tools_walkers_annotator") \
                    and "VariantAnnotator" not in rest_text:
                    # VariantAnnotator is wrongly categorized in it's url (it's a tool)
                annotator_urls.append(full_url)
            elif rest_text.startswith("engine_filters"):
                readfile_urls.append(full_url)
            elif rest_text.startswith("utils_codecs"):
                resourcefile_urls.append(full_url)
            else:
                tool_urls.append(full_url)

    # Remove duplicates
    tool_urls = list(set(tool_urls))

    # Move CommandLine to the front of the list
    if is_gatk_3(version):
        i = find_index(tool_urls, lambda x: "CommandLineGATK" in x)
        tool_urls[0], tool_urls[i] = tool_urls[i], tool_urls[0]

    return JSONLinks(tool_urls, annotator_urls, readfile_urls, resourcefile_urls)

def generate_cwl_and_json_files(out_dir, grouped_urls, cmd_line_options):
    """
    Generates the cwl and json files
    """
    global_args = get_global_arguments(grouped_urls, is_gatk_3(cmd_line_options.version))

    _logger.info("Creating and converting json files...")

    # Get current directory and make folders for files
    json_dir = os.path.join(out_dir, 'json')
    cwl_dir = os.path.join(out_dir, 'cwl')

    try:
        os.makedirs(json_dir)
        os.makedirs(cwl_dir)
    except OSError as e:
        if cmd_line_options.dev:
            shutil.rmtree(json_dir) # Removing existing generated files if the folder already exists, for testing
            shutil.rmtree(cwl_dir)
            os.makedirs(json_dir)
            os.makedirs(cwl_dir)
        else:
            raise


    # Create json for each tool and convert to cwl
    for tool_url in grouped_urls.tool_urls:
        if cmd_line_options.include is None or cmd_line_options.include in tool_url or "CommandLineGATK" in tool_url:
            _logger.info("Fetching tool url: %s", tool_url)
            tool_json = requests.get(tool_url)
            tool_json.raise_for_status()
            try:
                tool_json_json = tool_json.json()
            except ValueError as error:
                raise Exception("Could not decode json retrieved from %s" % tool_url) from error

            tool_name = tool_json_json['name']
            json_name = tool_name + ".json"

            json_path = os.path.join(json_dir, json_name)
            _logger.info("Writing json to " + json_path)
            json_file = open(json_path, 'w+')
            json_file.write(tool_json.text)
            json_file.close()

            # Don't append options for CommandLinkGATK or read filters for CatVariants,
            # it bypasses the GATK engine
            # https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_CatVariants.php
            if not (tool_name == "CommandLineGATK" or tool_name == "CatVariants"):
                apply_global_arguments(tool_json_json, global_args)

            cwl_path = os.path.join(cwl_dir, tool_name + ".cwl")
            _logger.info("Writing cwl to " + cwl_path)
            json2cwl(
                tool_json_json,
                cwl_dir,
                cmd_line_options
            )

    _logger.info("Success!")

def apply_global_arguments(GATK_json, global_args):
    """
    Adds globals arguments to the GATK json object, not adding arguments if they are duplicated
    in the GATK json file

    :param GATK_json: The GATK json object to modify
    :param global_args: An array of arguments to add as global arguments
    """
    GATK_args_names = set(arg["name"] for arg in GATK_json["arguments"])

    for global_arg in global_args:
        if global_arg["name"] not in GATK_args_names:
            GATK_json["arguments"].append(global_arg)

def get_global_arguments(grouped_urls, apply_cmdlineGATK):
    """
    Get arguments (e.g. CommandLinkGATK and read filters) that should be avaliable to all CWL files

    :param grouped_urls: Urls as generated by get_json_links
    :param apply_cmdlineGATK: should be false on v4+
    """
    arguments = []

    if apply_cmdlineGATK:
        commandLineGATK_response = requests.get(grouped_urls.tool_urls[0])
        commandLineGATK_response.raise_for_status()

        try:
            commandLineGATK = commandLineGATK_response.json() # This should be CommandLineGATK
        except ValueError as ve:
            raise Exception("Error decoding CommandLineGATK JSON retrieved from %s" % grouped_urls.tool_urls[0]) from ve
        arguments.extend(commandLineGATK["arguments"])

    _logger.info("Getting read filter arguments ...")

    for readfilter_url in grouped_urls.readfilter_urls:
        _logger.info("Fetching " + readfilter_url)
        readfilter_response = requests.get(readfilter_url)
        readfilter_response.raise_for_status()
        try:
            readfilter_json = readfilter_response.json()
        except ValueError as error:
            raise Exception("Could not decode read filter json retrieved from %s" % readfilter_url) from error

        if "arguments" in readfilter_json:
            args = readfilter_json["arguments"]

            for arg in args:
                arg["defaultValue"] = "NA" # This argument is not necessarily valid, so we shouldn't set the default
                arg["required"] = "no"

            arguments.extend(args)
    return arguments

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

def cmdline_main(args=sys.argv[1:]):
    """
    Function to be called when this is invoked on the command line.
    """
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

    if cmd_line_options.verbose:
        coloredlogs.install(level='DEBUG', logger=_logger)
    else:
        coloredlogs.install(level='WARNING', logger=_logger)

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

    _logger.info("Ouputting to: '%s'" % cmd_line_options.output_dir)
    grouped_urls = get_json_links(cmd_line_options.version)

    generate_cwl_and_json_files(cmd_line_options.output_dir, grouped_urls, cmd_line_options)


if __name__ == '__main__':
    cmdline_main()
