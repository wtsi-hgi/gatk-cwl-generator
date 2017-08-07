# gatk-cwl-generator

Generates [CWL](http://www.commonwl.org/v1.0/) files from the [GATK documentation](https://software.broadinstitute.org/gatk/documentation/tooldocs/)

## Installation

First, install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
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

```bash
generate_cwl.py [-h] [-v GATKVERSION] [-out OUTPUTDIR]
                     [-include INCLUDE_FILE]
```

The version defaults to 3.5 and the default out directory is `/cwlscript_[VERSION]/`, where `[VERSION]` is the version of GATK you are using.

The cwl files will be outputted to `cwlfiles` and the JSON files given by the documentation to `jsonfolder`

## Examples

To test the generated CWL files, provided are inputs to the HaplotypeCaller tool. To test assuming you have used the default options and have installed everything as above, run:
```bash
cwl-runner cwlscripts_3.5/HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

## Limitations:

- The parameter `annotation` (in, for example, [HaplotypeCaller](https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php#--annotation)) is specified to take in a string in the generated CWL file, not an enumeration of all the possible options
- All parameters that you can pass to read filters that don't conflict with tool parameters are included and they are marked as optional and no default arguments are specified