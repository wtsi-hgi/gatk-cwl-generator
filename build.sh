VERSIONS="3.5
3.6
3.7
3.8"

PYTHONPATH=.

for ver in $VERSIONS
do
    python gatkcwlgenerator -v $ver "$@"
done
zip gatk_cmdline_tools gatk_cmdline_tools/*