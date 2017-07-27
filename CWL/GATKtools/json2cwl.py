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

    skelleton_cwl = {'id': json_with_cmdlineGATK['name'],
           'cwlVersion': 'v1.0',
           'baseCommand': [],
           'class': 'CommandLineTool',
           'requirements': [{"class": "ShellCommandRequirement"},
                            {"class": "InlineJavascriptRequirement",
                             "expressionLib": ["function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                               "function NonNull(x) {if(x === null || x == 'NA') {throw new UserException('NullValue');} else {return x;}}",
                                               """function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} 
                                              else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');}
                                              else if (def =='false') {return '';} else if (def == 'true') {return com;} 
                                              if (def == []) {return '';} else {return com + ' ' + def;}}""",
                                               """function secondaryfiles(f) { return typeof f; }"""]},
                            {"dockerPull": "gatk:latest", "class": "DockerRequirement"}]}

    # Create and write the cwl file
    fname = json_with_cmdlineGATK['name'] + '.cwl'
    f = open(os.path.join(cwl_dir, fname), 'a')
    cwl_generator(json_with_cmdlineGATK, skelleton_cwl)
    f.write(json.dumps(skelleton_cwl, indent=4, sort_keys=False))  # write the file
    f.close()
