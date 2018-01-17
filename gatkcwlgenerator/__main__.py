import sys

if sys.version_info[0] < 3:
    raise Exception("Must run in python 3.")

from . import cmdline_main

cmdline_main()
