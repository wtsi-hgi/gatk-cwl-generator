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
