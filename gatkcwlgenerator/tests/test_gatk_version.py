from gatkcwlgenerator.common import GATKVersion as v


def test_version_comparisons():
    assert v("4") == v("4.0") == v("4.0.0")
    assert v("4.0.5.0") < v("4.0.6.0")
    assert v("3.8-0") > v("3.5-0")
    assert v("4.beta.6") < v("4.0.0.0")
