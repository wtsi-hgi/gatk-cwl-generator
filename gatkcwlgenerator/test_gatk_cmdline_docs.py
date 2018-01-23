from os import path, sys
import argparse
import re
from collections import namedtuple
import typing
from bs4 import BeautifulSoup
import logging
import shlex

import pytest
import requests
from .main2 import *

def get_suffix_from(iterable, prefixes: List[str]):
    """
    Gets suffixes of places in the iterable which has prefixes
    in prefix. If nothing is found, return None
    """
    commands = []
    start_position = 0
    found_command = False

    for i, _ in enumerate(iterable):
        for start in prefixes:
            if iterable[i: i + len(start)] == start:
                found_command = True
                if start_position != 0:
                    commands.append(iterable[start_position: i])
                start_position = i + len(start)

    if not found_command:
        return None

    commands.append(iterable[start_position:])
    return commands

def get_cmdline_dict(split_cmdline: List[str]):
    arguments = dict()
    cmdline_key = None

    for element in split_cmdline:
        if element[0] == "-":
            if cmdline_key is not None:
                arguments[cmdline_key] = True

            cmdline_key = element[1:]
        else:
            if cmdline_key is None:
                raise Exception("Invalid parse")
            else:
                arguments[cmdline_key] = element

    return arguments

GATKCommandLine = namedtuple("GATKCommandLine", ["tool_name", "arguments"])

def get_args_from_cwl(example: str, gatk_version: bool) -> typing.Dict[str, str]:
    example = re.sub(r"\[(.*)\]", r"\1", example)
    example = re.sub(r"#.*\n", "", example)
    example = example.replace("\n", " ").replace("\\", "").replace("...", "")

    lexed_command = shlex.split(example)

    gatk_3_command_prefixes = [
        ["java", "-jar", "GenomeAnalysisTK.jar"],
        ["java", "-Xmx4g", "-jar", "GenomeAnalysisTK.jar"]
    ]

    gatk_4_command_prefixes = [
        ["gatk", "--java-options", "-Xmx4g"]
    ]

    commands_array = get_suffix_from(
        lexed_command,
        gatk_3_command_prefixes if is_gatk_3(gatk_version) else gatk_4_command_prefixes
    )
    if commands_array is None:
        return None

    commands = []

    if is_gatk_3(gatk_version):
        for command_array in commands_array:
            cmdline_dict = get_cmdline_dict(command_array)
            tool_name = cmdline_dict["T"]
            del cmdline_dict["T"]

            commands.append(GATKCommandLine(
                tool_name=tool_name,
                arguments=cmdline_dict
            ))
    else:
        for command_array in commands_array:
            cmdline_dict = get_cmdline_dict(command_array[1:])

            commands.append(GATKCommandLine(
                tool_name=command_array[0],
                arguments=cmdline_dict
            ))

    return commands

gatk_3_test = r"""
java -jar GenomeAnalysisTK.jar \
    -R reference.fasta \ # this is a comment
    -T CompareCallableLoci \
    -comp1 callable_loci_1.bed \
    -comp2 callable_loci_2.bed \
    [-L input.intervals \]
    -o comparison.table

java -jar GenomeAnalysisTK.jar \
    -R reference.fasta \ # this is a comment
    -T CompareCallableLoci
"""

gatk_4_test = r"""
gatk --java-options "-Xmx4g" HaplotypeCaller  \
    -R Homo_sapiens_assembly38.fasta \
    -I input.bam \
    -O output.g.vcf.gz \
    -ERC GVCF
"""

def test_get_args_from_cwl():
    assert len(get_args_from_cwl(gatk_3_test, "3.5-0")[0].arguments) == 5
    assert len(get_args_from_cwl(gatk_4_test, "4.0.0.0")[0].arguments) == 4

def test_cwl_docs_in_docs():
    import requests_cache
    requests_cache.install_cache() # Decreases the time to run dramatically

    gatk_version = "3.5-0"
    gatk_links = get_gatk_links(gatk_version)

    gatk_tools = get_gatk_tools(gatk_links, gatk_version)
    for tool in gatk_tools:
        print(f"Processing {tool.name}")
        soup = BeautifulSoup(tool.docs, "html.parser")

        for docs_pre in soup.select("pre"):
            example_text = docs_pre.text

            arguments = get_args_from_cwl(example_text, gatk_version)
            if arguments is not None:
                # do something
                pass