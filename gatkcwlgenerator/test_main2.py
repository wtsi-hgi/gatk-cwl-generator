from .main2 import *

def test_get_gatk_links():
    gatk_links = get_gatk_links("3.5-0")

    assert len(gatk_links.tool_urls) > 2

    assert len(gatk_links.readfilter_urls) > 2

def test_get_gatk_tools():
    get_gatk_tools(
        get_gatk_links("3.5-0")
    )