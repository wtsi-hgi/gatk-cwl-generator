"""
A collection of helper functions
"""

class GATKVersion:
    def __init__(self, version_str: str) -> None:
        self._version_str = version_str

    def is_4(self):
        return self._version_str.startswith("4")

    def is_3(self):
        return not self.is_4()

    def __str__(self):
        return self._version_str
