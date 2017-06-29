import requests
import pprint
import os
import json


#import the json url manually
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
d = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_engine_CommandLineGATK.php.json')

jsonf = {}
jsonf['arguments'] = r.json()['arguments']
#jsonf['arguments'] = r.json()['arguments']+d.json()['arguments']
jsonf['name'] = r.json()['name']


# #########remove this line for actual parser############
# sanger_specific = ['-maxGt', '-maxNumPLValues', '-heterozygosityStandardDeviation', '-maxReadsInMemoryPerSample', '-maxTotalReadsInMemory']
# ########remove above lines #########



fname = jsonf['name']+'.cwl' #set file name
f = open(fname, 'a')

cwl = {}
cwl['id'] = jsonf['name']
cwl["cwlVersion"]= "v1.0"

#commandline = ""

def convt_type(typ):
    if typ == 'double':
        return "float"
    elif typ == 'integer' or typ == 'int':
        return "int"
    elif typ == 'file':
        return "File"
    elif typ in ('string','float','boolean','bool'):
        return typ
    else:
        return "string"


def inputs(item):
    inputs = [{ "doc": "fasta file of reference genome", "type": "File",
                "id": "ref", "secondaryFiles": [".fai","^.dict"]},
              { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
              { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
              { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
                "id": "input_file","secondaryFiles": [".crai","^.dict"]},
              { "doc": "An optional parameter which allows the user to specify additions to the command line at run time",
                "type": "string?", "id": "userString"} ]
    
    for args in jsonf['arguments']:
        inpt = {}
        if args['name'] == '--input_file':
          continue
        elif args['name'] == '--help':
          inpt['doc'] = args['summary']+'\n Name and Synonym modified from help -> gatk_help as it conflicts with cwl-runner argument.'
          inpt['id'] = 'gatk_help'
          typ = args['type'].lower()
        else:
          inpt["doc"] = args['summary']
          inpt["id"] = args['name'][2:]
          typ = args['type'].lower()

        if args['required'] == 'no':
            if 'list' not in typ: 
                inpt["type"] = convt_type(typ) +"?"
            else:
                inpt["type"] = convt_type(typ[5:-1])+"[]?" 

        elif args['required'] == 'yes':
            if 'list' not in typ:
                inpt["type"] = convt_type(typ)
            else:
                inpt["type"] = convt_type(typ[5:-1])
            # if args["defaultValue"] == "NA":
            #   #$(WDLCommandPart('\"-nct\" + NonNull(inputs.nctVal)', ''))

            #   pass
            # else:
            #   #-ActProbThresh $(WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002'))
            #   pass
        inputs.append(inpt)

    item["inputs"] = inputs

def outputs(item):
    item["outputs"] = [{ "outputBinding": { "glob":"$(inputs.out)"},
                         "type": "File",
                         "id": "taskOut" }]

def need_def(arg):
    if 'List' in arg['type']:
        if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
            arg['defaultValue'] = []
        else:
            arg['defaultValue'] = [str(a) for a in arg['defaultValue'][1:-1].split(',')]
    if ('boolean' in arg['type'] or 'List' in arg['type'] or 'false' in arg['defaultValue']):
        return True
    return False

def commandLine(item):
    comLine = ""
    for args in item["arguments"] :
        # #####remove next line#####
        # if args['synonyms'] in sanger_specific:
        #     continue
        # ######remove above lines####
        if need_def(args):
            comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + str(args['defaultValue'])  + "))) "
        else:
            if args['defaultValue'] != "NA" and args['defaultValue']!= "none":
                comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + args['defaultValue'] + "')) "
            else:
                comLine += "$(WDLCommandPart('\"" + args['synonyms'] + "\" + NonNull(inputs." + args['name'].strip("-") + ")', ' ')) " 
        # if need_def(args):
        #     comLine += "  $(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + (str(args['defaultValue']) if args['defaultValue'] != "NA" else "' '"  )  + ")))"
        # else:
        #     comLine += ' ' + args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + (args['defaultValue'] if args['defaultValue'] != "NA" else "' '")  + "'))"
    return comLine

def handleReqs(item):
    item["requirements"] = [{"class": "ShellCommandRequirement"},
                            {
                                           "class": "InlineJavascriptRequirement",
                                           "expressionLib": [
                                                               "function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                                               "function NonNull(x) {if(x === null) {throw new UserException('NullValue');} else {return x;}}",
                                                               "function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');} else if (def =='false') {return '';} else if (def == 'true') {return com;} if (def == []) {return '';} else {return com + ' ' + def;}}"
                                                               ]
                                       },
                                   {
                                                  "dockerPull": "gatk:latest",
                                                  "class": "DockerRequirement"
                                              }
                                 ]
    item["baseCommand"] = []
    item["class"] = "CommandLineTool"
    item["arguments"] = [{"shellQuote": False, "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  commandLine(jsonf)}] 

inputs(cwl)
handleReqs(cwl)
outputs(cwl)

f.write(json.dumps(cwl, indent = 4, sort_keys = False))
f.close()

#print(json.dumps(cwl, indent = 4, sort_keㅑys = False))
