from types import SimpleNamespace
from typing import *

class GATKType(SimpleNamespace):
    pass

class GATKInfo(SimpleNamespace):
    pass

output_type_to_file_ext = {
    "GATKSAMFileWriter": ".bam",
    "PrintStream": '.txt',
    'VariantContextWriter': '.vcf.gz'
}

class GATKArgument(SimpleNamespace):
    def __init__(self, **kwargs):
        self._init_dict = kwargs

    def is_required(self):
        return self.required != "no"

    @property
    def long_prefix(self):
        return self._init_dict["name"]

    def get_output_default_arg(self):
        """
        Returns the overriden default argument for an output argument.
        """
        # Output types are defined to be keys of output_type_to_file_ext, so
        # this should not error
        for output_type in output_type_to_file_ext:
            if self.type in output_type:
                return self.id + output_type_to_file_ext[output_type]

        raise Exception("Output argument should be defined in output_type_to_file_ext")

    @property
    def id(self):
        return self.long_prefix.strip("-")

    def infer_if_file(self):
        """
        Infer from properties of an argument if it is a file. To be used if an argument's type contains a 'string'
        as a string could represent a string or a file.
        """
        known_non_file_params = [
            "--prefixForAllOutputFileNames",
            "--READ_NAME_REGEX"
        ]

        return "file" in self.summary and self.name not in known_non_file_params

    def is_output_argument(self):
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

        no_num_or_bool_type = all((x not in self.type for x in ("boolean", "int")))
        has_known_gatk_output_types = any(output_type in self.type for output_type in output_type_to_file_ext)
        has_output_suffix = any(map(self.name.endswith, output_suffixes))
        in_known_output_files = self.name in known_output_files

        return no_num_or_bool_type and \
            (has_known_gatk_output_types \
            or has_output_suffix \
            or in_known_output_files)

    def has_default(self):
        return  self.defaultValue != "NA" \
            and self.defaultValue.lower() != "none" \
            and self.defaultValue.lower() != "null"

    def __getattr__(self, name: str):
        return self._init_dict[name]

class GATKTool:
    def __init__(
        self,
        original_tool_dict: Dict,
        additional_arguments: List
    ):
        self.original_tool_dict = original_tool_dict
        self._additional_arguments = additional_arguments

    @property
    def docs(self):
        return self.original_tool_dict["description"]

    @property
    def arguments(self) -> List[Dict]:
        return self._additional_arguments + self.original_tool_dict["arguments"]

    def __getattr__(self, name: str):
        return self.original_tool_dict[name]