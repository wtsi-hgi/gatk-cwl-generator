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



#=======================================================================================
#helps form a commandline
def need_def(arg):
    if 'List' in arg['type']:
        if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
            arg['defaultValue'] = []
        else:
            arg['defaultValue'] = [str(a) for a in arg['defaultValue'][1:-1].split(',')]
    if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
        return False
    if ('boolean' in arg['type'] or 'List' in arg['type']) or 'false' in arg['defaultValue']:
        return True
    return False


def output_writer(args,outputs=[]):
  if 'writer' in args['type'].lower():
    outpt = {'id': args['name'], 'type': ['null','File'], 'outputBinding':{'glob':'$(inputs.'+args['name'][2:]+')'}}
    outputs.append(outpt)

def command_line_writer(args,comLine=""):
    if need_def(args):
        comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + str(args['defaultValue'])  + "))) "
    else:
        if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
           comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + args['defaultValue'] + "')) "
        elif args['synonyms'] == '-o':
           comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', "+"'stdout'"+"))) "
        else:
           comLine += "$(WDLCommandPart('\"" + args['synonyms'] + "\" + NonNull(inputs." + args['name'].strip("-") + ")', ' ')) " 



#=======================================================================================






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
                                            """function secondary_files(f) { return typeof f; if (f.indexOf('.cram')!= -1 ){ return '.crai';} 
                                            else if (f.search('.bam')) { return '.bai'; } else if (f.search('.fa')) { return ['.fai','^.dict']; }}"""]},
                       { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}







# These arguments are classified invalid for following reasons:
#         --DBQ: invalid default
#         --help: argument conflicts with cwl-runner's --help' argument    #issue has been submitted
#         --input_file: I don't know how to deal with secondary files yet sorry
invalid_args = ['--input_file','--reference_sequence','--help', '--defaultBaseQualities']

#def get_file_type(f):

#$("."+(inputs.input_file).split('.')[1].replace("m","i"))



#given an argument and a dictionary to write the files in, it writes the secondary files for that argument
#input = {}

##  $("."+(inputs.input_file).split('.')[1].replace("m","i"))

'''
'cram' in $(inputs.input_file) ? "crai" : "bai"

'''


# function secondary_files(f) {
#   if (f.includes('.cram') ){ return '.crai';} else if (f.includes('.bam')) { return '.bai'; } else if (f.includes('.fa')) { return ['.fai','^.dict']; }
#     }

  # secondaryfiles = []
  # if 'dictionary' in args['fulltext']:
  #   secondaryfiles += '^.dict'
  # if 'index' in args['fulltext']:
  #   secondaryfiles += "$('.'+(inputs." + args['name'] + ").split('.')[1].replace('m','i'))"
# def add_secondary_files(args, inpt): #return secondary file in [ '.crai'] formet
#   if 'required' not in args['fulltext']:
#     pass
#   else:
#     if 'dictionary' in args['fulltext']:
#       secondaryfiles = ['^.dict','^fai']
#     elif 'index' in args['fulltext']: #CRAM / BAM for input_files
#       print('requires and index: only input should have this', args['name'])
#       secondaryfiles = ["$('.'+(inputs." + args['name'] + ").split('.')[1].replace('m','i'))"]

      
      # "$('.'+(inputs." + args['id'] + ").split('.')[1].replace('m','i'))""




################################################################################################################################
#interval, filewriter 
################################################################################################################################
def convt_type(typ):
  #  typ = args['type'].lower()
 #   if 'list' in typ:
#       typ = typ[5:-1]
    if typ in ('integer','byte'):
        return 'int'
#    elif typ == 'intervalbinding[feature]':
#        pass        
    elif typ == 'file':
        return 'File'
    elif typ in ('long','double','int','string','float','boolean','bool'):
        return typ
    elif 'rodbinding' in typ: #ROD file, File to which output should be written
        return 'File'
    #file writer: take in as an input string
    elif 'writer' in typ or 'rule' in typ or 'option' in typ or 'timeunit' in typ or 'type' in typ or 'mode' in typ or 'validationstringency' in typ: #minutes pedigreevalidationtype, gatkvcfindextype, downsampletype ...
        return 'string'
    elif 'printstream' in typ:
        return 'null'
    else:
#        print('typeerror',typ)   
        return 'string'
        #temporary measurement`
        #raise ValueError("unsupported type %s" %(typ)) 

#helps form a commandline
def need_def(arg):
    if 'List' in arg['type']:
        if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
            arg['defaultValue'] = []
        else:
            arg['defaultValue'] = [str(a) for a in arg['defaultValue'][1:-1].split(',')]
    if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
        return False
    if ('boolean' in arg['type'] or 'List' in arg['type']) or 'false' in arg['defaultValue']:
        return True
    return False

#converts json to cwl
def cwlf_generator(item,cwlf):
    comLine = ""
   # inputs = [{ "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
    #          { "doc": "dict file of reference genome", "type": "File", "id": "refDict"}]          

    inputs = [{ "doc": "fasta file of reference genome", "type": "File",
                 "id": "reference_sequence", "secondaryFiles": [".fai","^.dict"]},
               { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
               { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
                 "id": "input_file","secondaryFiles": [".crai","^.dict"]}]      
#    inputs = [ { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
 #                "id": "input_file","secondaryFiles": [".crai","^.dict"]}]
###########
###   if need secondaryfiles:
####       inpt['secondaryfiles'] = get_secondary_files(arg)
#######

    outputs = []

    for args in item['arguments']:
      inpt = {}
     
      if args['name'] in invalid_args:
        #print(args['name']) ###NEED TO DO STH ABOUT IT
        continue

      if args['required'] == 'yes':
        print(args)
        continue
        ################################################################ANALYSIS TYPE
      else: #if not required
        inpt['doc'] = args['summary']
        inpt['id'] = args['name'][2:] 
        typ = args['type'].lower()        
        if args['name'] == '--input_file':
          inpt['type'] = 'File'
        elif 'list' not in typ:  
          inpt['type'] = convt_type(typ) +'?'
        else: #if list is in type
          inpt['type'] = convt_type(typ)+'[]?' 
     
        output_writer(args,outputs)

      # inpt = add_secondary_files(args, inpt)
      inputs.append(inpt)
      
      command_line_writer(args,comLine)
      
      
  #    if 'requires' in args['fulltext'] and 'index' in args['fulltext']:
 #       print(args['name'])
#        inpt['secondaryFiles'] = '$(secondary_files(self))'

    cwlf["inputs"] = inputs
    cwlf["outputs"] = outputs
    cwlf["arguments"] = [{"shellQuote": False, 
                          "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.reference_sequence.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  comLine}] 
   


cwlf_generator(jsonf,cwl)
f.write(json.dumps(cwl, indent = 4, sort_keys = False)) #write the file
f.close()


