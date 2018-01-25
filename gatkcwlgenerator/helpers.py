"""
A collection of helper functions
"""

import typing as t

def is_gatk_3(version):
    return not version.startswith("4")

