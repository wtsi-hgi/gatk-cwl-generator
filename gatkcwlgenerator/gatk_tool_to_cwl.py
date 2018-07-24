"""
GATKTool -> CWL Dict
"""

import os
import logging

from ruamel.yaml.scalarstring import PreservedScalarString

from .gatk_argument_to_cwl import gatk_argument_to_cwl
from .common import GATKVersion
from .GATK_classes import *

_logger = logging.getLogger("gatkcwlgenerator")

INVALID_ARGS = [
    "help",
    "defaultBaseQualities",
    "analysis_type"  # this is hard coded into the baseCommand for each tool
]

# This indicates gatk modules that require extra undocumented output arguments in gatk3.
# These haven't been ported to gatk 4, but when they are, the patched arguments need to be updated.
SPECIAL_GATK3_MODULES = [
    "DepthOfCoverage",
    "RandomlySplitVariants"
]

def get_js_library() -> str:
    js_library_path = os.path.join(
        os.path.dirname(__file__),
        "js_library.js"
    )

    with open(js_library_path) as file:
        return file.read()


JS_LIBRARY = get_js_library()

def gatk_tool_to_cwl(gatk_tool: GATKTool, cmd_line_options, annotation_names: List[str]) -> Dict:
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    version = GATKVersion(cmd_line_options.version)

    if gatk_tool.name in SPECIAL_GATK3_MODULES and not version.is_3():
        _logger.warning(f"Tool {gatk_tool.name}'s cwl may be incorrect. The GATK documentation needs to be looked at by a human and hasn't been yet.")

    base_command = cmd_line_options.gatk_command.split(" ")

    if version.is_3():
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
            },
            {
                "class": "SchemaDefRequirement",
                "types": [{
                    "type": "enum",
                    "name": "annotation_type",
                    "symbols": annotation_names
                }]
            }
        ] + ([] if cmd_line_options.no_docker else [{
            "class": "DockerRequirement",
            "dockerPull": cmd_line_options.docker_image_name
        }])
    }

    # Create and write the cwl file

    outputs = []
    inputs = []

    for argument in gatk_tool.arguments:
        if argument.name not in INVALID_ARGS:
            argument_inputs, argument_outputs = gatk_argument_to_cwl(
                argument,
                gatk_tool.name,
                version
            )

            synonym = argument.synonym
            if synonym is not None and len(argument_inputs) >= 1 and synonym.lstrip("-") != argument.name.lstrip("-"):
                argument_inputs[0]["doc"] += f" [synonymous with {synonym}]"

            outputs.extend(argument_outputs)

            for argument_input in argument_inputs:
                if "secondaryFiles" in argument_input:  # So reference_sequence doesn't conflict with refIndex and refDict
                    inputs.insert(0, argument_input)
                else:
                    inputs.append(argument_input)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

    return cwl
