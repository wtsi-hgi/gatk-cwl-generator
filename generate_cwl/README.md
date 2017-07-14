# CWL Generator for GATK Command Line tools

This script will generate the JSON files from the GATK documentation (found at https://software.broadinstitute.org/gatk/documentation/tooldocs/ depending on the version).

To run, use the following command:

```
$ python generate_cwl.py version /path/to/files
```

For example

```
$ python generate_cwl.py 3.5 /home/pkarnati/cwlscripts
```

The script will create two folders, one with the json scripts and one with cwl scripts.

## Make sure to place `generate_cwl.py` and `json2cwl` in the same directory.
