import pytest
import requests_cache

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.web_to_gatk_tool import get_gatk_links, get_gatk_tool, get_extra_arguments
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
