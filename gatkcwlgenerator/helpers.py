"""
A collection of helper functions
"""

def is_gatk_3(version):
    return not version.startswith("4")