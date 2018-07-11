# gatk-cwl-generator

Generates [CWL](http://www.commonwl.org/v1.0/) files from the [GATK documentation](https://software.broadinstitute.org/gatk/documentation/tooldocs/)

## Installation

First, install the module
```bash
git clone https://github.com/wtsi-hgi/gatk-cwl-generator
cd gatk-cwl-generator
python setup.py install
```

You may also want to install [cwltool](https://github.com/common-workflow-language/cwltool) to run the generated CWL files

## Requirements

- Python 3
- Docker and node.js for the tests

## Usage

```
usage: gatk_cwl_generator [-h] [--version VERSION] [--verbose] [--out OUTPUT_DIR]
                          [--include INCLUDE] [--dev] [--use_cache [CACHE_LOCATION]]
                          [--no_docker] [--docker_image_name DOCKER_IMAGE_NAME]
                          [--gatk_command GATK_COMMAND]

Generates CWL files from the GATK documentation

optional arguments:
  -h, --help            show this help message and exit
  --version VERSION, -v VERSION
                        Sets the version of GATK to parse documentation for.
                        Default is 3.5-0
  --verbose             Set the logging to be verbose. Default is False.
  --out OUTPUT_DIR, -o OUTPUT_DIR
                        Sets the output directory for generated files. Default
                        is ./gatk_cmdline_tools/<VERSION>/
  --include INCLUDE     Only generate this file (note, CommandLinkGATK has to
                        be generated for v3.x)
  --dev                 Enable --use_cache and overwriting of the generated
                        files (for development purposes). Requires
                        requests_cache to be installed
  --use_cache [CACHE_LOCATION]
                        Use requests_cache, using the cache at CACHE_LOCATION,
                        or 'cache' if not specified. Default is False.
  --no_docker           Make the generated CWL files not use docker
                        containers. Default is False.
  --docker_image_name DOCKER_IMAGE_NAME, -c DOCKER_IMAGE_NAME
                        Docker image name for generated cwl files. Default is
                        'broadinstitute/gatk3:<VERSION>' for version 3.x and
                        'broadinstitute/gatk:<VERSION>' for 4.x
  --gatk_command GATK_COMMAND, -l GATK_COMMAND
                        Command to launch GATK. Default is 'java -jar
                        /usr/GenomeAnalysisTK.jar' for gatk 3.x and 'java -jar
                        /gatk/gatk.jar' for gatk 4.x
```

This has been tested on versions 3.5-0 to 3.8-0 and 4.beta.6.

The parameters generated are the same as you would need to specify on the command line, with "--" stripped from the beginning.

To add tags to arguments that have a file type, add to the parameter `<NAME>_tags`. e.g. to output the parameter `--variant:vcf path\to\file`, use the input:
```yml
variant:
   class: File
   path: path\to\file

variant_tags: [vcf]
```

For convenience, you can also specify any array input argument as a single element.

The cwl files will be outputted to `gatk_cmdline_tools/<VERSION>/cwl` and the JSON files given by the documentation to `gatk_cmdline_tools/<VERSION>/json`.

## Generated CWL files

- The input parameters of all cwl files have the same id as they would be used on the command line
- The output parameters id's are of the format `<NAME>Output`
- All read filter parameters are included as optional parameters in every tool, if they don't conflict with input parameters
- Types of parameters are mostly what is specified in the documentation, corrected in a couple of places
- The type of the input parameter `annotation` is a string, not an enumeration of all the possible options
- Array types in the documentation are implemented as a union of the base type and the array type

## Examples

To test the generated CWL files, provided are inputs to the HaplotypeCaller tool. To test assuming you have used the default options and have installed everything as above, run:
```bash
cwl-runner gatk_cmdline_tools/3.5/HaplotypeCaller.cwl examples/HaplotypeCaller_inputs.yml
```

The generated CWL files can also be found in the [releases](https://github.com/wtsi-hgi/gatk-cwl-generator/releases)

## Tests

Install the tests requirements, then run the tests. Note: docker must be installed in order to run the tests (the cwl files are tested during the tests):
```bash
pip install -r test_requirements.txt
pytest gatkcwlgenerator
```

You can also run the tests in parallel with `-n` to improve performance

## Limitations:

- The parameter `annotation` (for example, in [HaplotypeCaller](https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php#--annotation)) is specified to take in a string in the generated CWL file, not an enumeration of all the possible options
- All parameters that you can pass to read filters that don't conflict with tool parameters are included and they are marked as optional

## Creating a new version

To create a `gatk_cmdline_tools.zip` zip file containing all the generated cwl files for gatk versions 3.5, 3.6, 3.7, 3.8 and 4.0.0.0, run `bash build.sh`. This file is uploaded as a release on GitHub for every new release of this package.
