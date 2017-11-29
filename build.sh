#!/bin/bash

set -euf -o pipefail

VERSIONS=( 3.5 3.6 3.7 3.8 4.beta-latest )

tmpdir=$(mktemp -d)
builddir="${tmpdir}/gatk_cmdline_tools"
mkdir -p "${builddir}"
echo "Building CWL in ${builddir} for GATK ${VERSIONS[@]}"

for ver in ${VERSIONS[@]}
do
    echo "Generating CWL for GATK version ${ver}"
    PYTHONPATH=. python gatkcwlgenerator -v ${ver} -o "${builddir}/${ver}" "$@"
done

echo "Generating zip file"
( cd "${tmpdir}"; zip -r gatk_cmdline_tools gatk_cmdline_tools )
cp "${tmpdir}/gatk_cmdline_tools.zip" ./

echo "Generating tgz file"
( cd "${tmpdir}"; tar zcvf gatk_cmdline_tools.tgz gatk_cmdline_tools/ )
cp "${tmpdir}/gatk_cmdline_tools.tgz" ./

echo "Generating .tar.bz2 file"
( cd "${tmpdir}"; tar jcvf gatk_cmdline_tools.tar.bz2 gatk_cmdline_tools/ )
cp "${tmpdir}/gatk_cmdline_tools.tar.bz2" ./

echo "Removing tmpdir: ${tmpdir}"
rm -rf "${tmpdir}"

echo "Done."
