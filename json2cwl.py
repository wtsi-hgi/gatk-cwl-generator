import requests
import pprint

#for now we would be importing the url manually but there should be a way to take inputs and put that url into get
#ie. take in url as a string then r = requests.get(url)
r = requests.get('https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php.json')
doc = r.json()

cwl = {}
cwl['id'] = doc['name']
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




print(doc['name'])
print(cwl)
