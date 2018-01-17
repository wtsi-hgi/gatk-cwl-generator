"""
Functions to generate the CWL descriptions for GATK arguments.
The main exported functions are get_output_json and get_input_objects
"""

import logging
import re

from .cwl_ast import *

_logger = logging.getLogger("gatkcwlgenerator")

def get_arg_id(argument):
    return argument["name"].strip("-")

def is_arg_with_default(argument):
    return  argument['defaultValue'] != "NA" \
        and argument['defaultValue'].lower() != "none" \
        and argument['defaultValue'].lower() != "null"

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
        # NOTE: this actually refers to VariantContext.Type in the gatk 3 source code
        "type": ['INDEL', 'SNP', 'MIXED', 'MNP', 'SYMBOLIC', 'NO_VARIATION'],
        # from https://git.io/vNmFy
        "sparkcollectors": ["CollectInsertSizeMetrics", "CollectQualityYieldMetrics"],
        # from https://git.io/vNmAe
        "metricaccumulationlevel": ["ALL_READS", "SAMPLE", "LIBRARY", "READ_GROUP"]
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
    elif "rodbinding" in gatk_type or "featureinput" in gatk_type:
        # TODO: This type indicates the type of file as below. We could verify the file
        # is correct
        # https://gist.github.com/ThomasHickman/b4a0552231f4963520927812ad29eac8
        return CWLBasicType("File")
    else:
        raise UnknownGATKTypeError("Unknown GATK type: '" + gatk_type + "'")

def check_cwl_type_makes_sense(cwl_type: CWLType, argument):
    if cwl_type.find_node(is_file_type) is None:
        if "file" in argument["summary"] \
         and isinstance(cwl_type, CWLBasicType) and cwl_type.name == "string" \
         and not is_output_argument(argument):
             _logger.warning(
                f"Argument {argument['name']} has 'file' in it's summary and is type {argument['type']}\nsummary: {argument['summary']}"
             )

def is_gatk_argument_a_file(argument):
    known_non_file_params = [
        "--prefixForAllOutputFileNames",
        "--READ_NAME_REGEX"
    ]

    return "file" in argument["summary"] and argument["name"] not in known_non_file_params

def get_base_CWL_type_for_argument(argument):
    prefix = argument['name']

    if argument['options']:
        return CWLEnumType([x['name'] for x in argument['options']])

    gatk_type = argument['type']

    if prefix == "--input_file" or prefix == "--input":
        gatk_type = "List[File]"
    elif is_output_argument(argument):
        gatk_type = "string"

    if is_gatk_argument_a_file(argument):
        gatk_type = "File"

    if prefix == "--genomicsdb-workspace-path":
        return CWLBasicType("Directory")

    try:
        cwl_type = GATK_type_to_CWL_type(gatk_type)
    except UnknownGATKTypeError as error:
        _logger.warning(
            "Unable to assign to a CWL type, defaulting to string\nArgument: %s   Type: %s",
            argument['name'][2:],
            error.unknown_type
        )

        cwl_type = CWLBasicType("string")

    #check_cwl_type_makes_sense(cwl_type, argument)

    if isinstance(cwl_type, CWLArrayType):
        return CWLUnionType(cwl_type, cwl_type.inner_type)
    else:
        return cwl_type

output_type_to_file_ext = {
    "GATKSAMFileWriter": ".bam",
    "PrintStream": '.txt',
    'VariantContextWriter': '.vcf.gz'
}

def get_output_default_arg(argument):
    """
    Returns the overriden default argument for an output argument.
    """
    # Output types are defined to be keys of output_type_to_file_ext, so
    # this should not error
    for output_type in output_type_to_file_ext:
        if argument["type"] in output_type:
            return get_arg_id(argument) + output_type_to_file_ext[output_type]

    # The definition of is_output_argument should mean this is never reached
    return ".txt"
    #raise Exception("Output argument should be defined in output_type_to_file_ext")

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
        # NOTE: this is fixing the issue at https://github.com/common-workflow-language/cwltool/issues/593
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
            "valueFrom": "$(applyTagsToArgument(\"--{0}\", inputs['{0}_tags']))".format(arg_id)
        }
    elif has_array_type:
        base_cwl_arg["inputBinding"] = {
            "valueFrom": "$(generateArrayCmd(\"--{}\"))".format(arg_id)
        }
    else:
        base_cwl_arg["inputBinding"] = {
            "prefix": argument["name"]
        }

    # Provide a default output location for required output arguments
    if is_output_argument(argument) and argument['required'] != 'no':
        base_cwl_arg["default"] = get_output_default_arg(argument)

    if arg_id == "reference_sequence" or arg_id == "reference":
        base_cwl_arg["secondaryFiles"] = [".fai", "^.dict"]
    elif arg_id == "input_file" or arg_id == "input":
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
    known_output_files = [
        "--score-warnings",
        "--read-metadata",
        "--filter-metrics",
        "--prefixForAllOutputFileNames"
    ]

    return any(output_type in argument["type"] for output_type in output_type_to_file_ext) \
        or "-out" in argument["name"] \
        or re.match("-out(put)?$", argument["name"]) is not None \
        or argument["name"].endswith("Out") or argument["name"].endswith("Output") \
        or argument["name"] in known_output_files


def get_output_json(argument):
    if argument["name"] == "--prefixForAllOutputFileNames":
        return {
            "id": "splitToManyOutput",
            "type": "File?",
            "outputBinding": {
                "glob": "$(inputs.prefixForAllOutputFileNames + '.split.*.vcf')"
            }
        }

    is_optional_arg = argument["required"] == "no"

    return {
        'id': get_arg_id(argument) + "Output",
        'type': 'File?' if is_optional_arg else "File",
        'outputBinding': {
            'glob': "$(inputs.['{}'])".format(get_arg_id(argument))
        }
    }