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
  if typ in ('long','double','int','integer','string','float','boolean','bool','file'):
    return typ
  elif typ == 'byte':
    return 'int'
  elif 'rodbinding' in typ: #ROD files
    return 'file'
  elif any (x in typ for x in ('writer','rule','option','timeunit','type','mode','validationstringency')):
    return 'string'
  elif 'printstream' in typ: #meant for debugging
    return 'null'
  else:
    raise ValueError('unsupported type: {}'.format(typ))


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
