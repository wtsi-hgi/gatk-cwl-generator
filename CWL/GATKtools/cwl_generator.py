#!/bin/python

from helper_functions import *

invalid_args = ['--help', '--defaultBaseQualities']

"""
Converts GATK tools in .json to .cwl (this function changes the cwl parameter)

Arguments below are classified as invalid for following reasons:
     --DBQ: holds invalid default
     --help: conflicts with cwl-runner '--help'    #issue has been submitted

:param json: The json file to convert
:param cwl: A skelleton of the cwl file, which this function will complete.
"""
def cwl_generator(json, cwl):
    com_line = ""
    outputs = []
    inputs = [{"doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"}]

    for args in json['arguments']:
        if args['name'] in invalid_args:
            continue

        input_writer(args, inputs)
        output_writer(args, outputs)
        com_line = commandline_writer(args, com_line)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs
    cwl["arguments"] = [{"shellQuote": False,
                         "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar  " +  com_line}] 
