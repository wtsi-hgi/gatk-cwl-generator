from os import sys, path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from gatkcwlgenerator.cwl_type_ast import *

def test_cwl_type_contains():
    assert CWLFloatType().contains(CWLIntType())
    assert not CWLIntType().contains(CWLFloatType())

    assert CWLUnionType(CWLIntType(), CWLFileType()).contains(CWLIntType())
    assert not CWLUnionType(CWLIntType(), CWLFileType()).contains(CWLDirectoryType())

    assert CWLStringType().contains(CWLEnumType(["one", "two"]))

    assert CWLFileType().contains(CWLFileType())
