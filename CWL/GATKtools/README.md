# GATK tools

This script will generate the JSON files from the GATK documentation (found at https://software.broadinstitute.org/gatk/documentation/tooldocs/ depending on the version).

First, install the required dependencies by running the following command:
```
$ pip install -r requirements.txt
```

To run, use the following command:
```
$ python generate_cwl.py [-v gatk_version] [-out /path/to/desired/output/directory] 
```
If the version of the GATKtools documentation or the directory to save generated files are unspecified, 
the default is set to GATK version 3.5-0 (type `current` for the most current version) and the default directory is set to current working directory.
The script will automatically create a `cwlfiles` folder in the specified directory which contains two folders `jsonfolder` and `cwlfiles` each containing gatk tool documentations in json format and translations in cwl.
