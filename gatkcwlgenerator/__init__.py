import sys

if sys.version_info[0] < 3:
    raise Exception("Must run in Python 3.")

from .main import *
import gatkcwlgenerator.web_to_gatk_tool
import gatkcwlgenerator.gatk_tool_to_cwl
import gatkcwlgenerator.gatk_argument_to_cwl

import os.path as path

with open(path.join(path.dirname(__file__), "VERSION"), "r") as _version_file:
    __version__ = _version_file.read()
