#!/bin/python

"""
Collection of helper functions for cwl_generator.py and json2cwl.py
"""

# You cannot get the enumeration information for an enumeration in a nested type, so they are hard coded here
enum_types = {
    # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.6-0/org_broadinstitute_gatk_tools_walkers_variantutils_ValidateVariants.php
    "validationtype": ["ALL", "REF", "IDS", "ALLELES", "CHR_COUNTS"],
    # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.7-0/org_broadinstitute_gatk_tools_walkers_cancer_contamination_ContEst.php#--lane_level_contamination
    "contaminationruntype": ['META', 'SAMPLE', 'READGROUP'], # default is META
    # Example: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php#--partitionType
    "partition": ["readgroup", "sample", "library", "platform", "center",
        "sample_by_platform", "sample_by_center", "sample_by_platform_by_center"],
    "type": ['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION']
}

def GATK_to_CWL_type(argument, type_):
    """
    Gets the correct CWL type for an argument, given an argument's GATK type 

    :param argument: The cwl argument, as specified in the json file
    :param type: The GATK type given
    """
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
    elif type_ in enum_types.keys():
        return {
            "type": "enum",
            "symbols": enum_types[type_]
        }
    #elif 'intervalbinding' in type_: 
    #    argument['type'] = type_ # TODO: look into this
    #    return ['null', 'string', 'string[]', 'File']

    elif type_ == 'rodbinding[variantcontext]' or  type_ == 'rodbinding[feature]' \
     or  type_ == 'rodbinding[bedfeature]' or type_ == 'rodbinding[sampileupfeature]' \
     or  type_ == 'rodbindingcollection[variantcontext]': 
        """
         rodbinding
          variantcontext                       # VCF VCF3 BCF2
          feature                              # BCF2, BEAGLE, BED, BEDTABLE, EXAMPLEBINARY, GELITEXT, RAWHAPMAP, REFSEQ, SAMPILEUP, SAMREAD, TABLE, VCF, VCF3
          BEDfeature                           # BED
          SAMPileupFeature                     # files in SAMPILEUP format
          RodBindingCollection[VariantContext] # List of files
        """
        argument['type'] = 'string'
        return 'string'

    else:
#         return 'string'
        raise ValueError('unsupported type: {}'.format(type_))


"""
Fills the type in an incomplete cwl description, outputing to cwl_desc

:param argument: The cwl argument, as specified in the json file
:param cwl_desc: The inputs object, to be written to with the correct information
"""


def type_writer(argument, cwl_desc, prefix):
    # Patch the incorrect description given by GATK for both --input_file and the type intervalbinding
    if argument['synonyms'] == '-I': 
        argument['type'] = 'File'
        cwl_desc['type'] = 'File'
    elif 'intervalbinding' in argument['type'].lower():
        cwl_desc['type'] = ['null','string','string[]','File'] # TODO: this line
    else:
        type_ = GATK_to_CWL_type(argument, argument['type'].lower())
        
        if 'list' in argument['type'].lower() or '[]' in argument['type'].lower():
            type_ = {
                "type": "array",
                "items": type_,
                "inputBinding": {
                    "prefix": prefix
                }
            }

        if argument['required'] == 'no':
            type_ = ['null', type_]
        cwl_desc['type'] = type_


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
            'prefix': argument['name']
        }
    }

    type_writer(argument, cwl_desc)
    if argument['defaultValue'] != "NA": 
      default_helper(cwl_desc,argument)
    secondaryfiles_writer(argument,cwl_desc,inputs)

def argument_writer(argument, inputs, outputs, com_line):
    if is_output_argument(argument):
      com_line =  output_commandline_writer(argument,com_line,inputs, outputs)
    else:
      input_writer(argument, inputs)
    return com_line

def typcash(args, typ, defVal):
    if defVal == '[]':
        return []
    elif typ == 'int':
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
    else:
        raise Exception('failed to cash argument: {}   unable to cash type: {}'.format(args['name'],typ))

def default_helper(inpt, args):
    typ = inpt['type']
    defVal = args['defaultValue'].encode()
    try:
        if isinstance(typ, list):
            typ = typ[1]
        if isinstance(typ, dict):                      
          if typ['type'] == 'array':
            typ = typ['items'] 
          else: 
            typ = typ['type']
    except:
       raise Exception('Argument: {}   Unrecognized type: {}'.format(args['name'],typ))

    if '[]' in typ and typ != '[]':
        typ = typ.strip('[]')
        if defVal == '[]':
            inpt['default'] = []
        else:
            inpt['default'] = [typcash(args, typ, val)
                               for val in defVal[1:-1].replace(' ', '').split(',')]
    elif typ == "array":
        inpt['default'] = [typcash(args,item_type,val) for val in defVal[1:-1].replace(' ', '').split(',')]
    else:
        inpt['default'] = typcash(args, typ, defVal)


def secondaryfiles_writer(args, inpt, inputs):
    if args['name'] == '--reference_sequence':
        inpt['secondaryFiles'] = ['.fai', '^.dict']
        inputs.insert(0, inpt) # ... trying to get around a bug in CWL ...
    elif 'requires' in args['fulltext'] and 'files' in args['fulltext']:
        inpt['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"
        inputs.insert(0, inpt)
    else:
        inputs.append(inpt)


"""
Returns whether this argument's type indicates it's an output argument
"""


def is_output_argument(argument):
    return any(x in argument["type"].lower() for x in ('printstream', 'writer'))


"""
Modifies the `outputs` parameter with the cwl syntax for expressing a given output argument

:param argument Object: The cwl argument, as specified in the json file
:param outputs Object: The outputs object, to be written to with the correct information
"""

def output_commandline_writer(argument,com_line,inputs,outputs):
  
  prefix = argument['name']

  name = prefix.strip('-')

  if argument['type'] == "GATKSAMFileWriter":
    output_path = '{}.bam'.format(name)
  elif argument['type'] == "PrintStream":
    output_path = '{}.txt'.format(name) 
  elif argument['type'] == 'VariantContextWriter':
    output_path = '{}.vcf'.format(name)
  else:
    print('################################3argument to fix',argument['name'],argument['type'])
    output_path = '{}.txt'.format(name)
                              # when not an required argument, 
  argument['type'] = 'string' # option as an input so to specify path_to_file 
 
  if argument['required'] == "no":
    if argument['defaultValue'] == "NA":
      """
      if the argument is not required and doesn't have a default value
      it is an optional input to which file is generated to
      if specified, the outputbinding should be the specified value
      """
      input_writer(argument,inputs)                                               # input
      output_writer(argument,outputs,'$(inputs.{})'.format(name),['null','File'])  # optional outputbinding

    else:
      """
      if the argument is not required but has a default value
      reset the default value to sth that isn't standard output
      it is an optional input to which file is generated to
      if specified, the outputbinding should be the specified value
      else default
      """
      argument['defaultValue'] = output_path                                      # reset default
      input_writer(argument,inputs)                                               # input
      output_writer(argument, outputs,'$(inputs.{})'.format(name),'File')          # always an output

  else: #if input required, get rid of the requirement 
    """
    if input is required, remove it as an input
    hardcode the name of the file in and make it as a output
    """
    com_line += '{} {}'.format(prefix,output_path)                               # hardcode ie. -o output.bam
    output_writer(argument,outputs,output_path,'File')                           # hardcoded name, always an output
  return com_line

def output_writer(argument, outputs, globval, type_):
    outpt = {
        'id': argument['name'],
        'type': type_,
        'outputBinding': {
            'glob': globval
        }
    }

    outputs.append(outpt)
