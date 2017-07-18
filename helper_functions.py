"""
List of helper functions for json2cwl.py
"""

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

def convt_type(typ):
  if 'list' in typ:
    typ = typ[5:-1]
  if typ in ('long','double','int','string','float','boolean','bool'):
    return typ
  elif typ == 'file':
    return 'File'
  elif typ in ('byte','integer'):
    return 'int'
  elif 'rodbinding' in typ: #ROD files
    return 'File'
  elif any (x in typ for x in ('writer','rule','option','timeunit','type','mode','validationstringency')):
    return 'string'
  elif 'printstream' in typ: #meant for debugging
    return 'null'
  else:
    raise ValueError('unsupported type: {}'.format(typ))

def type_writer(args,inpt):
  typ = args['type'].lower()             
  if args['name'] == '--input_file': ##################################
    inpt['type'] = 'File'
  elif 'intervalbinding' in typ: ##################################
    inpt['type'] =  ["string[]?", "File?"]

  else:
    typ = convt_type(args['type'].lower())
    if 'list' in args['type'].lower():             #List[interval binding]
      typ = typ + '[]'
    if args['required'] == 'no':
      typ = typ +'?'
    inpt['type'] = typ

  # typ = args['type'].lower()        
    # if args['name'] == '--input_file':
    #   inpt['type'] = 'File'
    # elif 'list' not in typ:  
    #   inpt['type'] = convt_type(typ) +'?'
    # else: #if list is in type
    #   inpt['type'] = convt_type(typ)+'[]?'


# ################################################################################################################################
# #interval, filewriter 
# # ################################################################################################################################
# def convt_type(typ):
#   #  typ = args['type'].lower()
#  #   if 'list' in typ:
# #       typ = typ[5:-1]
#     if typ in ('integer','byte'):
#         return 'int'
# #    elif typ == 'intervalbinding[feature]':
# #        pass        
#     elif typ == 'file':
#         return 'File'
#     elif typ in ('long','double','int','string','float','boolean','bool'):
#         return typ
#     elif 'rodbinding' in typ: #ROD file, File to which output should be written
#         return 'File'
#     #file writer: take in as an input string
#     elif 'writer' in typ or 'rule' in typ or 'option' in typ or 'timeunit' in typ or 'type' in typ or 'mode' in typ or 'validationstringency' in typ: #minutes pedigreevalidationtype, gatkvcfindextype, downsampletype ...
#         return 'string'
#     elif 'printstream' in typ:
#         return 'null'
#     else:
# #        print('typeerror',typ)   
#         return 'string'
#         #temporary measurement`
#         #raise ValueError("unsupported type %s" %(typ)) 


def output_writer(args,outputs):
  if 'writer' in args['type'].lower():
    outpt = {'id': args['name'], 'type': ['null','File'], 'outputBinding':{'glob':'$(inputs.'+args['name'][2:]+')'}}
    outputs.append(outpt)


def commandline_writer(args,comLine):
  if need_def(args):
      comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', " + str(args['defaultValue'])  + "))) "
  else:
      if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
         comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', '" + args['defaultValue'] + "')) "
      elif args['synonyms'] == '-o':
         comLine += "$(defHandler('" + args['synonyms'] + "', WDLCommandPart('NonNull(inputs." + args['name'].strip("-") + ")', "+"'stdout'"+"))) "
      else:
         comLine += "$(WDLCommandPart('\"" + args['synonyms'] + "\" + NonNull(inputs." + args['name'].strip("-") + ")', ' ')) " 
