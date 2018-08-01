"""Configuration for pytest."""


import pytest
import requests_cache

from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.tests.globals import TESTED_VERSIONS


requests_cache.install_cache()


@pytest.fixture(params=TESTED_VERSIONS)
def gatk_version(request) -> GATKVersion:
    """Given a version number, return a GATKVersion."""
    return GATKVersion(request.param)
