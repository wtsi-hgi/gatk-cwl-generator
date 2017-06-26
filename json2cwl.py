import requests
import pprint
import os



#for now we would be importing the url manually but there should be a way to take inputs and put that url into get

#import the json url manually
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
jsonf = r.json()

fname = jsonf['name']+'.cwl' #set file name
fpath = 'c:/home/yejinyou/PY'

filepath = os.path.join(fpath,fname)
if not os.path.exists(fpath):
	os.makedirs(fpath)
f = open(filepath, 'a')

#fi = open("C:\\example.txt","w+")
#print(fi)
#ie. take in url as a string then r = requests.get(url)


g = open("cwl.txt","w+")
cwl = {}
cwl['id'] = jsonf['name']

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




#print(jsonf['name'])
#print(cwl)
