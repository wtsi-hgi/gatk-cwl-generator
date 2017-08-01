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


"""
Gets the correct CWL type for an argument, given an argument's GATK type 

:param argument: The cwl argument, as specified in the json file
:param type: The GATK type given
"""


def GATK_to_CWL_type(argument, type_):
    # Remove list[...], set[...] or ...[] to get the inner type
    if 'list[' in type_ or 'set[' in type_:
        type_ = type_[type_.index('[') + 1:-1]
    elif '[]' in type_:
        type_ = type_.strip('[]')

    if type_ in ('long', 'double', 'int', 'string', 'float', 'boolean', 'bool'):
        return type_
    elif type_ == 'file':
        return 'File'
    elif type_ in ('byte', 'integer'):
        return 'int'
    elif type_ == 'set':  # ig. -goodSM: name of sample(s) to keep
        return 'string[]'
    # Check for enumerated types, and if they exist, ignore the specified type name
    elif argument['options']:
        return {
            'type': 'enum',
            'symbols': [x['name'] for x in argument['options']]
        }
    # Include enum types which are not included in the documentation
    elif type_ == 'validationtype':
        # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.6-0/org_broadinstitute_gatk_tools_walkers_variantutils_ValidateVariants.php
        return {'type': 'enum', 'symbols': ["ALL", "REF", "IDS", "ALLELES", "CHR_COUNTS"]}
    elif type_ == 'contaminationruntype':
        # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.7-0/org_broadinstitute_gatk_tools_walkers_cancer_contamination_ContEst.php#--lane_level_contamination
        # default is set to 'META'
        return {'type': 'enum', 'symbols': ['META', 'SAMPLE', 'READGROUP']}
    elif type_ == 'type':
        return 'string'
    # any combination of those below enumerated types
    #  return {'type':'enum','symbols':['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION']}
    elif type_ == 'partitionType':
        # Example: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php#--partitionType
        # any combination of sample, readgroup and/or library (enum with combinations ?)
        return 'string'
    elif 'intervalbinding' in type_:
        argument['type'] = type_
        return ['null', 'string', 'string[]', 'File']
    else:
        raise ValueError('unsupported type: {}'.format(type_))
####


"""
Fills the type in an incomplete cwl description, outputing to cwl_desc

:param argument: The cwl argument, as specified in the json file
:param cwl_desc: The inputs object, to be written to with the correct information
"""


def type_writer(argument, cwl_desc):
    # Patch the incorrect description given by GATK for both --input_file and the type intervalbinding
    if argument['name'] == '--input_file':
        argument['type'] = 'File'
        cwl_desc['type'] = 'File'
    if 'intervalbinding' in argument["type"].lower():  
        cwl_desc['type'] = ['string[]?', 'File']
    else:
        inner_type = GATK_to_CWL_type(argument, argument['type'].lower())
        if 'list' in argument['type'].lower() or '[]' in argument['type'].lower():
            inner_type += '[]'

        if argument['required'] == 'no':
            inner_type = ['null', inner_type]
        cwl_desc['type'] = inner_type


"""
Modifies the `inputs` parameter with the cwl syntax for expressing a given input argument

:param argument: The cwl argument, as specified in the json file
:param inputs: The inputs object, to be written to with the correct information
"""


def input_writer(argument, inputs):
    cwl_desc = {
        'doc': argument['summary'],
        'id': argument['name'].strip('-'),
        'inputBinding': {
            'prefix': argument['name'][1:]
        }
    }

    type_writer(argument, cwl_desc)
    if argument['defaultValue'] != "NA": 
      default_helper(cwl_desc,argument)
    secondaryfiles_writer(argument,cwl_desc,inputs)

def argument_writer(argument, inputs, outputs):
    if is_output_argument(argument):
#        print(argument)
        output_writer(argument, outputs)
    else:
        input_writer(argument, inputs)


def typcash(args, typ, defVal):
    if typ == 'int':
        return int(defVal)
    elif typ == 'boolean':
        return bool(defVal)
    elif typ == 'string':
        return defVal
    elif typ == 'enum':
        return defVal
    elif typ == 'long':
        return long(defVal)
    elif typ == 'double':
        return float(defVal)
    elif defVal == '[]':
        return []
    else:
        raise Exception('failed to cash type {}'.format(typ))


def default_helper(inpt, args):
    typ = inpt['type']
    defVal = args['defaultValue'].encode()
    try:
        if isinstance(typ, list):
            typ = typ[1]
        if isinstance(typ, dict):
            typ = typ['type']
    except:
        raise Exception('Unverified type {}'.format(typ))

    if '[]' in typ and typ != '[]':
        typ = typ.strip('[]')
        if defVal == '[]':
            inpt['default'] = []
        else:
            inpt['default'] = [typcash(args, typ, val)
                               for val in defVal[1:-1].replace(' ', '').split(',')]
    else:
        inpt['default'] = typcash(args, typ, defVal)


def secondaryfiles_writer(args, inpt, inputs):
    if args['name'] == '--reference_sequence':
        inpt['secondaryFiles'] = ['.fai', '^.dict']
        inputs.insert(0, inpt)
    elif 'requires' in args['fulltext'] and 'files' in args['fulltext']:
        inpt['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"
        inputs.insert(0, inpt)
    else:
        inputs.append(inpt)


"""
Returns whether this argument's type indicates it's an output argument
"""


def is_output_argument(argument):
    return any(x in argument["type"].lower() for x in ('rodbinding', 'printstream', 'writer'))


"""
Modifies the `outputs` parameter with the cwl syntax for expressing a given output argument

:param argument Object: The cwl argument, as specified in the json file
:param outputs Object: The outputs object, to be written to with the correct information
"""


def output_writer(argument, outputs):
    outpt = {
        'id': argument['name'],
        'type': ['null', 'File'],
        'outputBinding': {
            'glob': '$(inputs.' + argument['name'].strip('-') + ')'
        }
    }

    outputs.append(outpt)
