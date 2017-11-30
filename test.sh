#!/bin/bash

set -euf -o pipefail

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

echo "Installing test_requirements in virtualenv"
set -x
pip install -r test_requirements.txt
set +x

echo "Running tests"
set -x
py.test -v gatkcwlgenerator/tests/test.py
set +x

echo "Deactivating virtualenv"
deactivate

echo "Removing tmpdir: ${tmpdir}"
rm -rf "${tmpdir}"

echo "Done."
