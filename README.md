# PY

Build the gatk-3.5 docker from https://github.com/yejinyou/arvados-pipelines/tree/master/docker/gatk-3.5.
```
docker build gatk-3.5 -t gatk
```

Enter the gatk container with: 
``` 
docker run -it gatk /bin/bash 
```

Copy the HaplotypeCaller and GATK tools documentation files to your localhost.
```
docker cp CONTAINERID:SRC_PATH DEST_PATH
``` 

#Maybe consider making a bash script that would build the docker and copy the files to the local directory.


Follow the instructions to install cwltools and cwl-runner: https://github.com/common-workflow-language/cwltool


To test generated HaplotypeCaller CWL files, invoke ```cwl-runner``` and provide the tool wrapper and the input object on the command line.
```
$ cwl-runner HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

