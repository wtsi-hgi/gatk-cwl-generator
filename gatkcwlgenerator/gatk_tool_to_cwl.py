"""
GATKTool -> CWL Dict
"""

import os
import logging
from typing import *

from ruamel.yaml.scalarstring import PreservedScalarString

from .gatk_argument_to_cwl import gatk_argument_to_cwl
from .common import GATKVersion
from .GATK_classes import *

_logger = logging.getLogger("gatkcwlgenerator")

INVALID_ARGS = [
    "help",
    "defaultBaseQualities",
    "analysis_type"  # this is hard coded into the baseCommand for each tool
]

# This indicates GATK modules that require extra undocumented output arguments in GATK 3.
# These haven't been ported to GATK 4, but when they are, the patched arguments need to be updated.
SPECIAL_GATK3_MODULES = [
    "DepthOfCoverage",
    "RandomlySplitVariants"
]


def get_js_library() -> str:
    js_library_path = os.path.join(
        os.path.dirname(__file__),
        "js_library.js"
    )

    with open(js_library_path) as file:
        return file.read()


JS_LIBRARY = get_js_library()


def gatk_tool_to_cwl(gatk_tool: GATKTool, cmd_line_options, annotation_names: List[str]) -> Dict:
    """
    Return a dictionary representing a CWL file from a given GATKTool.
    """

    version = GATKVersion(cmd_line_options.version)

    if gatk_tool.name in SPECIAL_GATK3_MODULES and not version.is_3():
        _logger.warning(f"Tool {gatk_tool.name}'s cwl may be incorrect. The GATK documentation needs to be looked at by a human and hasn't been yet.")

    base_command = cmd_line_options.gatk_command.split(" ")

    if version.is_3():
        base_command.append("--analysis_type")

    base_command.append(gatk_tool.name)

    cwl = {
        'id': gatk_tool.name,
        'cwlVersion': 'v1.0',
        'baseCommand': base_command,
        'class': 'CommandLineTool',
        "doc": PreservedScalarString(gatk_tool.dict.description),
        'requirements': [
            {
                "class": "ShellCommandRequirement"
            },
            {
                "class": "InlineJavascriptRequirement",
                "expressionLib": [
                    PreservedScalarString(JS_LIBRARY)
                ]
            },
            {
                "class": "SchemaDefRequirement",
                "types": [{
                    "type": "enum",
                    "name": "annotation_type",
                    "symbols": annotation_names
                }]
            }
        ] + ([] if cmd_line_options.no_docker else [{
            "class": "DockerRequirement",
            "dockerPull": cmd_line_options.docker_image_name
        }])
    }

    # Create and write the cwl file

    outputs = []
    inputs = []

    for argument in gatk_tool.arguments:
        if argument.name not in INVALID_ARGS:
            argument_inputs, argument_outputs = gatk_argument_to_cwl(
                argument,
                gatk_tool.name,
                version
            )

            synonym = argument.synonym
            if synonym is not None and len(argument_inputs) >= 1 and synonym.lstrip("-") != argument.name.lstrip("-"):
                argument_inputs[0]["doc"] += f" [synonymous with {synonym}]"

            for argument_input in argument_inputs:
                if "secondaryFiles" in argument_input:  # So reference_sequence doesn't conflict with refIndex and refDict
                    inputs.insert(0, argument_input)
                else:
                    inputs.append(argument_input)

            if argument_outputs and any(arg.name.startswith("create-output-") for arg in gatk_tool.arguments):
                # This depends on the first output always being the main one (not a tag).
                assert "tag" not in argument_outputs[0]["doc"]
                argument_outputs[0].setdefault("secondaryFiles", [])
                doc = argument.summary + argument.dict.fulltext
                if (
                    ("BAM" in doc or "bam" in argument.name) and ("VCF" not in doc and "variant" not in doc)
                    or gatk_tool.name in (
                        "UnmarkDuplicates", "FixMisencodedBaseQualityReads", "RevertBaseQualityScores", "ApplyBQSR",
                        "PrintReads"
                )):
                    # This is probably the BAM/CRAM output.
                    argument_outputs[0]["secondaryFiles"].extend([
                        "$(inputs['create-output-bam-index']? self.basename + self.nameext.replace('m', 'i') : [])",
                        "$(inputs['create-output-bam-md5']? self.basename + '.md5' : [])"
                    ])
                elif (("VCF" in doc or "variant" in doc) and "BAM" not in doc
                    or gatk_tool.name == "CNNScoreVariants"
                ):
                    # This is probably the VCF output.
                    argument_outputs[0]["secondaryFiles"].extend([
                        # If the extension is .vcf, the index's extension is .vcf.idx;
                        # if the extension is .vcf.gz, the index's extension is .vcf.gz.tbi.
                        "$(inputs['create-output-variant-index']? self.basename + (inputs['output-filename'].endsWith('.gz')? '.tbi':'.idx') : [])",
                        "$(inputs['create-output-variant-md5']? self.basename + '.md5' : [])"
                    ])
                elif "IGV formatted file" in doc or "table" in doc or argument.name in (
                    "graph-output", "activity-profile-out"
                ) or gatk_tool.name in (
                    "Pileup", "AnnotateIntervals", "VariantsToTable", "GetSampleName", "PreprocessIntervals",
                    "BaseRecalibrator", "CountFalsePositives", "CollectAllelicCounts", "CalculateMixingFractions",
                    "SplitIntervals", "GenomicsDBImport", "GetPileupSummaries", "VariantRecalibrator",
                    "CollectReadCounts", "CheckPileup", "ASEReadCounter"
                ):
                    # This is not a BAM or VCF output, no need to add secondary files.
                    pass
                else:
                    _logger.warning(f"Ambiguous output argument {argument.name} for {gatk_tool.name}")

            outputs.extend(argument_outputs)

    cwl["inputs"] = inputs
    cwl["outputs"] = outputs

    return cwl
