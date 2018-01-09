"""
Functions to generate the CWL descriptions for GATK arguments.
The main exported functions are get_output_json and get_input_objects
"""

from .cwl_ast import *
import logging

_logger = logging.getLogger("gatkcwlgenerator")

def get_arg_id(argument):
    return argument["name"].strip("-")

def is_arg_with_default(argument):
    return  argument['defaultValue'] != "NA" \
        and argument['defaultValue'].lower() != "none"

class UnknownGATKTypeError(Exception):
    def __init__(self, unknown_type):
        super(UnknownGATKTypeError, self).__init__("Unknown GATK type: '" + unknown_type + "'")

        self.unknown_type = unknown_type

def is_file_type(typ):
    return isinstance(typ, CWLBasicType) and typ.name == "File"

def GATK_type_to_CWL_type(gatk_type):
    """
    Convert a GATK type to a CWL type.
    NOTE: No "hacks" or patching GATK types should be done in this function,
    do that in get_base_CWL_type_for_argument.
    """
    # You cannot get the enumeration information for an enumeration in a nested type, so they are hard coded here
    gatk_enum_types = {
        # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.6-0/org_broadinstitute_gatk_tools_walkers_variantutils_ValidateVariants.php
        "validationtype": ["ALL", "REF", "IDS", "ALLELES", "CHR_COUNTS"],
        # Example: https://software.broadinstitute.org/gatk/gatkdocs/3.7-0/org_broadinstitute_gatk_tools_walkers_cancer_contamination_ContEst.php#--lane_level_contamination
        "contaminationruntype": ['META', 'SAMPLE', 'READGROUP'],  # default is META
        # Example: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php#--partitionType
        "partition": ["readgroup", "sample", "library", "platform", "center",
                    "sample_by_platform", "sample_by_center", "sample_by_platform_by_center"],
        "type": ['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION']
    }

    gatk_type = gatk_type.lower()

    if 'list[' in gatk_type or 'set[' in gatk_type:
        inner_type = gatk_type[gatk_type.index('[') + 1 : -1]
        return CWLArrayType(GATK_type_to_CWL_type(inner_type))
    elif '[]' in gatk_type:
        inner_type = gatk_type.strip('[]')
        return CWLArrayType(GATK_type_to_CWL_type(inner_type))
    elif gatk_type in ("long", "double", "int", "string", "float", "boolean", "bool"):
        return CWLBasicType(gatk_type)
    elif gatk_type == "file":
        return CWLBasicType("File")
    elif gatk_type in ("byte", "integer"):
        return CWLBasicType("int")
    elif gatk_type == "set":
        return CWLArrayType(CWLBasicType("string"))
    elif gatk_type in gatk_enum_types.keys():
        return CWLEnumType(gatk_enum_types[gatk_type])
    elif "intervalbinding" in gatk_type:
        return CWLUnionType(
            CWLBasicType("File"),
            CWLBasicType("string")
        )
    elif "rodbinding" in gatk_type:
        # Possible options: https://gist.github.com/ThomasHickman/b4a0552231f4963520927812ad29eac8
        return CWLBasicType("File")
    else:
        raise UnknownGATKTypeError("Unknown GATK type: '" + gatk_type + "'")

def get_base_CWL_type_for_argument(argument):
    prefix = argument['name']

    if argument['options']:
        return CWLEnumType([x['name'] for x in argument['options']])

    gatk_type = argument['type']

    if prefix == "--input_file" or prefix == "--input":
        gatk_type = "List[File]"
    elif is_output_argument(argument):
        gatk_type = "string"

    try:
        cwl_type = GATK_type_to_CWL_type(gatk_type)
    except UnknownGATKTypeError as error:
        _logger.warning(
            "WARNING: Unable to assign to a CWL type, defaulting to string\nArgument: %s   Type: %s",
            argument['name'][2:],
            error.unknown_type
        )

        cwl_type = CWLBasicType("string")

    if isinstance(cwl_type, CWLArrayType):
        return CWLUnionType(cwl_type, cwl_type.inner_type)
    else:
        return cwl_type

def get_output_default_arg(argument):
    """
    Returns the overriden default argument for an output argument
    """
    output_type_to_file_ext = {
        "GATKSAMFileWriter": ".bam",
        "PrintStream": '.txt',
        'VariantContextWriter': '.vcf.gz'
    }

    arg_name = get_arg_id(argument)

    if argument["type"] in output_type_to_file_ext.keys():
        return arg_name + output_type_to_file_ext[argument["type"]]
    else:
        cwl_default = arg_name + ".txt"
        _logger.warning(
            "Unknown output type '%s', making the default argument '%s'",
            argument["type"],
            cwl_default
        )

        return cwl_default

def get_input_objects(argument):
    """
    Returns a list of cwl input arguments for expressing the given gatk argument

    :param argument: The cwl argument, as specified in the json file
    :param options: Command line options

    :returns: CWL objects to describe the given argument
    """
    def handle_required(typ):
        """Makes a given type optional if required"""
        if argument['required'] == 'no':
            return CWLOptionalType(typ)
        else:
            return typ

    arg_id = get_arg_id(argument)

    cwl_type = get_base_CWL_type_for_argument(argument)

    has_array_type = False
    has_file_type = cwl_type.find_node(is_file_type) is not None

    array_node = cwl_type.find_node(lambda node: isinstance(node, CWLArrayType))
    if array_node is not None:
        if has_file_type:
            array_node.add_input_binding({
                "valueFrom": "$(null)"
            })

        has_array_type = True

    base_cwl_arg = {
        "doc": argument['summary'],
        "id": arg_id,
        "type": handle_required(cwl_type).get_cwl_object()
    }

    if has_file_type:
        base_cwl_arg["inputBinding"] = {
            "valueFrom": "$(applyTagsToArgument(\"--{0}\", inputs.{0}_tags))".format(arg_id)
        }
    elif has_array_type:
        base_cwl_arg["inputBinding"] = {
            "valueFrom": "$(generateArrayCmd(\"--{}\"))".format(arg_id)
        }
    else:
        base_cwl_arg["inputBinding"] = {
            "prefix": argument["name"]
        }

    # For output arguments with a default, override the gatk default with
    # a more predictable name
    if is_arg_with_default(argument) and is_output_argument(argument):
        base_cwl_arg["default"] = get_output_default_arg(argument)

    if argument["name"] == "--reference_sequence":
        base_cwl_arg["secondaryFiles"] = [".fai", "^.dict"]
    elif "requires" in argument["fulltext"] and "files" in argument["fulltext"]:
        base_cwl_arg["secondaryFiles"] = "$(self.basename + self.nameext.replace('m','i'))"

    if has_file_type:
        if has_array_type:
            tags_type = [
                "null",
                {
                    "type": "array",
                    "items": [
                        "string",
                        {
                            "type": "array",
                            "items": "string"
                        }
                    ]
                }
            ]
        else:
            tags_type = [
                "null",
                "string",
                {
                    "type": "array",
                    "items": "string"
                }
            ]

        tag_argument = {
            "type": tags_type,
            "doc": "A argument to set the tags of '{}'".format(arg_id),
            "id": arg_id + "_tags"
        }

        return [base_cwl_arg, tag_argument]
    else:
        return [base_cwl_arg]


def is_output_argument(argument):
    """
    Returns whether this argument's type indicates it's an output argument
    """
    return any(x in argument["type"] for x in ('PrintStream', 'Writer'))


def get_output_json(argument):
    # NOTE: Whether this always outputs depends on whether the input argument is
    # specified - we can't specify this in the type, so mark it as optional if there
    # is a possibilty if could not output
    is_optional_arg = argument["required"] == "no" and not is_arg_with_default(argument)

    return {
        'id': get_arg_id(argument) + "Output",
        'type': 'File?' if is_optional_arg else "File",
        'outputBinding': {
            'glob': '$(inputs.{})'.format(argument['name'].strip("-"))
        }
    }