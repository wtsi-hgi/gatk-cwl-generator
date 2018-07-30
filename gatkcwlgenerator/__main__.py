import sys

if sys.version_info[0] < 3:
    raise Exception("Must run in Python 3.")

from gatkcwlgenerator import cmdline_main

cmdline_main()
