import re
import shlex
import textwrap
from typing import *
from collections import namedtuple

import requests_cache

from gatkcwlgenerator.common import GATKVersion
from gatkcwlgenerator.web_to_gatk_tool import get_gatk_tool, get_gatk_links, get_extra_arguments
from gatkcwlgenerator.gatk_argument_to_cwl import get_CWL_type_for_argument
from gatkcwlgenerator.cwl_type_ast import *

requests_cache.install_cache()

COMMAND_STARTS = ("java -jar ", "gatk ")

ParsedCommand = namedtuple("ParsedCommand", ["program_name", "positional_arguments", "arguments"])

def parse_program_command(command: str):
    # below is not parsed in shlex, so do it for it
    command = command.replace("\\\n", "")
    # Remove technically-invalid but frequently-used comments after a line continuation.
    command = re.sub(r"\\\s+#.*$", "", command, flags=re.MULTILINE)
    lexed_command = shlex.split(command, comments=True, posix=False)
    program_name = lexed_command[0]

    arguments = dict() # type: Dict[str, Union[str, List[str], bool]]
    positional_arguments = []

    cmdline_key = None # type: str

    for element in lexed_command[1:]:
        if element == "--":
            # It seems that, usually, anything after "--" is Spark configuration that we don't have types for.
            break
        if element[0] == "-":
            if cmdline_key is not None:
                if arguments.get(cmdline_key):
                    raise Exception(f"Cannot have two boolean arguments. Found two of {cmdline_key}.")
                arguments[cmdline_key] = True
            if ":" in element:
                # Remove a tag, if there is one (e.g. "--variant:RawHapMap" to "--variant").
                element = element[:element.index(":")]
            cmdline_key = element
        else:
            if cmdline_key is None:
                if element != "...":
                    # If there's a positional argument '...', it's probably just indicating that
                    # the previous (non-positional) argument can be repeated, so we ignore it.
                    # For example, see the first GATK 3 UnifiedGenotyper example:
                    # <https://software.broadinstitute.org/gatk/documentation/tooldocs/3.8-0/org_broadinstitute_gatk_tools_walkers_genotyper_UnifiedGenotyper.php>
                    positional_arguments.append(element)
            else:
                old_value = arguments.get(cmdline_key)

                if old_value is None:
                    arguments[cmdline_key] = element
                elif isinstance(old_value, bool):
                    raise Exception(f"Invalid usage of argument {cmdline_key}")
                elif isinstance(old_value, list):
                    arguments[cmdline_key].append(element) # type: ignore
                else:
                    arguments[cmdline_key] = [old_value, element]

            cmdline_key = None

    return ParsedCommand(
        program_name=program_name,
        positional_arguments=positional_arguments,
        arguments=arguments
    )

def test_parse_program_command():
    pass

def remove_from_dict_if_exists(input_dict: Dict, keys: Iterable[str]):
    for key in keys:
        if input_dict.get(key) is not None:
            del input_dict[key]

GATKCommand = namedtuple("GATKCommand", ["tool_name", "arguments"])
def parse_gatk_command(gatk_command: str) -> Optional[GATKCommand]:
    parsed_command = parse_program_command(gatk_command)

    arguments = parsed_command.arguments

    if parsed_command.program_name == "java" and arguments.get("-jar") == "GenomeAnalysisTK.jar":
        assert not parsed_command.positional_arguments, parsed_command.positional_arguments

        gatk_tool_name = arguments.get("-T") or arguments.get("--analysis_type")

        remove_from_dict_if_exists(arguments, (
            "-T",
            "--analysis_type",
            "-jar",
            "-Xmx4g"
        ))
    elif parsed_command.program_name == "gatk":
        assert len(parsed_command.positional_arguments) == 1, parsed_command
        gatk_tool_name = parsed_command.positional_arguments[0]

        remove_from_dict_if_exists(arguments, ["--java-options"])
    else:
        return None

    return GATKCommand(
        tool_name=gatk_tool_name,
        arguments=arguments
    )

def parse_gatk_pre_box(pre_box_text: str) -> List:
    # get rid of "[<COMMAND>]"
    pre_box_text = re.sub(r"\[(.*)\]", r"\1", pre_box_text)
    # remove common whitespace
    pre_box_text = textwrap.dedent(pre_box_text)
    # remove leading whitespace
    pre_box_text = pre_box_text.lstrip(" \n")

    box_text_lines = pre_box_text.split("\n")

    # Find the start of the first command (in case there are comments before it).
    while not box_text_lines[0].startswith(COMMAND_STARTS):
        box_text_lines.pop(0)
        if not box_text_lines:
            return []

    # Split each potential command into a separate string.
    commands: List[str] = []
    command_lines = [] # type: List[str]
    for line in box_text_lines:
        if line.startswith(COMMAND_STARTS) and command_lines:
            commands.append("\n".join(command_lines))
            command_lines = [line]
        else:
            command_lines.append(line)
    commands.append("\n".join(command_lines))

    # Attempt to parse each command, and return the ones we can parse.
    parsed_commands: List[GATKCommand] = []
    for command in commands:
        parsed = parse_gatk_command(command)
        if parsed is not None:
            parsed_commands.append(parsed)

    return parsed_commands

def infer_cwl_type_for_value(value: str) -> CWLType:
    """
    Given a string of a cwl value, returns a list of correct cwl types
    """
    if value in ("true", "false", "True", "False"):
        return CWLBooleanType()

    try:
        float(value)
    except ValueError:
        pass
    else:
        if "." in value:
            return CWLFloatType()
        else:
            return CWLIntType()

    if "." in value:
        return CWLFileType()

    if "/" in value:
        return CWLDirectoryType()

    return CWLStringType()

def assert_cwl_type_matches_value(cwl_type: CWLType, value: Union[bool, str, List[str]]):
    if isinstance(value, bool):
        value = "true"

    if isinstance(value, list):
        return isinstance(cwl_type, CWLArrayType) and \
            any(
                map(lambda args: assert_cwl_type_matches_value(*args), zip(cwl_type.children, value))
            )

    infered_cwl_type = infer_cwl_type_for_value(value)

    if cwl_type.contains(infered_cwl_type):
        return True
    else:
        print(f"Type: {cwl_type} doesn't match infered cwl type: {infered_cwl_type} for value {repr(value)}")
        return False
