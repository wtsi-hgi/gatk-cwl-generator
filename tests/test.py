from __future__ import print_function

import subprocess
import unittest
import os
from os import path
import sys

# Assertions

def assert_equals(a, b, message=""):
    if a != b:
        raise AssertionError("{}{} != {}".format(message, a, b))


def assert_gt(a, b, message):
    if a > b:
        raise AssertionError("{}{} > {}".format(message, a, b))

"""
Runs the specified command and reports it as an AssertionError if it fails
"""
def run_command(command, fail_message=None):
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcode = process.returncode

    if exitcode != 0:
        print("{}\"{}\" fails with exit code {}\nstdout:\n{}\nstderr:\n{}".format(
            "" if fail_message is None else fail_message + ": ",
            command,
            exitcode,
            stdout,
            stderr
        ), file=sys.stderr)

        raise AssertionError("Command failed")

    return stdout, stderr, exitcode

def get_ht_caller_base_text():
    f = open("HaplotypeCaller_inputs.yml")
    text = f.read()
    f.close()

    return text

ht_caller_base_text = get_ht_caller_base_text()

base_dir = os.path.dirname(os.path.dirname(__file__))
os.chdir(base_dir) # Need to be in the base directory for the cwl-runner to pick up the correct files

"""
Runs the haplotype_caller tool with the specified data
"""
def run_haplotype_caller(extra_info):
    f = open("tests/test_haplotypecaller_input.yml", "w")
    f.write(ht_caller_base_text + "\n" + extra_info)
    f.close()

    return run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl tests/test_haplotypecaller_input.yml")

def test_cwl_file(cwl_file):
    is_valid_cwl_file(cwl_file)

def is_valid_cwl_file(cwl_file):
    run_command("cwl-runner --validate " + cwl_file)

def test_haplotype_caller():
    run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl HaplotypeCaller_inputs.yml")

def test_booleans_handled_correctly():
    print(run_haplotype_caller("debug: True"))

"""
The entry point for testing
"""
def test():
    test_booleans_handled_correctly()

if __name__ == "__main__":
    test()