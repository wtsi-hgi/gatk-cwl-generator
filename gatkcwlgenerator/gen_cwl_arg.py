"""
Functions to generate the CWL descriptions for GATK arguments.
The main exported functions are get_output_json and get_input_objects
"""

import copy
import logging
import re

from .cwl_ast import *
from .helpers import is_gatk_3

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
    do that in get_CWL_type_for_argument.
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
    elif gatk_type == "map[docoutputtype,printstream]":
        # This is used in DepthOfCoverage.out, gatk 3
        return CWLBasicType("string")
    elif gatk_type in map(str.lower, output_type_to_file_ext.keys()):
        # insert this in here and replace it later
        return CWLBasicType("string")
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

def infer_if_gatk_argument_is_file(argument):
    """
    Infer from properties of an argument if it is a file. To be used if an argument's type contains a 'string'
    as a string could represent a string or a file.
    """
    known_non_file_params = [
        "--prefixForAllOutputFileNames",
        "--READ_NAME_REGEX"
    ]

    return "file" in argument["summary"] and argument["name"] not in known_non_file_params

def get_CWL_type_for_argument(argument, toolname):
    prefix = argument['name']

    gatk_type = argument['type']

    if prefix == "--input_file" or prefix == "--input":
        gatk_type = "List[File]"

    if prefix == "--intervals":
        # Enforce the GATK 3 type and fix https://github.com/broadinstitute/gatk/issues/4196
        if toolname == "GenomicsDBImport":
            gatk_type = "IntervalBinding[Feature]"
        else:
            gatk_type = "List[IntervalBinding[Feature]]"

    if prefix == "--genomicsdb-workspace-path":
        cwl_type = CWLBasicType("Directory")
    elif argument['options']:
        cwl_type = CWLEnumType([x['name'] for x in argument['options']])
    else:
        try:
            cwl_type = GATK_type_to_CWL_type(gatk_type)
        except UnknownGATKTypeError as error:
            _logger.warning(
                "Unable to assign to a CWL type, defaulting to string\nArgument: %s   Type: %s",
                argument['name'][2:],
                error.unknown_type
            )

            cwl_type = CWLBasicType("string")

    if is_output_argument(argument):
        file_or_string_type = cwl_type.find_node(lambda node: node == CWLBasicType("File") or node == CWLBasicType("string"))
        if file_or_string_type is not None:
            file_or_string_type.name = "string"
        else:
            _logger.warning(f"Output argument {argument['name']} should have a string or file type in it. GATK type: {argument['type']}")

    string_type = cwl_type.find_node(lambda node: node == CWLBasicType("string"))

    # overload the type of a gatk argument if think it should be a string
    if string_type is not None and infer_if_gatk_argument_is_file(argument):
        string_type.name = "File"

    if isinstance(cwl_type, CWLArrayType):
        cwl_type = CWLUnionType(cwl_type, cwl_type.inner_type)

    if argument['required'] == 'no':
        return CWLOptionalType(cwl_type)
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

    raise Exception("Output argument should be defined in output_type_to_file_ext")


def get_input_argument_name(argument, gatk_version):
    arg_id = get_arg_id(argument)

    if is_output_argument(argument):
        if is_gatk_3(gatk_version):
            return arg_id + "Filename"
        else:
            return arg_id + "-filename"

    return arg_id


def get_depth_of_coverage_outputs():
    # TODO: autogenerate this from https://software.broadinstitute.org/gatk/documentation/tooldocs/3.8-0/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php
    partition_types = ["library", "read_group", "sample"]
    output_types = [
        "summary",
        "statistics",
        "interval_summary",
        "interval_statistics",
        "gene_summary",
        "gene_statistics",
        "cumulative_coverage_counts",
        "cumulative_coverage_proportions"
    ]

    outputs = []

    for partition_type in partition_types:
        for output_type in output_types:
            output_suffix = f"{partition_type}_{output_type}"

            outputs.extend({
                "id": f"{output_suffix}Output",
                "doc": f"The {output_suffix} generated file",
                "type": "File?",
                "outputBinding": {
                    "glob": f"$(inputs.out + '{output_suffix}')"
                }
            })

    return outputs

def gatk_argument_to_cwl_arguments(argument, toolname: str, gatk_version: str):
    """
    Returns inputs and outputs for a given gatk argument, in the form (inputs, outputs).
    """

    inputs = get_input_objects(argument, toolname, gatk_version)

    arg_id = get_arg_id(argument)

    input_argument_name = get_input_argument_name(argument, gatk_version)

    if arg_id in ("create-output-bam-md5", "create-output-variant-md5", "create-output-bam-index", "create-output-variant-index"):
        outputs = [{
            "id": arg_id[len("create-output-"):],
            "doc": f"{'md5' if arg_id.endswith('md5') else 'index'} file generated if {arg_id} is true",
            "type": "File?",
            "outputBinding": {
                "glob": f"$(inputs['{input_argument_name}'] + '.md5')" if arg_id.endswith("md5") else [
                    f"$(inputs['{input_argument_name}'] + '.idx')",
                    f"$(inputs['{input_argument_name}'] + '.tbi')"
                ]
            }
        }]
    elif toolname == "DepthOfCoverage" and arg_id == "out":
        outputs = get_depth_of_coverage_outputs()
    elif toolname == "RandomlySplitVariants" and arg_id == "prefixForAllOutputFileNames":
        outputs = [{
            "id": "splitToManyOutput",
            "doc": "Output if --splitToManyFiles is true",
            "type": "File[]?",
            "outputBinding": {
                "glob": "$(inputs.prefixForAllOutputFileNames + '.split.*.vcf')"
            }
        }]
    elif is_output_argument(argument):
        outputs = [get_output_json(argument, gatk_version)]
    else:
        outputs = []

    return inputs, outputs

def get_input_binding(argument, gatk_version, cwl_type: CWLType):
    has_file_type = cwl_type.find_node(is_file_type) is not None
    has_array_type = cwl_type.find_node(lambda node: isinstance(node, CWLArrayType)) is not None
    has_boolean_type = cwl_type.find_node(lambda node: node == CWLBasicType("boolean"))

    arg_id = get_arg_id(argument)

    if has_file_type:
        return {
            "valueFrom": f"$(applyTagsToArgument(\"--{arg_id}\", inputs['{arg_id}_tags']))"
        }
    elif has_array_type:
        return {
            "valueFrom": f"$(generateArrayCmd(\"--{arg_id}\"))"
        }
    else:
        return {
            "prefix": argument["name"]
        }

ARRAY_TAGS_TYPE = [
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

NON_ARRAY_TAGS_TAGS = [
    "null",
    "string",
    {
        "type": "array",
        "items": "string"
    }
]

def get_input_objects(argument, toolname, gatk_version):
    """
    Returns a list of cwl input arguments for expressing the given gatk argument

    :param argument: The cwl argument, as specified in the json file
    :param options: Command line options

    :returns: CWL objects to describe the given argument
    """

    arg_id = get_arg_id(argument)

    cwl_type = get_CWL_type_for_argument(argument, toolname)

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
        "id": get_input_argument_name(argument, gatk_version),
        "type": cwl_type.get_cwl_object(),
        "inputBinding": get_input_binding(argument, gatk_version, cwl_type)
    }

    # Provide a default output location for required output arguments
    if is_arg_with_default(argument) and is_output_argument(argument) and argument['required'] != 'no':
        base_cwl_arg["default"] = get_output_default_arg(argument)

    if arg_id == "reference_sequence" or arg_id == "reference":
        base_cwl_arg["secondaryFiles"] = [".fai", "^.dict"]
    elif arg_id == "input_file" or arg_id == "input":
        base_cwl_arg["secondaryFiles"] = "$(self.basename + self.nameext.replace('m','i'))"

    if has_file_type:
        if has_array_type:
            tags_type = ARRAY_TAGS_TYPE
        else:
            tags_type = NON_ARRAY_TAGS_TAGS

        tag_argument = {
            "type": copy.deepcopy(tags_type),
            "doc": "A argument to set the tags of '{}'".format(arg_id),
            "id": arg_id + "_tags"
        }

        return [base_cwl_arg, tag_argument]
    else:
        return [base_cwl_arg]


def is_output_argument(argument):
    """
    Returns whether this this argument's properties indicate is should be an output argument.
    """
    known_output_files = [
        "--score-warnings",
        "--read-metadata",
        "--filter-metrics"
    ]

    output_suffixes = [
        "-out",
        "-output",
        "Output",
        "Out"
    ]

    no_num_or_bool_type = all((x not in argument["type"] for x in ("boolean", "int")))
    has_known_gatk_output_types = any(output_type in argument["type"] for output_type in output_type_to_file_ext)
    has_output_suffix = any(map(argument["name"].endswith, output_suffixes))
    in_known_output_files = argument["name"] in known_output_files

    return no_num_or_bool_type and \
        (has_known_gatk_output_types \
        or has_output_suffix \
        or in_known_output_files)


def get_output_json(argument, gatk_version):
    is_optional_arg = argument["required"] == "no"

    input_argument_name = get_input_argument_name(argument, gatk_version)

    return {
        'id': get_arg_id(argument),
        'doc': f"Output file from corresponding to the input argument {input_argument_name}",
        'type': 'File?' if is_optional_arg else "File",
        'outputBinding': {
            'glob': f"$(inputs['{input_argument_name}'])"
        }
    }
