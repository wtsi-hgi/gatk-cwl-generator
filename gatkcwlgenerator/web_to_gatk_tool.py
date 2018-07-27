import logging
from collections import namedtuple
from typing import *

import requests
from bs4 import BeautifulSoup

from .GATK_classes import *
from .common import GATKVersion

_logger: logging.Logger = logging.getLogger("gatkcwlgenerator")
_logger.addHandler(logging.StreamHandler())


# A class to store info from the leading GATK page
GATKLinks = namedtuple("GATKLinks", [
    "tool_urls",
    "annotator_urls",
    "readfilter_urls",
    "resourcefile_urls",
    "command_line_gatk_url"
])

def get_gatk_links(gatk_version: GATKVersion) -> GATKLinks:
    """
    Parse the tool docs HTML page to get links to the JSON resources.
    """

    # TODO: make this look at the JSON files to categorise them
    # The group they belong in is right there in the JSON, under "group" -- using that
    # rather than the URL to categorise them should work much better.

    base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" % gatk_version

    base_webpage_request = requests.get(base_url)
    base_webpage_request.raise_for_status()

    data = base_webpage_request.text
    soup = BeautifulSoup(data, "html.parser")

    tool_urls = []

    annotator_urls = []
    readfilter_urls = []
    resourcefile_urls = []

    starting_str = "org_broadinstitute_gatk" if gatk_version.is_3() else "org_broadinstitute_hellbender"

    # Parse the HTML to obtain all JSON file links.
    for link in soup.select("tr > td > a"):
        href = link['href']
        if href.startswith(starting_str) and "Exception" not in href:
            if gatk_version.is_3():
                full_url = base_url + href + ".json"  # v3 files end in .php.json
            else:
                full_url = base_url + href[:-4] + ".json"  # strip off .php as v4 files end in .json
            rest_text = href[len(starting_str + "_"):]

            # Need to process these separately
            if rest_text.startswith("tools_walkers_annotator") \
                    and "VariantAnnotator" not in rest_text:
                # VariantAnnotator is wrongly categorized in its url (it's a tool)
                annotator_urls.append(full_url)
            elif rest_text.startswith("engine_filters") or "HCMappingQualityFilter" in rest_text:
                # HCMappingQualityFilter's url suggests it's a tool
                readfilter_urls.append(full_url)
            elif rest_text.startswith("utils_codecs"):
                resourcefile_urls.append(full_url)
            else:
                tool_urls.append(full_url)

    # Remove duplicates
    tool_urls = list(set(tool_urls))

    cmd_line_gatk = None

    # Move CommandLine to the front of the list
    if gatk_version.is_3():
        cmd_line_gatk = next((x for x in tool_urls if "CommandLineGATK" in x))

    return GATKLinks(
        tool_urls=tool_urls,
        annotator_urls=annotator_urls,
        readfilter_urls=readfilter_urls,
        resourcefile_urls=resourcefile_urls,
        command_line_gatk_url=cmd_line_gatk
    )

def fetch_json_from(gatk_tool_url: str) -> Dict:
    _logger.info(f"Fetching {gatk_tool_url}")
    gatk_info_request = requests.get(gatk_tool_url)
    gatk_info_request.raise_for_status()

    try:
        gatk_info_dict = gatk_info_request.json()
    except ValueError as error:
        raise Exception("Could not decode JSON retrieved from " + gatk_tool_url) from error

    return gatk_info_dict

def _get_extra_readfilter_arguments(readfilter_urls: Iterable[str]) -> List[Dict]:
    arguments: List[Dict] = []

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

def get_extra_arguments(
        gatk_version: GATKVersion,
        gatk_links: GATKLinks
    ) -> List[Dict]:
    read_filter_arguments = _get_extra_readfilter_arguments(gatk_links.readfilter_urls)

    if gatk_version.is_3():
        cmd_line_gatk_dict = fetch_json_from(gatk_links.command_line_gatk_url)
        return cmd_line_gatk_dict["arguments"] + read_filter_arguments
    else:
        return read_filter_arguments

def get_gatk_tool(
        tool_url: str,
        extra_arguments: List[Dict] = None
    ) -> GATKTool:
    """
    Get GATK tools from the specified tool_urls.
    """
    if extra_arguments is None:
        extra_arguments = []

    tool_dict = fetch_json_from(tool_url)
    tool_name = tool_dict["name"]

    if tool_name in ("CommandLineGATK", "CatVariants"):
        extra_arguments = []

    return GATKTool(
        tool_dict,
        extra_arguments
    )

def get_annotation_name(annotation_url: str) -> str:
    """Get the annotation name from the specified URL."""
    # TODO: can this be done without a web request?
    json = fetch_json_from(annotation_url)
    return json["name"]
