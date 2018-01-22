from os import path, sys
import argparse
import re
from collections import namedtuple
import typing

import pytest
import requests
from cwltool.main import main as cwltool_main

# Use fix from https://stackoverflow.com/a/19190695 to import from the base directory
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
import gatkcwlgenerator as cwl_gen

def get_args_from_cwl(example: str, is_gatk3: bool) -> typing.Dict[str, str]:
    example = re.sub(r"\[(.*)\]", r"\1", example)

    parts = list(filter(None, example.replace("\n", "").replace("\\", "").split(" ")))

    if is_gatk3:
        assert parts[:3] == ["java", "-jar", "GenomeAnalysisTK.jar"]
        parts = parts[3:]
    else:
        assert parts[:4] == ["gatk",  "--java-options", '"-Xmx4g"', "HaplotypeCaller"]
        parts = parts[4:]

    print(parts)

    assert len(parts) // 2 == len(parts) / 2

    arguments = dict()

    for i in range(len(parts) // 2):
        prefix = parts[i*2]
        argument = parts[i*2 + 1]

        # Make sure we are using the correct syntax
        assert prefix[0] == "-" and prefix[1] != "-"

        arguments[prefix[1:]] = argument

    return arguments

gatk_3_test = r"""
java -jar GenomeAnalysisTK.jar \
    -R reference.fasta \
    -T CompareCallableLoci \
    -comp1 callable_loci_1.bed \
    -comp2 callable_loci_2.bed \
    [-L input.intervals \]
    -o comparison.table
"""

gatk_4_test = r"""
gatk --java-options "-Xmx4g" HaplotypeCaller  \
    -R Homo_sapiens_assembly38.fasta \
    -I input.bam \
    -O output.g.vcf.gz \
    -ERC GVCF
"""

def test_get_args_from_cwl():
    assert len(get_args_from_cwl(gatk_3_test, True)) == 6
    assert len(get_args_from_cwl(gatk_4_test, False)) == 4

def is_gatk_argument_valid(gatk_argument: str):
    cwl_argument = get_cwl_argument(gatk_argument)

    assert cwl_argument.cwl_type.is_member(gatk_argument.argument)

def check_cwl_documentation(cwl_documentation_text: str, is_gatk_3: bool, gatk_args: typing.List[cwl_gen.GATKType]):
    args = get_args_from_cwl(cwl_documentation_text, is_gatk_3)

    for gatk_arg in gatk_args:
        if args.get(gatk_arg.name) is not None:
            assert gatk_arg.cwl_type.is_in(args[gatk_arg.name])


def example_text_to_cwl(example: str, gatk_version):
    # Remove optional parts, with [...]
    example = re.sub("\[(.*)\]", "\1", example)

    parts = list(filter(None, example.strip(['\n', '\\']).split(" ")))

    if is_gatk3(gatk_version):
        assert parts[:3] == ["java", "-jar", "GenomeAnalysisTK.jar"]
        parts = parts[3:]
    else:
        assert parts[:4] == ["gatk",  "--java-options", '"-Xmx4g"', "HaplotypeCaller"]
        parts = parts[4:]

    assert len(parts) // 2 == len(parts) / 2

    arguments = []