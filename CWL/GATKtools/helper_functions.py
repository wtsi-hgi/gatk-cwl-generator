#!/bin/python



def argument_writer(argument, inputs, outputs, com_line):
    """
    Collection of helper functions for cwl_generator.py and json2cwl.py
    """

    if is_output_argument(argument):
      com_line =  output_commandline_writer(argument,com_line,inputs, outputs)
    else:
      input_writer(argument, inputs)
    return com_line

def input_writer(argument, inputs):
    """
    Modifies the `inputs` parameter with the cwl syntax for expressing a given input argument

    :param argument: The cwl argument, as specified in the json file
    :param inputs: The inputs object, to be written to with the correct information
    """

    cwl_desc = {
        'doc': argument['summary'],
        'id': argument['name'].strip('-'),
    }

    type_writer(argument, cwl_desc)
    if argument['defaultValue'] != "NA": 
      default_helper(cwl_desc,argument)
    secondaryfiles_writer(argument,cwl_desc,inputs)


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
    # ig. -goodSM: name of sample(s) to keep
    elif type_ == 'set':  
        argument['type'] = 'List[string]'
        return 'string'
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
    # type intervalbinding can be a list of strings or a list of files 
    elif 'intervalbinding' in type_:
       argument['type'] = ['List[File]','List[String]'] 
       return ['File','string'] 
    elif type_ == 'rodbinding[variantcontext]' or  type_ == 'rodbinding[feature]' or  \
         type_ == 'rodbinding[bedfeature]' or type_ == 'rodbinding[sampileupfeature]' or  \
         type_ == 'rodbindingcollection[variantcontext]': 
        """
        rodbinding[options]
          variantcontext                         # VCF VCF3 BCF2
          feature                                # BCF2, BEAGLE, BED, BEDTABLE, EXAMPLEBINARY, GELITEXT, RAWHAPMAP, REFSEQ, SAMPILEUP, SAMREAD, TABLE, VCF, VCF3
          BEDfeature                             # BED
          SAMPileupFeature                       # files in SAMPILEUP format
          RodBindingCollection[VariantContext]   # List of files
        """
        argument['type'] = 'string'
        return 'string'

    else:
        raise ValueError('Unable to assign to a CWL type \n Argument: {}   Type: {}'.format(argument['name'][2:],type_))


def typcash(argument, typ, defVal):
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
    else:
        raise ValueError('Failed to cash default value to assigned type. \n Argument: {}    Type: {}   DefaultValue: {}'.format(argument['name'],typ,defVal))






def type_writer(argument, cwl_desc):
    """
    Fills the type in an incomplete cwl description, outputing to cwl_desc

    :param argument: The cwl argument, as specified in the json file
    :param cwl_desc: The inputs object, to be written to with the correct information
    """

    def helper (item_type, prefix):
      type_ = { 
                  "type": "array",
                  "items": item_type,
                  "inputBinding": {
                        "prefix": prefix
                  }
              }
      return type_

    prefix = argument['name'][1:]

    # Patch the incorrect description given by GATK for both --input_file and the type intervalbinding
    if argument['synonyms'] == '-I': 
        argument['type'] = 'File'
        cwl_desc['type'] = 'File'

    else:
        type_ = GATK_to_CWL_type(argument, argument['type'].lower())

        if isinstance(type_, list):
          type_dict = []
          for elm in type_:
            if 'list' in elm.lower():
              type_dict.append(helper(elm,prefix))
            else:
              type_dict.append(elm)
          type_ = type_dict
                
        if 'list' in argument['type'].lower() or '[]' in argument['type'].lower():
            type_ = helper(type_,prefix)      
        else: 
           cwl_desc['inputBinding'] = { 'prefix': argument['name'] }

        if argument['required'] == 'no':
            type_ = ['null', type_]
        cwl_desc['type'] = type_





def default_helper(inpt, argument):
    """
    Sets the default value as in its original type
    """
    typ = inpt['type']
    defVal = argument['defaultValue']

    try:
        if isinstance(typ, list):
            typ = typ[1]
        if isinstance(typ, dict):                      
          if typ['type'] == 'array':
            typ = typ['items'] 
          else:  # if type == 'enum'
            typ = typ['type']
    except:
       raise ValueError('Failed to identify the type of the input argument \n Input argument: {}    Input type: {}'.format( argument['name'], typ ))

    if defVal == '[]':
        inpt['default'] = []
    else:
        if '[]' in typ and typ != '[]':
            typ = typ.strip('[]')
            inpt['default'] = [typcash(argument, typ, val) for val in defVal[1:-1].replace(' ', '').split(',')]
        elif typ == "array":
            inpt['default'] = [typcash(argument,item_type,val) for val in defVal[1:-1].replace(' ', '').split(',')]
        else:
            inpt['default'] = typcash(argument, typ, defVal)




def secondaryfiles_writer(argument, inpt, inputs):
    """
    Sets up file dependencies for certain input files
    """
    if argument['name'] == '--reference_sequence':
        inpt['secondaryFiles'] = ['.fai', '^.dict']
        inputs.insert(0, inpt) # ... trying to get around a bug in CWL ...
    elif 'requires' in argument['fulltext'] and 'files' in argument['fulltext']:
        inpt['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"
        inputs.insert(0, inpt)
    else:
        inputs.append(inpt)




def is_output_argument(argument):
    """
    Returns whether this argument's type indicates it's an output argument
    """
    return any(x in argument["type"].lower() for x in ('printstream', 'writer'))



def output_commandline_writer(argument,com_line,inputs,outputs):
  """
  Modifies the `outputs` parameter with the cwl syntax for expressing a given output argument

  :param argument Object: The cwl argument, as specified in the json file
  :param outputs Object: The outputs object, to be written to with the correct information
  """
  
  prefix = argument['name']
  name = prefix.strip('-')

  if argument['type'] == "GATKSAMFileWriter":
    output_path = '{}.bam'.format(name)
  elif argument['type'] == "PrintStream":
    output_path = '{}.txt'.format(name) 
  elif argument['type'] == 'VariantContextWriter':
    output_path = '{}.vcf'.format(name)
  else:
    print('################################ argument to fix',argument['name'],argument['type'])
    output_path = '{}.txt'.format(name)
                              # when not an required argument, 
  argument['type'] = 'string' # option as an input to specify filepath
 
  if argument['required'] == "no":
    if argument['defaultValue'] == "NA":
      """
      if the argument is not required and doesn't have a default value
      it is an optional input to which file is generated to
      if specified, the outputbinding should be the specified value
      """
      input_writer(argument,inputs)                                                # input
      output_writer(argument,outputs,'$(inputs.{})'.format(name),['null','File'])  # optional outputbinding

    else:
      """
      if the argument is not required but has a default value
      reset the default value to sth that isn't standard output
      it is an optional input to which file is generated to
      if specified, the outputbinding should be the specified value
      else default
      """
      argument['defaultValue'] = output_path                                       # reset default
      input_writer(argument,inputs)                                                # input
      output_writer(argument, outputs,'$(inputs.{})'.format(name),'File')          # always an output

  else: 
    """
    if input is required, remove it as an input
    hardcode the name of the file in and make it as a output
    """
    com_line += '{} {}'.format(prefix,output_path)                                 # hardcode ie. -o output.bam
    output_writer(argument,outputs,output_path,'File')                             # hardcoded name, always an output
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
