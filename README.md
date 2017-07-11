# Docker Requirements

Build the gatk-3.5 docker from https://github.com/yejinyou/arvados-pipelines/tree/master/docker/gatk-3.5.
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

# HaplotypeCaller

Follow the instructions to install cwltools and cwl-runner: https://github.com/common-workflow-language/cwltool

Run json2cwl.py to generate HaplotypeCaller.cwl file from the jsonfiles from the Docker.
```
python json2cwl.py
```

To test generated HaplotypeCaller CWL files, invoke ```cwl-runner``` and provide the tool wrapper and the input object on the command line.
```
$ cwl-runner HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

#Consider turning json2cwl.py into Cwlrunner format
