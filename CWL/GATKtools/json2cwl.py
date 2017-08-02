#!/bin/python

"""
The code converts json files to cwl files.
"""

import json
import os
from helper_functions import *
from cwl_generator import cwl_generator

def make_cwl(json_dir, cwl_dir, json_file_path):
    json_file = json.load(open(os.path.join(json_dir, json_file_path), 'r'))
    commandlineGATK = json.load(open(os.path.join(json_dir, 'CommandLineGATK.json'), 'r'))

    json_with_cmdlineGATK = {'arguments': json_file['arguments'] + commandlineGATK['arguments'], 'name': json_file['name']}

    skeleton_cwl = {'id': json_with_cmdlineGATK['name'],
           'cwlVersion': 'v1.0',
           'baseCommand': ['java','-jar','/gatk/GenomeAnalysisTK.jar'],
           'class': 'CommandLineTool',
           'requirements': [{"class": "ShellCommandRequirement"},
                            {"class": "InlineJavascriptRequirement"},
                            {"dockerPull": "gatk:latest", "class": "DockerRequirement"}]}

    # Create and write the cwl file
    fname = json_with_cmdlineGATK['name'] + '.cwl'
    f = open(os.path.join(cwl_dir, fname), 'a')
    cwl_generator(json_with_cmdlineGATK, skeleton_cwl)
    f.write(json.dumps(skeleton_cwl, indent=4, sort_keys=False))  # write the file
    f.close()
