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
       '  requirements':[{ "class": "ShellCommandRequirement"},
                         { "class": "InlineJavascriptRequirement",
                           "expressionLib": [ "function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                              "function NonNull(x) {if(x === null || x == 'NA') {throw new UserException('NullValue');} else {return x;}}",
                                              """function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} 
                                              else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');}
                                              else if (def =='false') {return '';} else if (def == 'true') {return com;} 
                                              if (def == []) {return '';} else {return com + ' ' + def;}}""",
                                              """function secondaryfiles(f) { return typeof f; }"""]},
                         { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}
  
  #create and write file
  os.chdir(todir)
  fname = jsonf['name']+'.cwl'
  f = open(fname, 'a')
  cwlf_generator(jsonf,cwl)
  f.write(json.dumps(cwl, indent = 4, sort_keys = False)) #write the file
  f.close()




#Combine two json documentations into one
jsonf = {}
jsonf['arguments'] = r['arguments']+d['arguments']
jsonf['name'] = r['name']

#create file
fname = jsonf['name']+'.cwl'
f = open(fname, 'a')

#Define cwl dictionary
cwl = {'id':jsonf['name'],
       'cwlVersion':'v1.0', 
       'baseCommand':[], 
       'class': 'CommandLineTool',
       'requirements':[{ "class": "ShellCommandRequirement"},
                       { "class": "InlineJavascriptRequirement",
                         "expressionLib": [ "function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                            "function NonNull(x) {if(x === null || x == 'NA') {throw new UserException('NullValue');} else {return x;}}",
                                            """function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} 
                                            else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');}
                                            else if (def =='false') {return '';} else if (def == 'true') {return com;} 
                                            if (def == []) {return '';} else {return com + ' ' + def;}}""",
                                            """function secondaryfiles(f) { return typeof f; }"""]},
                       { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}

"""function secondary_files(f) { return typeof f; if (f.indexOf('.cram')!= -1 ){ return '.crai';} 
                                            else if (f.search('.bam')) { return '.bai'; } else if (f.search('.fa')) { return ['.fai','^.dict']; }}"""
                                                                      

cwlf_generator(jsonf,cwl)
f.write(json.dumps(cwl, indent = 4, sort_keys = False)) #write the file
f.close()


