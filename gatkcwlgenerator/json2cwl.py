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
from .GATK_classes import *

_logger = logging.getLogger("gatkcwlgenerator")

INVALID_ARGS = [
    "help",
    "defaultBaseQualities",
    "analysis_type"           # this is hard coded into the baseCommand for each tool
]

"""
This indicates gatk modules that require extra undocumented output arguments in gatk3.
These haven't been ported to gatk 4, but when they are, the patched arguments need to be updated.
"""
SPECIAL_GATK3_MODULES = [
    "DepthOfCoverage",
    "RandomlySplitVariants"
]

def get_js_library():
    js_library_path = os.path.join(
        os.path.dirname(__file__),
        "js_library.js"
    )

    with open(js_library_path) as file:
        return file.read()


JS_LIBRARY = get_js_library()

def json2cwl(gatk_tool: GATKTool, cmd_line_options):
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    if gatk_tool.name in SPECIAL_GATK3_MODULES and not is_gatk_3(cmd_line_options.version):
        _logger.warning(f"Tool {gatk_tool.name}'s cwl may be incorrect. The GATK documentation needs to be looked at by a human and hasn't been yet.")

    base_command = cmd_line_options.gatk_command.split(" ")

    if is_gatk_3(cmd_line_options.version):
        base_command.append("--analysis_type")

    base_command.append(gatk_tool.name)

    cwl = {
        'id': gatk_tool.name,
        'cwlVersion': 'v1.0',
        'baseCommand': base_command,
        'class': 'CommandLineTool',
        "doc": PreservedScalarString(gatk_tool.dict.description),
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

    outputs = []
    inputs = []

    for argument in gatk_tool.arguments:
        if not argument.name in INVALID_ARGS:
            argument_inputs, argument_outputs = gatk_argument_to_cwl_arguments(
                argument,
                gatk_tool.name,
                cmd_line_options.version
            )

            outputs.extend(argument_outputs)

            for argument_input in argument_inputs:
                if "secondaryFiles" in argument_input: # So reference_sequence doesn't conflict with refIndex and refDict
                    inputs.insert(0, argument_input)
                else:
                    inputs.append(argument_input)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

    return cwl
