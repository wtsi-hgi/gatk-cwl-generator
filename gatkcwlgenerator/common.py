"""
A collection of helper functions
"""


import functools
import pkg_resources


@functools.total_ordering
class GATKVersion:
    def __init__(self, version_str: str) -> None:
        self._version_str = version_str
        self._version = pkg_resources.parse_version(version_str)

    def is_4(self) -> bool:
        return self._version_str.startswith("4")

    def is_3(self) -> bool:
        return not self.is_4()

    @property
    def as_version(self):
        """The GATK version number as a pkg_resources Version."""
        return self._version

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.as_version < other.as_version

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.as_version == other.as_version

    def __str__(self) -> str:
        return self._version_str
