#!/bin/bash

set -euf -o pipefail

VERSIONS="3.5
3.6
3.7
3.8"

tmpdir=$(mktemp -d)
builddir="${tmpdir}/gatk_cmdline_tools"
mkdir -p "${builddir}"

for ver in $VERSIONS
do
    PYTHONPATH=. python gatkcwlgenerator -v ${ver} -o "${builddir}/${ver}" "$@"
done
(cd "${tmpdir}"; zip -r gatk_cmdline_tools gatk_cmdline_tools)
(cd "${tmpdir}"; tar zcvf gatk_cmdline_tools.tgz gatk_cmdline_tools)
(cd "${tmpdir}"; tar jcvf gatk_cmdline_tools.tar.bz2 gatk_cmdline_tools)

rm -rf "${tmpdir}"
