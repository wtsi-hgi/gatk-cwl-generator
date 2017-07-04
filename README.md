# PY

Build the gatk-3.5 docker from https://github.com/yejinyou/arvados-pipelines/tree/master/docker/gatk-3.5.
```
docker build gatk-3.5 -t gatk
```

Enter the gatk container with: 
``` 
docker run -i -t gatk /bin/bash 
```
Follow the instructions to install cwltools and cwl-runner: https://github.com/common-workflow-language/cwltool


To test generated HaplotypeCaller CWL files, invoke ```cwl-runner``` and provide the tool wrapper and the input object on the command line.
```
$ cwl-runner HaplotypeCaller.cwl HaplotypeCaller_inputs.yml
```

