from __future__ import print_function

import subprocess
import unittest
import os
from os import path
import sys
import json

# Assertions

def assert_equals(a, b, message=""):
    if a != b:
        raise AssertionError("{}{} != {}".format(message, a, b))


def assert_gt(a, b, message=""):
    if a <= b:
        raise AssertionError("{}{} <= {}".format(message, a, b))

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

ht_caller_base_text = """
analysis_type: HaplotypeCaller
reference_sequence:
   class: File
   #path: /path/to/fasta/ref/file
   path: ../cwl-example-data/chr22_cwl_test.fa 
refIndex:
   class: File
   #path: /path/to/index/file
   path: ../cwl-example-data/chr22_cwl_test.fa.fai 
refDict:
   class: File
   #path: /path/to/dict/file
   path: ../cwl-example-data/chr22_cwl_test.fa.dict 
input_file: #must be BAM or CRAM
   class: File
   #path: /path/to/input/file 
   path: ../cwl-example-data/chr22_cwl_test.cram
out: out.gvcf.gz"""

base_dir = os.path.dirname(os.path.dirname(__file__))
os.chdir(base_dir) # Need to be in the base directory for the cwl-runner to pick up the correct files

"""
Runs the haplotype_caller tool with the specified data
"""
def run_haplotype_caller(extra_info="", interval=1):
    extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)

    f = open("tests/test_haplotypecaller_input.yml", "w")
    f.write(ht_caller_base_text + "\n" + extra_info)
    f.close()

    return run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl tests/test_haplotypecaller_input.yml")

normal_run = run_haplotype_caller()

def test_cwl_file(cwl_file):
    is_valid_cwl_file(cwl_file)

def is_valid_cwl_file(cwl_file):
    run_command("cwl-runner --validate " + cwl_file)

def test_haplotype_caller():
    run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl HaplotypeCaller_inputs.yml")

def test_booleans_handled_correctly():
    debug_stderr = run_haplotype_caller("debug: True")[1]

    assert_gt(len(debug_stderr), len(normal_run[1]), "Debug mode does not increase the size of stdout: ")

def test_integers():
    with_int_json = run_haplotype_caller("activeProbabilityThreshold: 1")[0]

    with_int_filesize = json.loads(with_int_json)["--out"]["size"] # should be quite a bit less size
    normal_filesize = json.loads(normal_run[0])["--out"]["size"]

    assert_gt(normal_filesize - with_int_filesize, 100)

"""
The entry point for testing
"""
def test():
    test_integers()

if __name__ == "__main__":
    test()