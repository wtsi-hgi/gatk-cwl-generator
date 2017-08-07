"""
The file converts the documentation's json files to cwl files
"""

import json
import os
from helper_functions import *

invalid_args = ['--help', '--defaultBaseQualities']


def cwl_generator(json_, cwl, cmd_line_options):
    """
    Converts GATK tools documented in .json to .cwl (this function changes the cwl parameter)

    Arguments below are classified as invalid for following reasons:
        --DBQ: holds invalid default
        --help: conflicts with cwl-runner '--help'    #issue has been submitted

    :param json: The json file to convert
    :param cwl: A skeleton of the cwl file, which this function will complete.
    """
    com_line = ""
    outputs = []
    inputs = [
        {"doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
        {"doc": "dict file of reference genome", "type": "File", "id": "refDict"}
    ]

    for argument in json_['arguments']:
        if not argument['name'] in invalid_args:
            com_line = argument_writer(argument, inputs, outputs, com_line, cmd_line_options)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs
    if com_line:
        cwl["arguments"] = [{
            "shellQuote": False,
            "valueFrom": com_line
        }]


def json2cwl(GATK_json, cwl_dir, cmd_line_options):
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    skeleton_cwl = {
        'id': GATK_json['name'],
        'cwlVersion': 'v1.0',
        'baseCommand': ['java', '-jar', '/gatk/GenomeAnalysisTK.jar'],
        'class': 'CommandLineTool',
        'requirements': [
            {
                "class": "ShellCommandRequirement"
            }, {
                "class": "InlineJavascriptRequirement",
                "expressionLib": [
                    # Allows you to add annotations
                    "function getFileArgs(f, a){if(a == undefined){return ' ' + f}else{return ':' + a + ' ' + f}}"
                    # TODO: make this more readable
                ]
            }, {
                "dockerPull": "gatk:latest",
                "class": "DockerRequirement"
            }
        ]
    }

    # Create and write the cwl file
    fname = GATK_json['name'] + '.cwl'
    f = open(os.path.join(cwl_dir, fname), 'a')

    cwl_generator(
        GATK_json,
        skeleton_cwl,
        cmd_line_options
    )
    f.write(json.dumps(skeleton_cwl, indent=4,
                       sort_keys=False))  # write the file
    f.close()
