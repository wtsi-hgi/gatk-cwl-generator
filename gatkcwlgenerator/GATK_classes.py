from types import SimpleNamespace
from typing import *

OUTPUT_TYPE_FILE_EXT = {
    "GATKSAMFileWriter": ".bam",
    "PrintStream": '.txt',
    'VariantContextWriter': '.vcf.gz'
}

class GATKArgument:
    def __init__(self, **kwargs):
        self._init_dict = kwargs

    def is_required(self):
        return self.dict.required != "no"

    @property
    def long_prefix(self):
        return self._init_dict["name"]

    def get_output_default_arg(self):
        """
        Returns the overriden default argument for an output argument.
        """
        # Output types are defined to be keys of output_type_to_file_ext, so
        # this should not error
        for output_type in OUTPUT_TYPE_FILE_EXT:
            if self.type in output_type:
                return self.name + OUTPUT_TYPE_FILE_EXT[output_type]

        raise Exception("Output argument should be defined in OUTPUT_TYPE_FILE_EXT")

    @property
    def name(self):
        return self.long_prefix.strip("-")

    def infer_if_file(self):
        """
        Infer from properties of an argument if it is a file. To be used if an argument's type contains a 'string'
        as a string could represent a string or a file.
        """
        known_non_file_params = [
            "prefixForAllOutputFileNames",
            "READ_NAME_REGEX"
        ]

        return "file" in self.summary and self.name not in known_non_file_params

    def is_output_argument(self):
        """
        Returns whether this this argument's properties indicate is should be an output argument.
        """
        known_output_files = [
            "score-warnings",
            "read-metadata",
            "filter-metrics",
            "output"
        ]

        output_suffixes = [
            "-out",
            "-output",
            "Output",
            "Out"
        ]

        no_num_or_bool_type = all((x not in self.type for x in ("boolean", "int")))
        has_known_gatk_output_types = any(output_type in self.type for output_type in OUTPUT_TYPE_FILE_EXT)
        has_output_suffix = any(map(self.name.endswith, output_suffixes))
        in_known_output_files = self.name in known_output_files

        return no_num_or_bool_type and \
            (has_known_gatk_output_types \
            or has_output_suffix \
            or in_known_output_files)

    def has_default(self):
        return  self.dict.defaultValue != "NA" \
            and self.dict.defaultValue.lower() != "none" \
            and self.dict.defaultValue.lower() != "null"

    @property
    def options(self):
        return self.dict.options

    @property
    def summary(self):
        return self.dict.summary

    @property
    def type(self):
        return self.dict.type

    @property
    def dict(self):
        return SimpleNamespace(**self._init_dict)

class GATKTool:
    def __init__(self, original_dict: Dict, additional_arguments: List) -> None:
        self.original_dict = original_dict
        self._additional_arguments = additional_arguments
        self._argument_dict = self._build_argument_dict()

    def _build_argument_dict(self):
        # Build a dict, where the original_dict arguments override the _additional_arguments arguments
        return dict(map(lambda argument: (argument["name"], argument), self._additional_arguments + self.original_dict["arguments"]))

    def get_argument(self, name: str) -> GATKArgument:
        return GATKArgument(**self._argument_dict[name])

    @property
    def name(self):
        return self.original_dict["name"]

    @property
    def dict(self):
        return SimpleNamespace(**self.original_dict)

    @property
    def arguments(self) -> Iterable[GATKArgument]:
        for argument_name in self._argument_dict:
            yield self.get_argument(argument_name)
