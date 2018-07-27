import pytest
import requests_cache

from gatkcwlgenerator.common import GATKVersion


requests_cache.install_cache()


EG_3 = "3.5-0"
EG_4 = "4.0.0.0"
# TODO: can we add a "current" version that has caching disabled?


@pytest.fixture(params=[EG_3, EG_4])
def gatk_version(request):
    return GATKVersion(request.param)
