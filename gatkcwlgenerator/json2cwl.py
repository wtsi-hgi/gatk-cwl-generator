"""
The file converts the documentation's json files to cwl files
"""

from ruamel import yaml
import os
from .gen_cwl_arg import get_input_objects, get_output_json, is_output_argument
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
    inputs = [
        {"doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
        {"doc": "Dict file of reference genome", "type": "File", "id": "refDict"}
    ]

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

# def minify_js(js):
#     """
#     Basic minification of javascript code
#     """
#     return re.sub("[/][*][\s\S]*?[*][/]", "",             # remove /**/ comments
#         js.replace("    ", "").replace("\n", "")    # remove 4 spaces and new lines (assume semicolons exist)
#     )

JS_LIBARY = get_js_libary()

def json2cwl(GATK_json, cwl_dir, cmd_line_options):
    """
    Make a cwl file with a given GATK json file in the cwl directory
    """

    skeleton_cwl = {
        'id': GATK_json['name'],
        'cwlVersion': 'v1.0',
        'baseCommand': [
            'java',
            '-jar',
            cmd_line_options.gatk_location,
            "--analysis_type",
            GATK_json['name']
            ],
        'class': 'CommandLineTool',
        'requirements': [
            {
                "class": "ShellCommandRequirement"
            },
            {
                "class": "InlineJavascriptRequirement",
                "expressionLib": [
                    JS_LIBARY
                ]
            },
            {
                "class": "DockerRequirement",
                "dockerPull": cmd_line_options.docker_container_name
            }
        ]
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
