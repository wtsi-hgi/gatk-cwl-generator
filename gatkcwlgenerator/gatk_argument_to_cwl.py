"""
Functions to generate the CWL descriptions for GATK arguments.
The main exported functions are get_output_json and get_input_objects
"""

import copy
import logging
from typing import *

from .cwl_type_ast import *
from .common import GATKVersion
from .GATK_classes import *

_logger = logging.getLogger("gatkcwlgenerator")

class UnknownGATKTypeError(Exception):
    def __init__(self, unknown_type) -> None:
        super(UnknownGATKTypeError, self).__init__("Unknown GATK type: '" + unknown_type + "'")

        self.unknown_type = unknown_type

def is_file_type(cwl_type: CWLType) -> bool:
    return cwl_type == CWLFileType()

def GATK_type_to_CWL_type(gatk_type: str) -> CWLType:
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
    elif gatk_type in ("long", "double", "int", "string", "float", "boolean"):
        return get_cwl_basic_type(gatk_type)
    elif gatk_type == "bool":
        return CWLBooleanType()
    elif gatk_type == "file":
        return CWLFileType()
    elif gatk_type in ("byte", "integer"):
        return CWLIntType()
    elif gatk_type == "set":
        return CWLArrayType(CWLStringType())
    elif gatk_type in gatk_enum_types.keys():
        return CWLEnumType(gatk_enum_types[gatk_type])
    elif gatk_type == "map[docoutputtype,printstream]":
        # This is used in DepthOfCoverage.out, gatk 3
        return CWLStringType()
    elif gatk_type in map(str.lower, OUTPUT_TYPE_FILE_EXT.keys()):
        # insert this in here and replace it later
        return CWLStringType()  # TODO: should this be CWLFileType?
    elif "intervalbinding" in gatk_type:
        return CWLUnionType(
            CWLFileType(),
            CWLStringType()
        )
    elif "rodbinding" in gatk_type or "featureinput" in gatk_type:
        # TODO: This type indicates the type of file as below. We could verify the file
        # is correct
        # https://gist.github.com/ThomasHickman/b4a0552231f4963520927812ad29eac8
        return CWLFileType()
    else:
        raise UnknownGATKTypeError("Unknown GATK type: '" + gatk_type + "'")

def get_CWL_type_for_argument(argument: GATKArgument, toolname: str) -> CWLType:
    cwl_type: CWLType
    gatk_type = argument.type

    if argument.name in ("input_file", "input"):
        gatk_type = "List[File]"

    if argument.name == "intervals":
        # Enforce the GATK 3 type and fix https://github.com/broadinstitute/gatk/issues/4196
        if toolname == "GenomicsDBImport":
            gatk_type = "IntervalBinding[Feature]"
        else:
            gatk_type = "List[IntervalBinding[Feature]]"

    if argument.name == "genomicsdb-workspace-path":
        cwl_type = CWLDirectoryType()
    elif toolname == "GenotypeGVCFs" and argument.name == "variant":
        cwl_type = CWLUnionType(CWLFileType(), CWLArrayType(CWLFileType()), CWLDirectoryType())
    elif argument.options:
        cwl_type = CWLEnumType([x['name'] for x in argument.options])
    else:
        try:
            cwl_type = GATK_type_to_CWL_type(gatk_type)
        except UnknownGATKTypeError as error:
            _logger.warning(
                "Unable to assign to a CWL type, defaulting to string\nArgument: %s   Type: %s",
                argument.long_prefix[2:],
                error.unknown_type
            )

            cwl_type = CWLStringType()

    if argument.is_output_argument():
        file_or_string_type = cwl_type.find_node(lambda node: node == CWLFileType() or node == CWLStringType())
        if file_or_string_type is not None:
            file_or_string_type.name = "string"
        else:
            _logger.warning(f"Output argument {argument.long_prefix} should have a string or file type in it. GATK type: {gatk_type}")

    string_type: Optional[CWLStringType] = cwl_type.find_node(lambda node: node == CWLStringType())

    # overload the type of a gatk argument if think it should be a string
    if string_type is not None and argument.infer_if_file():
        string_type.name = "File"

    if isinstance(cwl_type, CWLArrayType):
        cwl_type = CWLUnionType(cwl_type, cwl_type.inner_type)

    if not argument.is_required():
        return CWLOptionalType(cwl_type)
    else:
        return cwl_type

def get_input_argument_name(argument: GATKArgument, gatk_version: GATKVersion) -> str:
    if argument.is_output_argument():
        if gatk_version.is_3():
            return argument.name + "Filename"
        else:
            return argument.name + "-filename"

    return argument.name


def get_depth_of_coverage_outputs():
    # TODO autogenerate this from
    # https://software.broadinstitute.org/gatk/documentation/tooldocs/3.8-0/org_broadinstitute_gatk_tools_walkers_coverage_DepthOfCoverage.php
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

            outputs.append({
                "id": f"{output_suffix}Output",
                "doc": f"The {output_suffix} generated file",
                "type": "File?",
                "outputBinding": {
                    "glob": f"$(inputs.out + '{output_suffix}')"
                }
            })

    return outputs


def gatk_argument_to_cwl(argument: GATKArgument, toolname: str, gatk_version: GATKVersion) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns inputs and outputs for a given gatk argument, in the form (inputs, outputs).
    """
    inputs = get_input_objects(argument, toolname, gatk_version)

    # Special-case annotations, since they can only take certain values (see #14).
    # NB: annotation-group is different, and the possible values are not documented anywhere.
    if argument.name in ("annotation", "annotations-to-exclude"):
        assert len(inputs) == 1
        inputs[0]["type"] = ["null", "annotation_type", "annotation_type[]"]
        # In GATK 3, CombineGVCFs and GenotypeGVCFs allow the value "none" to remove the default annotations.
        # This isn't allowed in any other tools or in GATK 4.
        if gatk_version.is_3() and toolname in ("CombineGVCFs", "GenotypeGVCFs"):
            inputs[0]["type"].append({"type": "enum", "symbols": ["none"]})

    if toolname == "DepthOfCoverage" and argument.name == "out":
        outputs = get_depth_of_coverage_outputs()
    elif toolname == "RandomlySplitVariants" and argument.name == "prefixForAllOutputFileNames":
        outputs = [{
            "id": "splitToManyOutput",
            "doc": "Output if --splitToManyFiles is true",
            "type": "File[]?",
            "outputBinding": {
                "glob": "$(inputs.prefixForAllOutputFileNames + '.split.*.vcf')"
            }
        }]
    elif toolname == "GenomicsDBImport" and argument.name == "genomicsdb-workspace-path":
        outputs = [{
            "id": "genomicsdb-workspace-path-out",
            "doc": "Resulting GenomicsDB workspace (corresponding to the input genomicsdb-workspace-path).",
            "type": "Directory",
            "outputBinding": {
                "glob": "$(inputs['genomicsdb-workspace-path'])"
            }
        }]
    elif argument.is_output_argument():
        outputs = [get_output_json(argument, gatk_version)]
    else:
        outputs = []

    return inputs, outputs

def get_input_binding(argument, gatk_version: GATKVersion, cwl_type: CWLType) -> Dict:
    has_file_type = cwl_type.find_node(is_file_type) is not None
    has_array_type = cwl_type.find_node(lambda node: isinstance(node, CWLArrayType)) is not None
    has_boolean_type = cwl_type.find_node(lambda node: node == CWLBooleanType())

    if gatk_version.is_4() and has_boolean_type:
        return {
            "prefix": argument.long_prefix,
            "valueFrom": f"$(generateGATK4BooleanValue())"
        }
    elif has_file_type:
        return {
            "valueFrom": f"$(applyTagsToArgument(\"{argument.long_prefix}\", inputs['{argument.name}_tags']))"
        }
    elif has_array_type:
        return {
            "valueFrom": f"$(generateArrayCmd(\"{argument.long_prefix}\"))"
        }
    else:
        return {
            "prefix": argument.long_prefix
        }

# ((string | string[])[])?
ARRAY_TAGS_TYPE = CWLOptionalType(
    CWLArrayType(
        CWLUnionType(
            CWLStringType(),
            CWLArrayType(
                CWLStringType()
            )
        )
    )
)

# (string | string[])?
NON_ARRAY_TAGS_TAGS = CWLOptionalType(
    CWLUnionType(
        CWLStringType(),
        CWLArrayType(
            CWLStringType()
        )
    )
)

def get_input_objects(argument: GATKArgument, toolname: str, gatk_version: GATKVersion) -> List[Dict]:
    """
    Returns a list of cwl input arguments for expressing the given gatk argument

    :param argument: The cwl argument, as specified in the json file

    :returns: CWL objects to describe the given argument
    """

    cwl_type = get_CWL_type_for_argument(argument, toolname)

    has_array_type = False
    has_file_type = cwl_type.find_node(is_file_type) is not None

    array_node: Optional[CWLArrayType] = cwl_type.find_node(lambda node: isinstance(node, CWLArrayType))
    if array_node is not None:
        # NOTE: this is fixing the issue at https://github.com/common-workflow-language/cwltool/issues/593
        array_node.add_input_binding({
            "valueFrom": "$(null)"
        })

        has_array_type = True

    base_cwl_arg = {
        "doc": argument.summary,
        "id": get_input_argument_name(argument, gatk_version),
        "type": cwl_type.get_cwl_object(),
        "inputBinding": get_input_binding(argument, gatk_version, cwl_type)
    }

    # Provide a default output location for required output arguments
    if argument.has_default() and argument.is_output_argument() and argument.is_required():
        base_cwl_arg["default"] = argument.get_output_default_arg()

    if argument.name == "reference_sequence" or argument.name == "reference":
        base_cwl_arg["secondaryFiles"] = [".fai", "^.dict"]
    elif argument.name == "input_file" or argument.name == "input":
        base_cwl_arg["secondaryFiles"] = "$(self.basename + self.nameext.replace('m','i'))"

    if has_file_type:
        if has_array_type:
            tags_type = ARRAY_TAGS_TYPE.get_cwl_object()
        else:
            tags_type = NON_ARRAY_TAGS_TAGS.get_cwl_object()

        tag_argument = {
            "doc": "A argument to set the tags of '{}'".format(argument.name),
            "id": argument.name + "_tags",
            "type": copy.deepcopy(tags_type)
        }

        return [base_cwl_arg, tag_argument]
    else:
        return [base_cwl_arg]


def get_output_json(argument: GATKArgument, gatk_version: GATKVersion) -> Dict:
    input_argument_name = get_input_argument_name(argument, gatk_version)

    return {
        'id': argument.name,
        'doc': f"Output file from corresponding to the input argument {input_argument_name}",
        'type': "File" if argument.is_required() else "File?",
        'outputBinding': {
            'glob': f"$(inputs['{input_argument_name}'])"
        }
    }
