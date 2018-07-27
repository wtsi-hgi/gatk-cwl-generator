import pytest
import requests_cache

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.web_to_gatk_tool import (
    get_gatk_links, get_gatk_tool, get_extra_arguments, fetch_json_from, get_annotation_name
)
from gatkcwlgenerator.GATK_classes import GATKTool

requests_cache.install_cache()

EG_3 = "3.5-0"
EG_4 = "4.0.0.0"

@pytest.fixture(params=[EG_3, EG_4])
def gatk_version(request):
    return GATKVersion(request.param)

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

def test_zero_request_annotation_name(gatk_version: GATKVersion):
    """Test that the inferred annotation names are correct."""
    annotation_links = get_gatk_links(gatk_version).annotator_urls
    for link in annotation_links:
        json_name = fetch_json_from(link)["name"]
        inferred_name = get_annotation_name(link)
        assert json_name == inferred_name
