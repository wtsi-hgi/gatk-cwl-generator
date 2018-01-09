from .main import *
import gatkcwlgenerator.json2cwl
import gatkcwlgenerator.gen_cwl_arg

import os.path as path

with open(path.join(path.dirname(__file__), "VERSION"), "r") as _version_file:
    __version__ = _version_file.read()