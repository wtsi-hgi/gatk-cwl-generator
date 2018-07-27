import pytest

from gatkcwlgenerator.common import GATKVersion


EG_3 = "3.5-0"
EG_4 = "4.0.0.0"


@pytest.fixture(params=[EG_3, EG_4])
def gatk_version(request):
    return GATKVersion(request.param)
