# Docker Requirements

Build the gatk-3.5 docker from https://github.com/wtsi-hgi/arvados-pipelines/tree/master/docker/gatk-3.5.
```
docker build gatk-3.5 -t gatk
```
If you want to enter the container, enter the gatk container with: 
``` 
docker run --name='CONTAINERNAME' -it IMAGE /bin/bash 
(docker run --name='gatk' -it gatk /bin/bash)
```

Copy the HaplotypeCaller and GATK tools documentation files to your localhost. 
```
docker cp CONTAINERID:SRC_PATH DEST_PATH   
(docker cp gatk:/jsonfiles ~/PY)
```
## CWL/GATKtools/

This script will generate the JSON files from the GATK documentation (found at https://software.broadinstitute.org/gatk/documentation/tooldocs/ depending on the version).

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


## HaplotypeCaller

Follow the instructions to install cwltools and cwl-runner: https://github.com/common-workflow-language/cwltool

To test generated HaplotypeCaller CWL files, invoke ```cwl-runner``` and provide the tool wrapper and the input object on the command line.
```
$ cwl-runner HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

