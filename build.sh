#!/bin/bash

set -euf -o pipefail

generator_version=$(git describe --tags --always)
echo "GATK CWL generator: gatk-cwl-generator-${generator_version}"

#VERSIONS=( 3.5-0 3.6-0 3.7-0 3.8-0 4.beta.6 )
VERSIONS=( 4.beta.6 )

tarbase="gatk-cwl-generator-${generator_version}-gatk_cmdline_tools"

tmpdir=$(mktemp -d)
python_bin=$(which python)
echo "Using ${python_bin} to generate temporary virtualenv ${tmpdir}/venv"
set -x
${python_bin} -m virtualenv "${tmpdir}/venv"
set +x
echo "Activating virtualenv in ${tmpdir}/venv"
set +u # virtualenv activate script references unset vars
. "${tmpdir}/venv/bin/activate"
set -u

echo "Installing requirements in virtualenv"
set -x
pip install -r requirements.txt
set +x

builddir="${tmpdir}/${tarbase}"
mkdir -p "${builddir}"
echo "Building CWL in ${builddir} for GATK versions ${VERSIONS[@]}"

for ver in ${VERSIONS[@]}
do
    echo "Generating CWL for GATK version ${ver}"
    set -x
    PYTHONPATH=. python gatkcwlgenerator -v ${ver} -o "${builddir}/${ver}" "$@"
    set +x
done

echo "Deactivating virtualenv"
deactivate

echo "Generating zip file"
( cd "${tmpdir}"; zip -r ${tarbase} ${tarbase} )
cp "${tmpdir}/${tarbase}.zip" ./

echo "Generating tgz file"
( cd "${tmpdir}"; tar zcvf ${tarbase}.tgz ${tarbase}/ )
cp "${tmpdir}/${tarbase}.tgz" ./

echo "Generating .tar.bz2 file"
( cd "${tmpdir}"; tar jcvf ${tarbase}.tar.bz2 ${tarbase}/ )
cp "${tmpdir}/${tarbase}.tar.bz2" ./

echo "Removing tmpdir: ${tmpdir}"
rm -rf "${tmpdir}"

echo "Done."
