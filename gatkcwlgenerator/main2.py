#!/bin/python

import sys
import os
import argparse
import shutil
import itertools
import json
import time
from collections import namedtuple
import logging
from typing import *
import attr

from bs4 import BeautifulSoup
import requests
import coloredlogs

from .GATK_classes import *
from .json2cwl import json2cwl
from .helpers import is_gatk_3

_logger = logging.getLogger("gatkcwlgenerator")  # type: logging.Logger
_logger.addHandler(logging.StreamHandler())


class OutputWriter:
    def __init__(self, cmd_line_options):
        # Get current directory and make folders for files
        json_dir = os.path.join(out_dir, "json")
        cwl_dir = os.path.join(out_dir, "cwl")

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

    def write_cwl_file(self, cwl_file_name: str, text: str):
        json_path = os.path.join(self._json_dir, cwl_file_name + ".cwl")

        with open(json_path, "w+") as json_output_file:
            json_output_file.write(text)

    def write_json_file(self, cwl_file_name: str, text: str):
        cwl_path = os.path.join(self._cwl_dir, cwl_file_name + ".json")

        with open(cwl_path, "w") as cwl_output_file:
            cwl_output_file.write(text)


def find_index(lst, func):
    for i, item in enumerate(lst):
        if func(item):
            return i

    raise ValueError("Item not found")


# """
# GATKLinks: A class to store info from the leading GATK page
# """
# GATKLinks = namedtuple("GATKLinks", [
#     "tool_urls",
#     "annotator_urls",
#     "readfilter_urls",
#     "resourcefile_urls",
#     "command_line_gatk"
# ])


class GATKLinks(SimpleNamespace):
    pass


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
        command_line_gatk=cmd_line_gatk
    )


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


def should_generate_file(tool_url, cmd_line_options):
    return cmd_line_options.include is None or tool_url.endswith(cmd_line_options.include) or "CommandLineGATK" in tool_url

class CWLDescription:
    pass

def dump_gatk_json(x):
    pass

def gatk_tool_to_cwl(tool) -> CWLDescription:
    return None

def get_gatk_tool_dict(gatk_tool_url: str) -> Dict:
    _logger.info(f"Fetching {gatk_tool_url}")
    gatk_info_request = requests.get(gatk_tool_url)
    gatk_info_request.raise_for_status()

    try:
        gatk_info_dict = gatk_info_request.json()
    except ValueError as error:
        raise Exception("Could not decode json retrieved from " + gatk_tool_url) from error

    return gatk_info_dict

def get_extra_readfilter_arguments(readfilter_urls: List[str]):
    arguments = []

    for readfilter_url in readfilter_urls:
        readfilter_dict = get_gatk_tool_dict(readfilter_url)

        if "arguments" in readfilter_dict:
            args = readfilter_dict["arguments"]

            for arg in args:
                # This argument is not necessarily valid, so we shouldn't set the default
                arg["defaultValue"] = "NA"
                arg["required"] = "no"

            arguments.extend(args)

    return arguments

def get_gatk_tools(
        gatk_links: GATKLinks,
        gatk_version: str,
        # restrict_function: when given the url of a tool, if this returns
        # false, do not generate the tool
        should_include_url: Callable[[str], bool] = (lambda x:x)
    ) -> List[GATKTool]:
    """
    Gets GATK tools from GATKLinks, by getting tools and extra arguments
    """
    if is_gatk_3(gatk_version):
        cmd_line_gatk_dict = get_gatk_tool_dict(gatk_links.command_line_gatk)
    read_filter_arguments = get_extra_readfilter_arguments(gatk_links.readfilter_urls)

    gatk_tools = []

    for tool_url in gatk_links.tool_urls:
        if should_include_url(tool_url):
            tool_dict = get_gatk_tool_dict(tool_url)
            tool_name = tool_dict["name"]

            if tool_name not in ("CommandLineGATK", "CatVariants"):
                extra_arguments = cmd_line_gatk_dict["arguments"] + read_filter_arguments
            else:
                extra_arguments = []

            gatk_tools.append(GATKTool(
                tool_dict,
                extra_arguments
            ))

    return gatk_tools

def gatk_tool_to_cwl_description(
        gatk_tool: GATKTool,
        cmd_line_options: Dict
    ) -> CWLDescription:
    pass

def main2(cmd_line_options):
    start = time.time()

    gatk_links = get_gatk_links(cmd_line_options.gatk_version)

    for gatk_tool_url in gatk_links.tool_urls:
        tool_dict = get_gatk_tool_dict(gatk_tool_url)
        output_writer.write_json_file(json.dumps(tool_dict))
        #cwl_desc = gatk_tool_to_cwl(gatk_tool)
        #cwl_dict = cwl_desc.to_dict()
        # output_writer.write_cwl_file(yaml.round_trip_dump(cwl_dict))

    end = time.time()
    _logger.info(f"Completed in {start - end:.2f} seconds")
