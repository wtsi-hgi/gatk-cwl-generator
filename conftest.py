"""Configuration for pytest."""


import pytest
import requests_cache

from gatkcwlgenerator.common import GATKVersion


requests_cache.install_cache()


TESTED_VERSIONS = [
    "3.5-0",
    "3.8-0",
    "4.0.0.0",
    "4.0.6.0",
    "4.0.7.0",
]


@pytest.fixture(params=TESTED_VERSIONS)
def gatk_version(request) -> GATKVersion:
    """Given a version number, return a GATKVersion."""
    return GATKVersion(request.param)
