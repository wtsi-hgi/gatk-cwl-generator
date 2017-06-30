import requests
import pprint
import os
import json


#import the json url manually
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
d = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_engine_CommandLineGATK.php.json')

jsonf = {}
jsonf['arguments'] = r.json()['arguments']+d.json()['arguments']
jsonf['name'] = r.json()['name']

#create file
fname = jsonf['name']+'.cwl'
f = open(fname, 'a')
cwl = {'id':jsonf['name'],'cwlVersion':'v1.0', 'baseCommand':[], 'class': 'CommandLineTool','outputs':[{ "outputBinding": { "glob":"$(inputs.out)"}, "type": "File", "id": "taskOut" }],
       'requirements':[{ "class": "ShellCommandRequirement"},
                       { "class": "InlineJavascriptRequirement",
                         "expressionLib": [ "function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                            "function NonNull(x) {if(x === null) {throw new UserException('NullValue');} else {return x;}}",
                                            """function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} 
                                            else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');} 
                                            else if (def =='false') {return '';} else if (def == 'true') {return com;} if (def == []) {return '';} else {return com + ' ' + def;}}"""]},
                       { "dockerPull": "gatk:latest","class": "DockerRequirement"}]}

#undefined args, args with invalid default, args with conflicting name
invalid_args = ['--defaultBaseQualities','--heterozygosity_stdev','--max_genotype_count','--max_num_PL_values',
                '--maxReadsInMemoryPerSample','--maxTotalReadsInMemory','--secondsBetweenProgressUpdates','--input_file','--help']

def convt_type(typ):
    if typ == 'double':
        return 'float'
    elif typ in ('integer','int'):
        return 'int'
    elif typ == 'file':
        return 'File'
    elif typ in ('string','float','boolean','bool'):
        return typ
    else:
        return 'string'

def inputs(jsonf,cwlf):
    inputs = [{ "doc": "fasta file of reference genome", "type": "File","id": "ref", "secondaryFiles": [".fai","^.dict"]},
              { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
              { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
              { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File", "id": "input_file","secondaryFiles": [".crai","^.dict"]}] 
             
    for args in jsonf['arguments']:
      inpt = {}
      comLine = ""
      if args['required'] == 'yes' or args['name'] in invalid_args:
        continue

      inpt['doc'] = args['summary']
      inpt['id'] = args['name'][2:] 
      typ = args['type'].lower()        
      if 'list' not in typ: 
        if args['name'] == '--out':
          inpt['type'] = convt_type(typ) ########################
        else:
          inpt['type'] = convt_type(typ) +'?'
      else:
        inpt['type'] = convt_type(typ[5:-1])+'[]?'
      
      if need_def(args):
        comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + str(args['defaultValue'])  + "))) "
      else:
        if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
          comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + args['defaultValue'] + "')) "
        else:
          comLine += "$(WDLCommandPart('\"" + args['synonyms'] + "\" + NonNull(inputs." + args['name'].strip("-") + ")', ' ')) " 

    inputs.append(inpt)
    cwlf["arguments"] = [{"shellQuote": False, "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  comLine}] 
  

    cwlf["inputs"] = inputs

def need_def(arg):
    if 'List' in arg['type']:
        if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
            arg['defaultValue'] = []
        else:
            arg['defaultValue'] = [str(a) for a in arg['defaultValue'][1:-1].split(',')]
    if ('boolean' in arg['type'] or 'List' in arg['type']) or 'false' in arg['defaultValue']:
        return True
    return False

# def commandLine(jsonf,cwlf):
#     # comLine = ""
#     # for args in jsonf["arguments"] :
#     #    if args['required'] == 'yes' or args['name'] in invalid_args: 
#     #       continue
#        if need_def(args):
#           comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + str(args['defaultValue'])  + "))) "
#        else:
#           if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
#             comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + args['defaultValue'] + "')) "
#           else:
#             comLine += "$(WDLCommandPart('\"" + args['synonyms'] + "\" + NonNull(inputs." + args['name'].strip("-") + ")', ' ')) " 
#     cwlf["arguments"] = [{"shellQuote": False, "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  comLine}] 

#inputs(cwl)
inputs(jsonf,cwl)

f.write(json.dumps(cwl, indent = 4, sort_keys = False))
f.close()

