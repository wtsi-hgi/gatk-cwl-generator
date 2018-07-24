"""
A collection of helper functions
"""


class GATKVersion:
    def __init__(self, version_str: str) -> None:
        self._version_str = version_str

    def is_4(self) -> bool:
        return self._version_str.startswith("4")

    def is_3(self) -> bool:
        return not self.is_4()

    def __str__(self) -> str:
        return self._version_str
