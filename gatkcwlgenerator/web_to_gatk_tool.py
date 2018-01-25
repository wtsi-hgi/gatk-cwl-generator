import logging
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

from .gatk_classes import *
from .common import GATKVersion

_logger = logging.getLogger("gatkcwlgenerator")  # type: logging.Logger
_logger.addHandler(logging.StreamHandler())


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

def get_gatk_links(gatk_version: GATKVersion) -> GATKLinks:
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

    starting_str = "org_broadinstitute_gatk" if gatk_version.is_3() else "org_broadinstitute_hellbender"

    # Parse the html to obtain all json file links
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
        raise Exception("Could not decode json retrieved from " + gatk_tool_url) from error

    return gatk_info_dict

def _get_extra_readfilter_arguments(readfilter_urls: Iterable[str]) -> List[Dict]:
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
        gatk_version: GATKVersion,
        tool_urls: Iterable[str],
        readfilter_urls: Iterable[str],
        command_line_gatk_url: str = None
    ) -> Iterable[GATKTool]:
    """
    Gets gatk tools from the specified tool_urls.
    NOTE: command_line_gatk_url should be specified for gatk 3, and leave
    as None in gatk 4
    """
    if gatk_version.is_3():
        if command_line_gatk_url is None:
            raise Exception("command_line_gatk_url needs to be specified in gatk 3 in get_gatk_tools")

        cmd_line_gatk_dict = fetch_json_from(command_line_gatk_url)
    read_filter_arguments = _get_extra_readfilter_arguments(readfilter_urls)

    for tool_url in tool_urls:
        tool_dict = fetch_json_from(tool_url)
        tool_name = tool_dict["name"]

        if tool_name not in ("CommandLineGATK", "CatVariants"):
            if gatk_version.is_3():
                extra_arguments = cmd_line_gatk_dict["arguments"] + read_filter_arguments
            else:
                extra_arguments = read_filter_arguments
        else:
            extra_arguments = []

        yield GATKTool(
            tool_dict,
            extra_arguments
        )
