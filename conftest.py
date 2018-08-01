"""Configuration for pytest."""


import pytest
import requests_cache

from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.GATK_classes import GATKTool
from gatkcwlgenerator.tests.globals import TESTED_VERSIONS
from gatkcwlgenerator.web_to_gatk_tool import get_gatk_tool


requests_cache.install_cache()


@pytest.fixture(params=TESTED_VERSIONS)
def gatk_version(request) -> GATKVersion:
    """Given a version number, return a GATKVersion."""
    return GATKVersion(request.param)


@pytest.fixture
def gatk_tool(request) -> GATKTool:
    """Given a tuple of (tool URL, extra arguments), return a tool."""
    return get_gatk_tool(*request.param)
