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
  elif typ == 'file' or 'rodbinding' in typ: #ROD files
    return 'File'
  elif typ in ('byte','integer'):
    return 'int'
  elif any (x in typ for x in ('writer','rule','option','timeunit','type','mode','validationstringency')):
    return 'string'
  elif 'printstream' in typ: 
    return 'null'
  else:
    raise ValueError('unsupported type: {}'.format(typ))

def type_writer(args,inpt):
  typ = args['type'].lower()             
  if args['name'] == '--input_file':
    inpt['type'] = 'File' 
  elif 'intervalbinding' in typ:
    inpt['type'] = ['string[]?','File']
  else:
    typ = convt_type(args['type'].lower())
    if 'list' in args['type'].lower():
      typ += '[]'
    if args['required'] == 'no':
      typ += '?'
    inpt['type'] = typ

"""

def secondaryfiles_writer ()
"""

#def get_file_type(f):

#$("."+(inputs.input_file).split('.')[1].replace("m","i"))


##  $("."+(inputs.input_file).split('.')[1].replace("m","i"))


# function secondary_files(f) {
#   if (f.includes('.cram') ){ return '.crai';} else if (f.includes('.bam')) { return '.bai'; } else if (f.includes('.fa')) { return ['.fai','^.dict']; }
#     }

  # secondaryfiles = []
  # if 'dictionary' in args['fulltext']:
  #   secondaryfiles += '^.dict'
  # if 'index' in args['fulltext']:
  #   secondaryfiles += "$('.'+(inputs." + args['name'] + ").split('.')[1].replace('m','i'))"
# def add_secondary_files(args, inpt): #return secondary file in [ '.crai'] formet
#   if 'required' not in args['fulltext']:
#     pass
#   else:
#     if 'dictionary' in args['fulltext']:
#       secondaryfiles = ['^.dict','^fai']
#     elif 'index' in args['fulltext']: #CRAM / BAM for input_files
#       print('requires and index: only input should have this', args['name'])
#       secondaryfiles = ["$('.'+(inputs." + args['name'] + ").split('.')[1].replace('m','i'))"]

      
      # "$('.'+(inputs." + args['id'] + ").split('.')[1].replace('m','i'))""

def output_writer(args,outputs):
  if 'writer' in args['type'].lower():
    outpt = {'id': args['name'], 'type': ['null','File'], 'outputBinding':{'glob':'$(inputs.'+args['name'][2:]+')'}}
    outputs.append(outpt)


def commandline_writer(args,comLine):
  p = args['synonyms']
  argument = args['name'].strip('-')
  default = args['defaultValue']



  if 'file' in args['type'].lower():
    argument += '.path'
    #print(argument)

  if args['name'] == '--reference_sequence':
    comLine += p  + " $(WDLCommandPart('NonNull(inputs."+ argument + ")', '')) "
  elif args['required'] == 'yes':
    comLine += "{} $(inputs.{})".format(p,argument)
  elif need_def(args):
    #comLine += "$(defHandler('{}', WDLCommandPart('NonNull(inputs.{})', {}))) ".format(p,argument,str(default))
    comLine += "$(defHandler('{}', WDLCommandPart('NonNull(inputs.{})', {}))) ".format(p,argument,str(default))
  else:
      if args['defaultValue'] != "NA" and args['defaultValue'] != "none":
         comLine += "{} $(WDLCommandPart('NonNull(inputs.{})', '{}')) ".format(p,argument,default)
         #comLine += args['synonyms'] + " $(WDLCommandPart('NonNull(inputs." + argument  + ")', '" + args['defaultValue'] + "')) "
      elif args['synonyms'] == '-o':
         comLine += "$(defHandler('{}', WDLCommandPart('NonNull(inputs.{})', "+"'stdout'"+"))) ".format(p,argument)
         #comLine += "$(defHandler('" + p + "', WDLCommandPart('NonNull(inputs." + argument + ")', "+"'stdout'"+"))) "
      else:

        #comLine += "$(WDLCommandPart('" + p  + "  NonNull(inputs." + argument + ")', ' ')) " 
        comLine += "$(WDLCommandPart('{}  NonNull(inputs.{})', ' ')) ".format(p,argument)
  return comLine 


