"""
The file converts the documentation's json files to cwl files
"""

from ruamel import yaml
from ruamel.yaml.scalarstring import PreservedScalarString
import os
from .gen_cwl_arg import get_input_objects, get_output_json, is_output_argument
from .helpers import is_gatk_3
import re

invalid_args = [
    "--help",
    "--defaultBaseQualities",
    "--analysis_type"           # this is hard coded into the baseCommand for each tool
]

def cwl_generator(json_, cwl):
    """
    Converts GATK tools documented in .json to .cwl (this function changes the cwl parameter)

    Arguments below are classified as invalid for following reasons:
        --DBQ: holds invalid default
        --help: conflicts with cwl-runner '--help'    #issue has been submitted

    :param json: The json file to convert
    :param cwl: A skeleton of the cwl file, which this function will complete.
    """
    outputs = []
    inputs = []

    for argument in json_['arguments']:
        if not argument['name'] in invalid_args:
            if is_output_argument(argument):
                output_json = get_output_json(argument)
                outputs.append(output_json)

            input_objects_for_arg = get_input_objects(argument)

            for input_object in input_objects_for_arg:
                if "secondaryFiles" in input_object: # So reference_sequence doesn't conflict with refIndex and refDict
                    inputs.insert(0, input_object)
                else:
                    inputs.append(input_object)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

def get_js_libary():
    js_libary_path = os.path.join(
        os.path.dirname(__file__),
        "js_libary.js"
    )

    with open(js_libary_path) as file:
        return file.read()


JS_LIBARY = get_js_libary()

def json2cwl(GATK_json, cwl_dir, cmd_line_options):
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    base_command = cmd_line_options.gatk_command.split(" ")

    if is_gatk_3(cmd_line_options.version):
        base_command.append("--analysis_type")

    base_command.append(GATK_json['name'])

    skeleton_cwl = {
        'id': GATK_json['name'],
        'cwlVersion': 'v1.0',
        'baseCommand': base_command,
        'class': 'CommandLineTool',
        'requirements': [
            {
                "class": "ShellCommandRequirement"
            },
            {
                "class": "InlineJavascriptRequirement",
                "expressionLib": [
                    PreservedScalarString(JS_LIBARY)
                ]
            }
        ] + ([]
            if cmd_line_options.no_docker else
            [{
                "class": "DockerRequirement",
                "dockerPull": cmd_line_options.docker_image_name
            }])
    }

    # Create and write the cwl file
    fname = GATK_json['name'] + '.cwl'
    f = open(os.path.join(cwl_dir, fname), 'a')

    cwl_generator(
        GATK_json,
        skeleton_cwl
    )

    yaml.round_trip_dump(skeleton_cwl, f)  # write the file
    f.close()
