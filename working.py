"""
The code converts json to cwl files.
(This code converts the gatk-Haplotypecaller3.5 json to cwl.)


-jar /software/hgi/pkglocal/gatk-protected-3.5/GenomeAnalysisTK.jar 
-T HaplotypeCaller 
-R chr22_cwl_test.fa 
-I chr22_cwl_test.cram 
-o chr22.cram_cwl_test.vcf.gz 
-L chr22.interval_list


"""

import requests
import os
import json
from helper_functions import *

#import the json url manually (gatk 3.5-0 version)
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/3.5-0/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json').json()
d = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/3.5-0/org_broadinstitute_gatk_engine_CommandLineGATK.php.json').json()

#import the json documentation from jsonfiles built by the docker
#r = json.load(open('jsonfiles/HaplotypeCaller.json','r'))
#d = json.load(open('jsonfiles/CommandLineGATK.json','r'))


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
                                            """function secondary_files(f) { return typeof f; }"""]},
                       { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}

"""function secondary_files(f) { return typeof f; if (f.indexOf('.cram')!= -1 ){ return '.crai';} 
                                            else if (f.search('.bam')) { return '.bai'; } else if (f.search('.fa')) { return ['.fai','^.dict']; }}"""

# These arguments are classified invalid for following reasons:
#         --DBQ: invalid default
#         --help: argument conflicts with cwl-runner's --help' argument    #issue has been submitted
#         --input_file: I don't know how to deal with secondary files yet sorry
invalid_args = ['--input_file','--reference_sequence','--help', '--defaultBaseQualities']


#converts json to cwl
def cwlf_generator(item,cwlf):
    comLine = ""       
    inputs = [{ "doc": "fasta file of reference genome", "type": "File",
                 "id": "reference_sequence", "secondaryFiles": [".fai","^.dict"]},
               { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
               { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
                 "id": "input_file","secondaryFiles": [".crai","^.dict"]}]      

    outputs = []

    for args in item['arguments']:
      inpt = {}
     
      if args['name'] in invalid_args:
        continue

      inpt['doc'] = args['summary']
      inpt['id'] = args['name'][2:] 

      type_writer(args,inpt)
      output_writer(args,outputs)

      inputs.append(inpt)
      comLine = commandline_writer(args,comLine)
      #print(comLine)
      
      
      if 'requires' in args['fulltext'] and 'index' in args['fulltext']:
        print(args['name'])
        inpt['secondaryFiles'] = '$(secondary_files(self))'

    cwlf["inputs"] = inputs
    cwlf["outputs"] = outputs
    cwlf["arguments"] = [{"shellQuote": False,    
                          "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar  -R $(WDLCommandPart('NonNull(inputs.reference_sequence.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  comLine}] 
                                                                       

cwlf_generator(jsonf,cwl)
f.write(json.dumps(cwl, indent = 4, sort_keys = False)) #write the file
f.close()


