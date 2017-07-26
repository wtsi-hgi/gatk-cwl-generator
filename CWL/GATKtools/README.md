# GATK tools

This script will generate the JSON files from the GATK documentation (found at https://software.broadinstitute.org/gatk/documentation/tooldocs/ depending on the version).

First, install the required dependencies by running the following command:
```
$ pip install -r requirements.txt
```

To run, use the following command:
```
$ python generate_cwl.py gatk_version /path/to/dir/for/generated/files
```
If the version of the GATKtools documentation or the directory to save generated files are unspecified, 
the default is set to GATK version 3.5-0 (the most current version is 3.7-0) and the script will automatically create `cwlfiles` folder in current working directory.
```
$ python generate_cwl.py (3.5) (/current/working/directory/cwlfiles)
```

The script will create two folders inside the specified directory called `jsonfolder` with the json scripts and `cwlfiles` with translated cwl scripts.

