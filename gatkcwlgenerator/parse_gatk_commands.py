import re
import shlex
import textwrap
from typing import *
from collections import namedtuple

from gatkcwlgenerator.cwl_type_ast import *

COMMAND_STARTS = ("java -jar ", "gatk ")

ParsedCommand = namedtuple("ParsedCommand", ["program_name", "positional_arguments", "arguments"])

def parse_program_command(command: str) -> ParsedCommand:
    # below is not parsed in shlex, so do it for it
    command = command.replace("\\\n", "")
    # Remove technically-invalid but frequently-used comments after a line continuation.
    command = re.sub(r"\\\s+#.*$", "", command, flags=re.MULTILINE)
    # Split up arguments like "--foo=bar".
    command = re.sub(r"(--\S+)=(\S+)", r"\1 \2", command)
    lexed_command = shlex.split(command, comments=True, posix=False)
    program_name = lexed_command[0]

    arguments: Dict[str, Union[str, List[str], bool]] = {}
    positional_arguments: List[str] = []

    cmdline_key: Optional[str] = None

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
                    arguments[cmdline_key].append(element)  # type: ignore
                else:
                    arguments[cmdline_key] = [old_value, element]

            cmdline_key = None

    if cmdline_key is not None:
        if arguments.get(cmdline_key):
            raise Exception(f"Cannot have two boolean arguments. Found two of {cmdline_key}.")
        arguments[cmdline_key] = True

    return ParsedCommand(
        program_name=program_name,
        positional_arguments=positional_arguments,
        arguments=arguments
    )

T = TypeVar("T")

def remove_from_dict_if_exists(input_dict: Dict[T, Any], keys: Iterable[T]) -> None:
    for key in keys:
        if input_dict.get(key) is not None:
            del input_dict[key]

GATKCommand = namedtuple("GATKCommand", ["tool_name", "arguments"])
def parse_gatk_command(gatk_command: str) -> Optional[GATKCommand]:
    parsed_command = parse_program_command(gatk_command)

    arguments = parsed_command.arguments

    if parsed_command.program_name == "java" and arguments.get("-jar") == "GenomeAnalysisTK.jar":
        assert not parsed_command.positional_arguments, parsed_command

        gatk_tool_name = arguments.get("-T") or arguments.get("--analysis_type")

        remove_from_dict_if_exists(arguments, (
            "-T",
            "--analysis_type",
            "-jar",
            "-Xmx4g"
        ))
    elif parsed_command.program_name == "gatk":
        assert len(parsed_command.positional_arguments) == 1 or parsed_command.positional_arguments[0] == "CompareBaseQualities", parsed_command
        gatk_tool_name = parsed_command.positional_arguments[0]

        remove_from_dict_if_exists(arguments, ["--java-options"])
    else:
        return None

    return GATKCommand(
        tool_name=gatk_tool_name,
        arguments=arguments
    )

def parse_gatk_pre_box(pre_box_text: str) -> List[GATKCommand]:
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
    command_lines: List[str] = []
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

def infer_cwl_type_for_value(value: str) -> List[CWLType]:
    """
    Given a string of a CWL value, returns a list of possible CWL types.
    """
    if value in ("true", "false", "True", "False"):
        return [CWLBooleanType()]

    try:
        float(value)
    except ValueError:
        pass
    else:
        if "." in value:
            return [CWLFloatType()]
        else:
            return [CWLIntType()]

    if "." in value:
        return [CWLFileType(), CWLStringType()]

    if "/" in value:
        return [CWLFileType(), CWLDirectoryType(), CWLStringType()]

    return [CWLStringType(), CWLFileType(), CWLDirectoryType()]

def assert_cwl_type_matches_value(cwl_type: CWLType, value: Union[bool, str, List[str]]) -> bool:
    while isinstance(cwl_type, CWLOptionalType):
        cwl_type = cwl_type.inner_type

    if isinstance(cwl_type, CWLUnionType):
        return any(assert_cwl_type_matches_value(child, value) for child in cwl_type.children)

    if isinstance(value, bool):
        value = "true"

    if isinstance(value, list):
        return isinstance(cwl_type, CWLArrayType) and \
            any(
                map(lambda args: assert_cwl_type_matches_value(*args), zip(cwl_type.children, value))
            )

    inferred_cwl_types = infer_cwl_type_for_value(value)

    if any(cwl_type.contains(t) for t in inferred_cwl_types):
        return True
    elif any(isinstance(t, CWLFileType) or isinstance(t, CWLDirectoryType) for t in inferred_cwl_types) and cwl_type.contains(CWLStringType()):
        # Output filenames are usually inferred to be files (or sometimes directories), but must be strings in CWL.
        return True
    elif any(isinstance(t, CWLStringType) for t in inferred_cwl_types) and (
            cwl_type.has_file_type() or cwl_type.find_node(lambda node: isinstance(node, CWLEnumType))
    ):
        # Filenames may sometimes be inferred to be strings, and enum arguments are invariably detected as strings.
        return True
    else:
        # This is not necessarily an indication of a problem in the docs,
        # since there may be other types (in a union) that will be tested
        # once this type is known not to match.
        return False
