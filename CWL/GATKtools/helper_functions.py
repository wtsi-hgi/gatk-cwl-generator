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








#############################WORKIING ON THIS  ############################# 

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
#  print ('seraihtsio')
  inpt = {'doc':args['summary'],'id':args['name'].strip('-'),'inputBinding':{'prefix':args['name'][1:]}}
  type_writer(args,inpt) #CWL type of the input
  #if args['defaultValue'] != "NA": #if it has a default value
  print(args['name'],args['defaultValue'])
  default_helper(inpt,args)
    #inpt['default'] = args['defaultValue']
  secondaryfiles_writer(args,inpt,inputs)

# DON'T TOUCH

def typcash(args,typ,defVal):
   print('in typcahs')
   if typ  == 'int':
     return int(defVal)
   elif typ == 'boolean':
     return bool(defVal)
   elif typ == 'string':
     return defVal
   elif typ == 'long':
     return  long(defVal)
   elif typ == 'double':
     return float(defVal)
   elif defVal == '[]':
     return []
   #remaining types are File, enum, dictionary of enum
   else:
     print('#####################name: ',args['name'],'type to convert to : ',typ,'default value: ',args['defaultValue'])
  # else:
  #   try:
  #     if typ['type'] == 'enum':
  #       return defVal
  #   except:
  #     print('unrecognized type error',typ,defVal)


def default_helper(inpt, args):
  typ = inpt['type'] #CWL type that has been inserted
  defVal = args['defaultValue'].encode() #default Value in string

 # try:
  if not isinstance(typ,list): #if the type is not a list = 'string','bool'
    typ = typ.encode() #convert to string from unicode
  else: # if it is a list ['null', type]
    typ = typ[1]  #not null, could be a type or a dictionary again
  print(typ)
  inpt['default'] = typcash(args,typ,defVal)
  
#       else:
#         typ = typ[1]['type']
#   except:
#     print('the type of the input is:',inpt['type'],args['defaultValue'])

  # print(typ,defVal)
   #try:
   #  to =  inpt['type'][1].encode()
   #except:
   #  to = inpt['type'].encode()
   #inpt['default'] = to(args['defaultValue'].encode())

#   if '[]' in typ and typ != '[]':
     #print(inpt['id'],inpt['type'])
#     typ = typ.strip('[]')
#     l = []
#     for elm in args['defaultValue']:
#       l.append(typcash(args,typ,elm))
       #print(l)
#       inpt['default'] = l
#   else:
  

#############################WORKIING ON THIS  ############################# 
















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

#def commandline_writer(args,comLine):
#  comLine += "$(commandLine_Handler('{}','{}','{}','{}'))".format(args['name'][1:],args['required'],args['defaultValue'],'inputs.'+args['name'].strip('-'))
#  return comLine
"""
def input_writer(args, inputs):
    inpt = {'doc': args['summary'], 'id': args['name'][2:]}
    type_writer(args, inpt)
    secondaryfiles_writer(args, inpt, inputs)


def secondaryfiles_writer(args, inpt, inputs):
    if args['name'] == '--reference_sequence':
        inpt['secondaryFiles'] = ['.fai', '^.dict']
        inputs.insert(0, inpt)
    elif 'requires' in args['fulltext'] and 'files' in args['fulltext']:
        inpt['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"
        inputs.insert(0, inpt)
    else:
        inputs.append(inpt)


def output_writer(args, outputs):
    if 'writer' in args['type'].lower():
        outpt = {'id': args['name'], 'type': ['null', 'File'], 'outputBinding': {
            'glob': '$(inputs.' + args['name'][2:] + ')'}}
        outputs.append(outpt)


def commandline_writer(args, comLine):
    p = args['synonyms']
    argument = args['name'].strip('-')
    default = args['defaultValue']
    if 'file' in args['type'].lower():
        argument += '.path'
    if args['name'] in ('--reference_sequence', '--input_file'):
        comLine += p + \
            " $(WDLCommandPart('NonNull(inputs." + argument + ")', '')) "
    elif args['required'] == 'yes':
        comLine += p + " $(inputs." + argument + ")"
    elif need_def(args):
        comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + \
            args['name'].strip("-") + ")', " + \
            str(args['defaultValue']) + "))) "
    else:
        if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
            comLine += args['synonyms'] + \
                " $(WDLCommandPart('NonNull(inputs." + argument + \
                ")', '" + args['defaultValue'] + "')) "
        elif args['synonyms'] == '-o':
            comLine += "$(defHandler('" + p + "', WDLCommandPart('NonNull(inputs." + \
                argument + ")', " + "'stdout'" + "))) "
        else:
            comLine += "$(WDLCommandPart('" + p + \
                "  NonNull(inputs." + argument + ")', ' ')) "
    return comLine

"""
