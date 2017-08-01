"""
The code converts json files to cwl files.
"""

import requests
import os
import json
from helper_functions import *
from cwl_generator import cwlf_generator

#import the json url manually (gatk 3.5-0 version)
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/3.5-0/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json').json()
d = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/3.5-0/org_broadinstitute_gatk_engine_CommandLineGATK.php.json').json()

def make_cwl(fromdir, todir, jsonfile):
  try:
    r = json.load(open(os.path.join(fromdir, jsonfile),'r'))
    d = json.load(open(os.path.join(fromdir, 'CommandLineGATK.json'),'r'))
  except Exception as e:
    print e.message
    raise e
  
  jsonf = {'arguments':r['arguments']+d['arguments'],'name':r['name']}

  cwl = {'id':jsonf['name'],
         'cwlVersion':'v1.0', 
         'baseCommand':[], 
         'class': 'CommandLineTool',
         'requirements':[{ "class": "ShellCommandRequirement"},
                         { "class": "InlineJavascriptRequirement",
                           "expressionLib": ["""function commandLine_Handler(prefix, required, defval, item){
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
      
}"""] },
                   { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}



  #create and write file
  os.chdir(todir)
  fname = jsonf['name']+'.cwl'
  f = open(fname, 'a')
  cwlf_generator(jsonf,cwl)
  f.write(json.dumps(cwl, indent = 4, sort_keys = False)) #write the file
  f.close()






