#!/bin/bash

set -euf -o pipefail

VERSIONS="3.5
3.6
3.7
3.8"


for ver in $VERSIONS
do
    PYTHONPATH=. python gatkcwlgenerator -v $ver "$@"
done
zip -r gatk_cmdline_tools gatk_cmdline_tools
tar zcvf gatk_cmdline_tools.tgz gatk_cmdline_tools
tar jcvf gatk_cmdline_tools.tar.bz2 gatk_cmdline_tools
