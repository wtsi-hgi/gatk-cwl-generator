#!/bin/python

"""
The code converts json files to cwl files.
"""

import json
import os
from helper_functions import *
from cwl_generator import cwl_generator


javascript_expr = """
function commandLine_Handler(prefix, required, defval, item){
    if (required == 'yes'){

        if (item != null){
            return "".concat(prefix,' ',item);
        } else {
            if ( defval != "NA" ) {
               return "".concat(prefix,' ', item);
            } else {
                throw new UserException('Required Input');
            }
        }
    } else {
        
        if ( item != null ) {
            return "".concat(prefix,' ',item);
        }  else {
            if ( defval != "NA" ) {
                return "".concat(prefix,' ',defval);
            } else {
                return "";
            }
        }        
    }    
 
}

function assertIsSubset(superset, subset){
    if(!subset.every(element => superset.includes(element))){
        throw new UserException(subset + " is not a subset of " + superset)
    }
}
"""

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
                             "expressionLib": [javascript_expr]},
                            {"dockerPull": "gatk:latest", "class": "DockerRequirement"}]}

    # Create and write the cwl file
    fname = json_with_cmdlineGATK['name'] + '.cwl'
    f = open(os.path.join(cwl_dir, fname), 'a')
    cwl_generator(json_with_cmdlineGATK, skelleton_cwl)
    f.write(json.dumps(skelleton_cwl, indent=4, sort_keys=False))  # write the file
    f.close()
