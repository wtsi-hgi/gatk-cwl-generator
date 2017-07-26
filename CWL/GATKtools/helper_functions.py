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


def convt_type(typ):
    enumerated_types = ['partition', 'method', 'format', 'writer', 'rule', 'option', 'timeunit', 'type', 'mode', 'validationstringency',
                        'numberallelerestriction', 'implementation', 'platform', 'clippingrepresentation', 'solid_nocall_strategy']

    if 'list[' in typ or 'set[' in typ:
        typ = typ[typ.index('[') + 1:typ.index(']')]
    elif '[]' in typ:
        typ = typ.strip('[]')

    if typ in ('long', 'double', 'int', 'string', 'float', 'boolean', 'bool'):
        return typ
    elif typ == 'file' or 'rodbinding' in typ:  # ROD files
        return 'File'
    elif typ in ('byte', 'integer'):
        return 'int'
    elif any(x in typ for x in enumerated_types):
        return 'string'
    elif 'printstream' in typ:
        return 'null'
    elif typ == 'set':
        return 'string[]'
    else:
        raise ValueError('unsupported type: {}'.format(typ))


def type_writer(args, inpt):
    typ = args['type'].lower()
    if args['name'] == '--input_file':
        args['type'] = 'File'
        inpt['type'] = 'File'
    elif 'intervalbinding' in typ:
        inpt['type'] = ['string[]?', 'File']
    else:
        typ = convt_type(args['type'].lower())
        if 'list' in args['type'].lower() or '[]' in args['type'].lower():
            typ += '[]'
        if args['required'] == 'no':
            typ += '?'
        inpt['type'] = typ


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
