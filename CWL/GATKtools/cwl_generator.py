#!/bin/python

from helper_functions import *

invalid_args = ['--help', '--defaultBaseQualities']

"""
Converts GATK tools in .json to .cwl (this function changes the cwl parameter)

Arguments below are classified as invalid for following reasons:
     --DBQ: holds invalid default
     --help: conflicts with cwl-runner '--help'    #issue has been submitted

:param json: The json file to convert
:param cwl: A skeleton of the cwl file, which this function will complete.
"""
def cwl_generator(json, cwl):
    com_line = ""
    outputs = []
    inputs = [{"doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"}]

    for argument in json['arguments']:
        if argument['name'] in invalid_args:
            continue

        argument_writer(argument, inputs, outputs, com_line)
#        output_commandline_writer(argument,com_line,inputs,outputs)
        # com_line = commandline_writer(argument, com_line)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs
#    cwl["arguments"] = { "shellQuote": False,
#                         "valueFrom": com_line }
