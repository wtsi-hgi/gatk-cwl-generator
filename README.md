# gatk-cwl-generator

Generates [CWL](http://www.commonwl.org/v1.0/) files from the [GATK documentation](https://software.broadinstitute.org/gatk/documentation/tooldocs/)

## Installation

First, install the module 
```bash
git clone https://github.com/wtsi-hgi/openstack-tenant-cleaner.git
cd openstack-tenant-cleaner
python setup.py install
```

You may also want to install [cwltool](https://github.com/common-workflow-language/cwltool) to run the generated CWL files

### Docker Requirements

The generated CWL files have a dependency on a GATK docker container. These can be found at https://github.com/wtsi-hgi/arvados-pipelines/tree/master/docker/

To build the gatk-3.5 docker container, run:
```bash
git clone https://github.com/wtsi-hgi/arvados-pipelines
cd arvados-pipelines/docker
docker build gatk-3.5 -t gatk
```

To enter the container, run:
```bash
docker run --name='gatk' -it gatk /bin/bash
```

## Usage

```
usage: gatkcwlgenerator [-h] [--version GATKVERSION] [--out OUTPUTDIR]
                        [--include INCLUDE_FILE] [--dev]
                        [--docker_container_name DOCKER_CONTAINER_NAME]

Generates CWL files from the GATK documentation

optional arguments:
  -h, --help            show this help message and exit
  --version GATKVERSION, -v GATKVERSION
                        Sets the version of GATK to parse documentation for.
                        Default is 3.5
  --out OUTPUTDIR, -o OUTPUTDIR
                        Sets the output directory for generated files. Default
                        is ./cwl_files_<VERSION>
  --include INCLUDE_FILE
                        Only generate this file (note, CommandLinkGATK has to
                        be generated for v3.x)
  --dev                 Enable network caching and overwriting of the
                        generated files (for development purposes)
  --docker_container_name DOCKER_CONTAINER_NAME, -c DOCKER_CONTAINER_NAME
                        Enable network caching and overwriting of the
                        generated files (for development purposes). Default is
                        'gatk'
```

This has been tested on versions 3.5-3.8 and generates files for version 4 (though some parameters are unknown and default to outputting a string).

The input parameters are the same as in the documentation, with the addition of `refIndex` and `refDict` which are required parameters that specify the index and dict file of the reference genome. 

To add tags to arguments that have a file type, add to the parameter `<NAME>_tags`. e.g. to output the parameter `--varient:vcf path\to\file`, use the input:
```yml
varient:
   class: File
   path: path\to\file

varient_tags: [vcf]
```

The cwl files will be outputted to `cwl_files_<VERSION>/cwl` and the JSON files given by the documentation to `cwl_files_<VERSION>/json`.

## Examples

To test the generated CWL files, provided are inputs to the HaplotypeCaller tool. To test assuming you have used the default options and have installed everything as above, run:
```bash
cwl-runner cwl_files_3.5/HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

## Tests

To run the tests, run:

```bash
python tests/test.py
```

## Limitations:

- The parameter `annotation` (for example, in [HaplotypeCaller](https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php#--annotation)) is specified to take in a string in the generated CWL file, not an enumeration of all the possible options
- All parameters that you can pass to read filters that don't conflict with tool parameters are included and they are marked as optional and no default arguments are specified