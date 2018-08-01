import itertools

from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.web_to_gatk_tool import (
    get_gatk_links, get_gatk_tool, get_extra_arguments, fetch_json_from, get_tool_name
)
from gatkcwlgenerator.GATK_classes import GATKTool


def test_get_gatk_links(gatk_version: GATKVersion):
    gatk_links = get_gatk_links(gatk_version)

    assert len(gatk_links.tool_urls) > 5
    assert len(gatk_links.readfilter_urls) > 5

def test_get_gatk_tools(gatk_version: GATKVersion):
    gatk_links = get_gatk_links(gatk_version)

    assert isinstance(get_gatk_tool(
        gatk_links.tool_urls[0]
    ), GATKTool)

def test_get_extra_arguments(gatk_version: GATKVersion):
    gatk_links = get_gatk_links(gatk_version)

    assert get_extra_arguments(gatk_version, gatk_links)

def test_zero_request_tool_name(gatk_version: GATKVersion):
    """Test that the inferred tool names are correct."""
    gatk_links = get_gatk_links(gatk_version)
    for link in itertools.chain(
        gatk_links.tool_urls, gatk_links.annotator_urls,
        gatk_links.readfilter_urls, gatk_links.resourcefile_urls,
        [gatk_links.command_line_gatk_url] if gatk_links.command_line_gatk_url is not None else []
    ):
        json_name = fetch_json_from(link)["name"]
        inferred_name = get_tool_name(link)
        assert json_name == inferred_name
