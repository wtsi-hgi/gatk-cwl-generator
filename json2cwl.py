import requests
import pprint
import os
import json


#import the json url manually
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
jsonf = r.json()

cwl = {}
cwl['id'] = jsonf['name']
cwl["cwlVersion"]= "v1.0"

commandline = ""


def convt_type(typ):
    if typ == 'double':
        return "float"
    elif typ == 'integer':
        return "int"
    elif typ == 'file':
        return "File"
    elif typ in ('string','float','boolean'):
        return typ
    else:
        return "string"

def inputs(item):
    inputs = [{ "doc": "fasta file of reference genome", "type": "File",
                "id": "ref", "secondaryFiles": [".fai","^.dict"]},
              { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
              { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
              { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
                "id": "input_file","secondaryFiles": [".crai"]}]
    
    for args in jsonf['arguments']:
        inpt = {}
        inpt["doc"] = args['summary']
        inpt["id"] = args['name'][2:]

        if args['required'] == 'no':
            typ = args['type'].lower()  #boolean, integer, double, float, long ...
            if 'list' not in typ: 
                inpt["type"] = convt_type(typ) +"?"
            else:
                inpt["type"] = convt_type(typ[5:-1])+"[]?"  
        inputs.append(inpt)

    item["inputs"] = inputs

def outputs(item):
    item["outputs"] = [{ "outputBinding": { "glob":"$(inputs.out)"},
                         "type": "File",
                         "id": "taskOut" }]

def commandLine(item):
    comLine = ""
    for args in item["arguments"]:
        comLine += "  $(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + (args['defaultValue'] if args['defaultValue'] != "NA" else ' ')  + "')))"
    return comLine

def handleReqs(item):
    item["requirements"] = [{"class": "ShellCommandRequirement"},
                            {
                                           "class": "InlineJavascriptRequirement",
                                           "expressionLib": [
                                                               "function WDLCommandPart(expr, def) {var rval; try {rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                                                               "function NonNull(x) {if(x === null) {throw new UserException(\"NullValue\");} else {return x;}}",
                                                               "function defHandler(com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0 ) {return def.map(elementh=> com+ ' ' + element).join(' ');} else if (def == \"false\" {return "";} else if (def == \"true\" (r\
eturn com;} if (def == []) {return "";} else {return com + def;}}"
                                                               ]
                                       },
                                   {
                                                  "dockerPull": "gatk:latest",
                                                  "class": "DockerRequirement"
                                              }
                                 ]
    item["baseCommand"] = []
    item["class"] = "CommandLineTool"
    item["arguments"] = [{"shellQuote": False, "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', ''))" +  commandLine(jsonf)}]

inputs(cwl)
handleReqs(cwl)
outputs(cwl)

fname = jsonf['name']+'.cwl' #set file name
f = open(fname, 'a')
f.write(json.dumps(cwl, indent = 4, sort_keys = False))
f.close()

print(json.dumps(cwl, indent = 4, sort_keys = False))

