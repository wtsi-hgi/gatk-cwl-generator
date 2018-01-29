from os import path, sys

import pytest
from bs4 import BeautifulSoup

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.cwl_type_ast import *
from gatkcwlgenerator.parse_gatk_commands import (assert_cwl_type_matches_value,
                                                  parse_gatk_pre_box,
                                                  parse_program_command)
from gatkcwlgenerator.web_to_gatk_tool import (get_extra_arguments,
                                               get_gatk_links,
                                               get_gatk_tool)
from gatkcwlgenerator.gatk_argument_to_cwl import get_CWL_type_for_argument


gatk_3_test = r"""
java -jar GenomeAnalysisTK.jar \
    -R reference.fasta \
    -T CompareCallableLoci \
    -comp1 callable_loci_1.bed \
    -comp2 callable_loci_2.bed \
    [-L input.intervals \]
    -o comparison.table

java -jar GenomeAnalysisTK.jar \
    -R reference.fasta \
    -T CompareCallableLoci
"""

gatk_4_test = r"""
gatk --java-options "-Xmx4g" HaplotypeCaller  \
    -R Homo_sapiens_assembly38.fasta \
    -I input.bam \
    -O output.g.vcf.gz \
    -ERC GVCF
"""

EG_3 = "3.5-0"
EG_4 = "4.0.0.0"

@pytest.fixture(params=[EG_3, EG_4])
def gatk_version(request):
    return GATKVersion(request.param)

def test_parse_gatk_pre_box():
    assert len(parse_gatk_pre_box(gatk_3_test)) == 2
    assert len(parse_gatk_pre_box(gatk_4_test)) == 1

def test_does_cwl_type_match_value():
    assert assert_cwl_type_matches_value(CWLFileType(), "a_file.file")
    assert assert_cwl_type_matches_value(CWLFloatType(), "1234")
    assert not assert_cwl_type_matches_value(CWLFileType(), "this is a string")

    assert assert_cwl_type_matches_value(CWLArrayType(CWLStringType()), ["one", "two"])
    assert assert_cwl_type_matches_value(CWLBooleanType(), True)

EXCLUDE_TOOLS = (
    "PathSeqBuildReferenceTaxonomy" #https://github.com/broadinstitute/gatk/issues/4284
)

def test_gatk_docs(gatk_version: GATKVersion):
    gatk_links = get_gatk_links(gatk_version)

    extra_arguments = get_extra_arguments(gatk_version, gatk_links)

    for tool_url in gatk_links.tool_urls:
        gatk_tool = get_gatk_tool(tool_url, extra_arguments)
        soup = BeautifulSoup(gatk_tool.description, "html.parser")
        if gatk_tool.name not in EXCLUDE_TOOLS:
            for pre_element in soup.select("pre"):
                commands = parse_gatk_pre_box(pre_element.text)
                if commands is not None:
                    for command in commands:
                        assert command.tool_name == gatk_tool.name

                        for argument_name, argument_value in command.arguments.items():
                            try:
                                cwlgen_argument = gatk_tool.get_argument(argument_name)
                            except KeyError:
                                print(f"Argument {argument_name} not found for tool {gatk_tool.name}")

                            cwl_type = get_CWL_type_for_argument(cwlgen_argument, gatk_tool.name)

                            if not assert_cwl_type_matches_value(cwl_type, argument_value):
                                print(f"Argument {argument_name} in tool {gatk_tool.name} is invalid")
