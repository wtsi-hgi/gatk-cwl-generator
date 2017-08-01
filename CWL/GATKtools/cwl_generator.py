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

    for argument in json['arguments']:
        if argument['name'] in invalid_args:
            continue

        input_writer(argument, inputs)
        output_writer(argument, outputs)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

