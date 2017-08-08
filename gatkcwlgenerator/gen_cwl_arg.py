"""
Functions to generate the CWL descriptions for GATK arguments.

The main exported functions are get_output_json and get_input_json
"""


def get_input_bindings(argument, is_file_type):
    input_binding = {
        "prefix": argument["name"]
    }

    if is_file_type:
        input_binding["valueFrom"] = "$(parseTags(self.path, inputs.{}_tags))".format(get_arg_id(argument))
        input_binding["shellQuote"] = False
        input_binding["separate"] = False
    
    return input_binding

def get_arg_id(argument):
    return argument["name"].strip("-")

def get_input_json(argument, options):
    """
    Returns the cwl syntax for expressing the given argument

    :param argument: The cwl argument, as specified in the json file
    :param inputs: The inputs object, to be written to with the correct information

    :returns: CWL object to describe the given argument
    """

    cwl_desc = {
        'doc': argument['summary'],
        'id': get_arg_id(argument),
    }

    prefix = argument['name']
    # Patch the incorrect description given by GATK for both --input_file
    if prefix == '--input_file' or prefix == '--input':
        argument['type'] = 'File'

    cwl_type, is_array_type = get_CWL_type(argument)
    if not is_array_type:
        cwl_desc["inputBinding"] = get_input_bindings(argument, cwl_type == "File")

    cwl_desc["type"] = cwl_type

    if is_arg_with_default(argument, options) and is_output_argument(argument):
        cwl_desc["default"] = get_output_default_arg(argument, cwl_type)

    if argument['name'] == '--reference_sequence':
        cwl_desc['secondaryFiles'] = ['.fai', '^.dict']
    elif 'requires' in argument['fulltext'] and 'files' in argument['fulltext']:
        cwl_desc['secondaryFiles'] = "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"

    return cwl_desc


def is_arg_with_default(argument, cmd_line_options):
    return  argument['defaultValue'] != "NA" \
        and argument['defaultValue'].lower() != "none"

# You cannot get the enumeration information for an enumeration in a nested type, so they are hard coded here
enum_types = {
    # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.6-0/org_broadinstitute_gatk_tools_walkers_variantutils_ValidateVariants.php
    "validationtype": ["ALL", "REF", "IDS", "ALLELES", "CHR_COUNTS"],
    # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.7-0/org_broadinstitute_gatk_tools_walkers_cancer_contamination_ContEst.php#--lane_level_contamination
    "contaminationruntype": ['META', 'SAMPLE', 'READGROUP'],  # default is META
    # Example: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php#--partitionType
    "partition": ["readgroup", "sample", "library", "platform", "center",
                  "sample_by_platform", "sample_by_center", "sample_by_platform_by_center"],
    "type": ['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION']
}

warning_colour = '\033[93m'


def basic_GATK_type_to_CWL(argument, typ):
    """
    Gets the correct CWL type for an argument, given an argument's GATK type excluding List[...]

    typ may not be the same as the arguments type if you are overriding the type

    :param argument: The cwl argument, as specified in the json file
    :param typ: The GATK type given

    :returns: (cwl_type, is_array_type)
    """

    is_array_type = False

    if typ in ('long', 'double', 'int', 'string', 'float', 'boolean', 'bool'):
        cwl_type = typ
    elif typ == 'file':
        cwl_type = 'File'
    elif is_output_argument(argument):
        cwl_type = "string"
    elif typ in ('byte', 'integer'):
        cwl_type = 'int'
    elif typ == 'set':
        # The caller function will turn this into an array of sets
        # Example of this -goodSM
        is_array_type = True
        cwl_type = 'string'
    elif argument['options']:
        # Check for enumerated types, and if they exist, ignore the specified type name
        cwl_type = {
            'type': 'enum',
            'symbols': [x['name'] for x in argument['options']]
        }
    elif typ in enum_types.keys():
        cwl_type = {
            "type": "enum",
            "symbols": enum_types[typ]
        }
    elif 'intervalbinding' in typ:
        # Type intervalbinding can be a list of strings or a list of files
        is_array_type = True
        cwl_type = ['File', "string"]
    elif "rodbinding" in typ:
         # Possible options: https://gist.github.com/ThomasHickman/b4a0552231f4963520927812ad29eac8
        cwl_type = 'File'
    else:
        print(warning_colour + 'WARNING: Unable to assign to a CWL type, defaulting to string\n'
            + warning_colour + 'Argument: {}   Type: {}'.format(
            argument['name'][2:], typ))
        
        cwl_type = "string"

    return (cwl_type, is_array_type)


def get_CWL_type(argument):
    """
    Returns the CWL type of an argument, indicating if it is an array type

    :param argument: The cwl argument, as specified in the json file
    :param cwl_desc: The inputs object, to be written to with the correct information

    :returns: (type_json, is_array_type)
    If is_array_type is true, the caller shouldn't output inputBinding's prefix
    """

    is_array_type = False

    prefix = argument['name']
    # Patch the incorrect description given by GATK for both --input_file and the type intervalbinding
    if prefix == '--input_file' or prefix == '--input':
        typ = 'File'
    else:
        outer_type = argument['type'].lower()

        if 'list[' in outer_type or 'set[' in outer_type:
            inner_type = outer_type[outer_type.index('[') + 1 : -1]
            is_array_type = True
        elif '[]' in outer_type:
            inner_type = outer_type.strip('[]')
            is_array_type = True
        else:
            inner_type = outer_type

        typ, is_array_type2 = basic_GATK_type_to_CWL(argument, inner_type)

        if is_array_type2:
            is_array_type = True

        if is_array_type:
            # This needs to be done instead of adding [], as you can do correct
            # inputBinding prefixes and it works with object types
            typ = {
                "type": "array",
                "items": typ,
                "inputBinding": get_input_bindings(argument, typ == "File")
            }

        if argument['required'] == 'no':
            if isinstance(typ, list):
                typ.insert(0, 'null')
            else:
                typ = ['null', typ]

    return (typ, is_array_type)

# A dict of output type's file extentions
output_types_file_ext = {
    "GATKSAMFileWriter": ".bam",
    "PrintStream": '.txt',
    'VariantContextWriter': '.vcf'
}

def get_output_default_arg(argument, cwl_type):
    """
    Returns the default CWL argument for a given GATK argument, in a parsed form
    """
    arg_name = get_arg_id(argument)

    if argument["type"] in output_types_file_ext.keys():
        return arg_name + output_types_file_ext[argument["type"]]
    else:
        cwl_default = arg_name + ".txt"
        print("Unknown output type '{}', making the default argument '{}'".format(argument["type"], cwl_default))

        return cwl_default


def is_output_argument(argument):
    """
    Returns whether this argument's type indicates it's an output argument
    """
    return any(x in argument["type"] for x in ('PrintStream', 'Writer'))


def get_output_json(argument):
    return {
        'id': argument['name'],
        'type': ['null', 'File'] if argument["required"] == "no" else "File",
        'outputBinding': {
            'glob': '$(inputs.{})'.format(argument['name'].strip("-"))
        }
    }
