"""
converts GATK tools in .json to .cwl

Arguments below are classified as invalid for following reasons:
     --DBQ: holds invalid default
     --help: conflicts with cwl-runner '--help'    #issue has been submitted
"""

from helper_functions import *

invalid_args = ['--help', '--defaultBaseQualities']

def cwlf_generator(item,cwlf):
    comLine = ""       
    outputs = []
    inputs = [{"doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"}]

    for args in item['arguments']:

      if args['name'] in invalid_args:
        continue

      input_writer(args,inputs)
      output_writer(args,outputs)
      comLine = commandline_writer(args,comLine)


    cwlf["inputs"] = inputs
    cwlf["outputs"] = outputs
    cwlf["arguments"] = [{"shellQuote": False,    
                          "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar  " +  comLine}] 

