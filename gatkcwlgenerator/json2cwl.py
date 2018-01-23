"""
The file converts the documentation's json files to cwl files
"""

import os
import re
import logging

from ruamel import yaml
from ruamel.yaml.scalarstring import PreservedScalarString

from .gen_cwl_arg import gatk_argument_to_cwl_arguments
from .helpers import is_gatk_3

_logger = logging.getLogger("gatkcwlgenerator")

invalid_args = [
    "--help",
    "--defaultBaseQualities",
    "--analysis_type"           # this is hard coded into the baseCommand for each tool
]

"""
This indicates gatk modules that require extra undocumented output arguments in gatk3.
These haven't been ported to gatk 4, but when they are, the patched arguments need to be updated.
"""
SPECIAL_GATK3_MODULES = [
    "DepthOfCoverage",
    "RandomlySplitVariants"
]

def cwl_generator(json_, cwl, tool_name, cmd_line_options):
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
            argument_inputs, argument_outputs = gatk_argument_to_cwl_arguments(argument, tool_name, cmd_line_options.version)

            outputs.extend(argument_outputs)

            for argument_input in argument_inputs:
                if "secondaryFiles" in argument_input: # So reference_sequence doesn't conflict with refIndex and refDict
                    inputs.insert(0, argument_input)
                else:
                    inputs.append(argument_input)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

def get_js_library():
    js_library_path = os.path.join(
        os.path.dirname(__file__),
        "js_library.js"
    )

    with open(js_library_path) as file:
        return file.read()


JS_LIBRARY = get_js_library()

# class CWLDescription:
#     def __init__(self, **kwargs):
#         self._init_dict = kwargs

#     def get_argument_by_alias(self, alias: str) -> CWLArgument:
#         pass

#     def to_dict(self) -> Dict:
#         return {
#             **self._init_dict
#         }

def json2cwl(GATK_json, cwl_dir: str, tool_name: str, cmd_line_options):
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    if tool_name in SPECIAL_GATK3_MODULES and not is_gatk_3(cmd_line_options.version):
        _logger.warning(f"Tool {tool_name}'s cwl may be incorrect. The GATK documentation needs to be looked at by a human and hasn't been yet.")

    base_command = cmd_line_options.gatk_command.split(" ")

    if is_gatk_3(cmd_line_options.version):
        base_command.append("--analysis_type")

    base_command.append(GATK_json['name'])

    skeleton_cwl = {
        'id': GATK_json['name'],
        'cwlVersion': 'v1.0',
        'baseCommand': base_command,
        'class': 'CommandLineTool',
        "doc": PreservedScalarString(GATK_json["description"]),
        'requirements': [
            {
                "class": "ShellCommandRequirement"
            },
            {
                "class": "InlineJavascriptRequirement",
                "expressionLib": [
                    PreservedScalarString(JS_LIBRARY)
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
        skeleton_cwl,
        tool_name,
        cmd_line_options
    )

    yaml.round_trip_dump(skeleton_cwl, f)  # write the file
    f.close()
