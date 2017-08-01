#!/bin/python

"""
Collection of helper functions for cwl_generator.py and json2cwl.py
"""


def need_def(arg):
    if 'List' in arg['type']:
        if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
            arg['defaultValue'] = []
        else:
            arg['defaultValue'] = [
                str(a) for a in arg['defaultValue'][1:-1].split(',')]

    if arg['defaultValue'] == '[]' or arg['defaultValue'] == 'NA':
        return False
    if ('boolean' in arg['type'] or 'List' in arg['type']) or 'false' in arg['defaultValue']:
        return True
    return False



def convt_type(args,typ):
  if 'list[' in typ or 'set[' in typ:
    typ = typ[typ.index('[')+1:-1]
  elif '[]' in typ:
    typ = typ.strip('[]')

  
  if typ in ('long','double','int','string','float','boolean','bool'):
    return typ
  elif typ == 'file': 
    return 'File'
  elif typ in ('byte','integer'):
    return 'int'
  elif typ == 'set': #ig. -goodSM: name of sample(s) to keep
    return 'string[]'
  elif args['options']: #check for enumerated types
    return {'type': 'enum','symbols':[x['name'] for x in args['options']]}

  #output collecters / filewriters
  elif any (x in typ for x in ('rodbinding','printstream','writer')):
    return 'string'
 
#############################################################################################################################################################################################
  elif typ == 'validationtype':
  #https://software.broadinstitute.org/gatk/gatkdocs/3.6-0/org_broadinstitute_gatk_tools_walkers_variantutils_ValidateVariants.php
    return 'string' 
 
  elif typ == 'contaminationruntype':
  #https://software.broadinstitute.org/gatk/gatkdocs/3.7-0/org_broadinstitute_gatk_tools_walkers_cancer_contamination_ContEst.php#--lane_level_contamination
   return {'type':'enum','symbols':['META','SAMPLE','READGROUP']} #default is set to 'META'
  #  return 'string'
  elif typ == 'type':
    return 'string'
  # any combination of those below enumerated types
  #  return {'type':'enum','symbols':['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION']}
  elif typ == 'partition':
  #https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php#--partitionType
    return 'string' #any combination of sample, readgroup and/or library (enum with combinations ?)
 


  elif 'intervalbinding' in typ:
    args['type'] = typ
    return ['null','string','string[]','File']
  else:
     print 'unsupported type:',typ
#    raise ValueError('unsupported type: {}'.format(typ))
##############################################################################################################################################################################################









def type_writer(args,inpt):
  typ = args['type'].lower()             
  if args['name'] == '--input_file':
    args['type'] = 'File'
    inpt['type'] = 'File' 
  if 'intervalbinding' in typ:
    inpt['type'] = ['string[]?','File']
  else: 
    typ = convt_type(args,args['type'].lower())
    if 'list' in args['type'].lower() or '[]' in args['type'].lower():
     typ += '[]'
    if args['required'] == 'no':
      typ = ['null',typ]
    inpt['type'] = typ


def input_writer(args,inputs):
  inpt = {'doc':args['summary'],'id':args['name'].strip('-'),'inputBinding':{'prefix':args['name']}}
  type_writer(args,inpt) 
  if args['defaultValue'] != "NA": 
    default_helper(inpt,args)
  secondaryfiles_writer(args,inpt,inputs)


def typcash(args,typ,defVal):
   if typ  == 'int':
     return int(defVal)
   elif typ == 'boolean':
     return bool(defVal)
   elif typ == 'string':
     return defVal
   elif typ == 'enum':
     return defVal
   elif typ == 'long':
     return  long(defVal)
   elif typ == 'double':
     return float(defVal)
   elif defVal == '[]' :
     return []
   else: 
     raise Exception('failed to cash type {}'.format(typ))

def default_helper(inpt, args):
  typ = inpt['type'] 
  defVal = args['defaultValue'].encode() 
  try:
   if isinstance(typ,list):
     typ = typ[1] 
   if isinstance(typ,dict):
     typ = typ['type'] 
  except: 
   raise Exception('Unverified type {}'.format(typ)) 
  
  if '[]' in typ and typ != '[]':
    typ = typ.strip('[]')
    if defVal == '[]':
      inpt['default'] = []
    else: 
      inpt['default'] = [typcash(args,typ,val) for val in defVal[1:-1].replace(' ','').split(',')]
  else:
    inpt['default'] = typcash(args,typ,defVal)
  

def secondaryfiles_writer (args,inpt,inputs):
  if args['name'] == '--reference_sequence':
    inpt['secondaryFiles'] = ['.fai','^.dict']
    inputs.insert(0,inpt)
  elif 'requires' in args['fulltext'] and 'files' in args['fulltext']:
    inpt['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"  
    inputs.insert(0,inpt)
  else:
    inputs.append(inpt)


def output_writer(args,outputs):
  if 'writer' in args['type'].lower():
    outpt = {'id': args['name'], 'type': ['null','File'], 'outputBinding':{'glob':'$(inputs.'+args['name'].strip('-')+')'}}
    outputs.append(outpt)

