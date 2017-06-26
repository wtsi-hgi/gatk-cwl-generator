import requests
import pprint
import os


#import the json url manually
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
jsonf = r.json()

cwl = {}
cwl['id'] = jsonf['name']

commandline = ""

inputs = []

def convt_type(typ):
    if typ == 'double':
        return 'float'
    elif typ == 'integer':
        return 'int'
    elif typ == 'file':
        return 'File'
    elif typ in ('string','float','boolean'):
        return typ
    else:
        return 'string'

for args in jsonf['arguments']:
    inpt = {}
    inpt['doc'] = args['summary']
    inpt['id'] = args['name'][2:]


    if args['required'] == 'no':
        typ = args['type'].lower()  #boolean, integer, double, float, long ...
        if 'list' not in typ: 
            inpt['type'] = convt_type(typ) +'?'
        else:
            inpt['type'] = convt_type(typ[5:-1])+'[]?'

 


    #if type is string, double, boolean, float, integer, long, File ==> then double?, boolean? float? ...

    #if type is list ==. string[]?
    #if type is unidentified ---> string
    #unidentified type of list --> string[]?
    #double -> float
    #check if (String, boolean, Integer, List, 
    #string, float, boolean, File, integer

        #what if type is a list : (if 'List' in args['type']: '[]')
        
        if args['defaultValue'] == 'NA':
            pass
            #commandline function
        else:
            pass
            #commandline function
    inputs.append(inpt)



cwl['inputs'] = inputs
        # {
        #     "type": "float?", 


    #commandline += args['synonyms']+ "VALUE"
    #print(args)

# 'defaultValue': '0.002',
#   'fulltext': '',
#   'kind': 'advanced_param',
#   'maxRecValue': 'NA',
#   'maxValue': '1.0',
#   'minRecValue': 'NA',
#   'minValue': '0.0',

#   'options': [],
#   'required': 'no',
#   'rodTypes': 'NA',
#   'synonyms': '-ActProbThresh',
#   'type': 'Double'},



def commandLine(item):
    comLine = ""
    for args in item['arguments']:
        comLine += "  $(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + (args['defaultValue'] if args['defaultValue'] != "NA" else ' ')  + "')))"
    return comLine

def handleReqs(item):
    item["requirements"] = [{"class": "ShellCommandRequirement"},
                            {
                                           "class": "InLineJavascriptRequirement",
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
    item["arguments"] = [{"shellQuote": "false", "valueFrom": commandLine(jsonf)}]

handleReqs(cwl)

    
#for args in f['arguments']:
    #print(args)
#activeregion
#annotfield
#annotinfo
#arguments
    #default, kind, maxRecValue, macValue, minRecValue, minValue, name, options
    #full text, required, rodTypes, summary, synonyms, type, Double
#description
#downsampling
#group
#name
#parallel
#partitiontype
#readfilters

#--------------------------------------
#cwlversion
#inputs
    #doc, type, id
#requirements
    #class
        #expressionLib
    #dockerPull
#outputs
    #outputBinding
        #glob
    #type
    #id

#basecommand
#class
#arguments
    #shellquote
    #valueFrom
#id

fname = jsonf['name']+'.cwl' #set file name
f = open(fname, 'a')
f.write(str(cwl))
f.close()

#print(jsonf['name'])
#print(cwl)
