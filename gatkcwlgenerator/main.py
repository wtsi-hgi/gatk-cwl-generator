#!/bin/python

import argparse
import json
import logging
import os
import shutil
import sys
import time
from typing import *

import coloredlogs
from ruamel import yaml

from .gatk_tool_to_cwl import gatk_tool_to_cwl
from .common import GATKVersion
from .web_to_gatk_tool import get_tool_name, get_gatk_links, get_gatk_tool, get_extra_arguments

_logger: logging.Logger = logging.getLogger("gatkcwlgenerator")
_logger.addHandler(logging.StreamHandler())


class CmdLineArguments(argparse.Namespace):
    version: str
    verbose: bool
    output_dir: str
    include: Optional[str]
    dev: bool
    use_cache: Optional[str]
    no_docker: bool
    docker_image_name: str
    gatk_command: str


class OutputWriter:
    def __init__(self, cmd_line_options: CmdLineArguments) -> None:
        # Get current directory and make folders for files
        json_dir = os.path.join(cmd_line_options.output_dir, "json")
        cwl_dir = os.path.join(cmd_line_options.output_dir, "cwl")

        try:
            os.makedirs(json_dir)
            os.makedirs(cwl_dir)
        except OSError:
            if cmd_line_options.dev:
                # Remove existing generated files if the folder already exists, for testing
                shutil.rmtree(json_dir)
                shutil.rmtree(cwl_dir)
                os.makedirs(json_dir)
                os.makedirs(cwl_dir)
            else:
                raise

        self._json_dir = json_dir
        self._cwl_dir = cwl_dir

    def write_cwl_file(self, cwl_dict: Dict, tool_name: str) -> None:
        cwl_path = os.path.join(self._cwl_dir, tool_name + ".cwl")

        _logger.info(f"Writing CWL file to {cwl_path}")

        with open(cwl_path, "w") as file:
            yaml.round_trip_dump(cwl_dict, file)

    def write_gatk_json_file(self, gatk_json_dict: Dict, tool_name: str) -> None:
        gatk_json_path = os.path.join(self._json_dir, tool_name + ".json")

        _logger.info(f"Writing GATK JSON file to {gatk_json_path}")

        with open(gatk_json_path, "w") as file:
            json.dump(gatk_json_dict, file)

def should_generate_file(tool_url, gatk_version: GATKVersion, include_pattern: str = None) -> bool:
    no_ext_url = tool_url[:-len(".php.json" if gatk_version.is_3() else ".json")]

    return include_pattern is None or no_ext_url.endswith(include_pattern)

def main(cmd_line_options: CmdLineArguments) -> None:
    start = time.time()

    gatk_version = GATKVersion(cmd_line_options.version)

    output_writer = OutputWriter(cmd_line_options)
    gatk_links = get_gatk_links(gatk_version)

    extra_arguments = get_extra_arguments(
        gatk_version,
        gatk_links
    )

    have_generated_file = False

    annotation_names = [get_tool_name(url) for url in gatk_links.annotator_urls]

    for tool_url in gatk_links.tool_urls:
        if should_generate_file(tool_url, gatk_version, cmd_line_options.include):
            have_generated_file = True

            gatk_tool = get_gatk_tool(tool_url, extra_arguments=extra_arguments)

            output_writer.write_gatk_json_file(gatk_tool.original_dict, gatk_tool.name)

            cwl = gatk_tool_to_cwl(gatk_tool, cmd_line_options, annotation_names)
            output_writer.write_cwl_file(cwl, gatk_tool.name)

    if not have_generated_file:
        _logger.warning("No files have been generated. Check the include pattern is correct")

    end = time.time()
    _logger.info(f"Completed in {end - start:.2f} seconds")


def gatk_cwl_generator(**cmd_line_options) -> None:
    """
    Programmatic entry to gatk_cwl_generator.

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

def cmdline_main(args=None) -> None:
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
        help="Only generate this file (note, CommandLineGATK has to be generated for v3.x)")
    parser.add_argument("--dev", dest="dev", action="store_true",
        help="Enable --use_cache and overwriting of the generated files (for development purposes). " +
        "Requires requests_cache to be installed")
    parser.add_argument("--use_cache", dest="use_cache", nargs="?", const=default_cache_location, metavar="CACHE_LOCATION",
        help="Use requests_cache, using the cache at CACHE_LOCATION, or 'cache' if not specified. Default is False.")
    parser.add_argument("--no_docker", dest="no_docker", action="store_true",
        help="Make the generated CWL files not use Docker containers. Default is False.")
    parser.add_argument("--docker_image_name", "-c", dest="docker_image_name",
        help="Docker image name for generated CWL files. Default is 'broadinstitute/gatk3:<VERSION>' " +
        "for version 3.x and 'broadinstitute/gatk:<VERSION>' for 4.x")
    parser.add_argument("--gatk_command", "-l", dest="gatk_command",
        help="Command to launch GATK. Default is 'java -jar /usr/GenomeAnalysisTK.jar' for GATK 3.x and 'java -jar /gatk/gatk.jar' for GATK 4.x")
    cmd_line_options = parser.parse_args(args, namespace=CmdLineArguments())

    log_format = "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"

    version = GATKVersion(cmd_line_options.version)

    if cmd_line_options.verbose:
        coloredlogs.install(level='DEBUG', logger=_logger, fmt=log_format)
    else:
        coloredlogs.install(level='WARNING', logger=_logger, fmt=log_format)

    if not cmd_line_options.output_dir:
        cmd_line_options.output_dir = os.getcwd() + '/gatk_cmdline_tools/' + cmd_line_options.version

    if not cmd_line_options.docker_image_name:
        if version.is_3():
            cmd_line_options.docker_image_name = "broadinstitute/gatk3:" + cmd_line_options.version
        else:
            cmd_line_options.docker_image_name = "broadinstitute/gatk:" + cmd_line_options.version

    if not cmd_line_options.gatk_command:
        if version.is_3():
            cmd_line_options.gatk_command = "java -jar /usr/GenomeAnalysisTK.jar"
        else:
            cmd_line_options.gatk_command = "java -jar /gatk/gatk.jar"

    if cmd_line_options.dev:
        cmd_line_options.use_cache = default_cache_location

    if cmd_line_options.use_cache:
        import requests_cache
        requests_cache.install_cache(cmd_line_options.use_cache)  # Decreases the time to run dramatically

    main(cmd_line_options)


if __name__ == '__main__':
    cmdline_main()
