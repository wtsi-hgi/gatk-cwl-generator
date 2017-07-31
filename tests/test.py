from __future__ import print_function

import subprocess
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

def assert_contains(a, b, message=""):
    if a in b:
        raise AssertionError("{}{} in {}".format(message, a, b))

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

    return CommandOutput(stdout, stderr, exitcode)

class CommandOutput():
    def __init__(self, stdout, stderr, exitcode):
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode

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
def run_haplotype_caller(extra_info="", interval=1, filetext=None):
    if filetext is None:
        extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)
        filetext = ht_caller_base_text + "\n" + extra_info

    f = open("tests/test_haplotypecaller_input.yml", "w")
    f.write(filetext)
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
    debug_stderr = run_haplotype_caller("debug: True").stderr

    assert_gt(len(debug_stderr), len(normal_run.stderr), "Debug mode does not increase the size of stdout: ")

def test_integers():
    assert_contains(run_haplotype_caller("num_threads: 42").stderr, "42 data thread")

def test_string():
    pass

def test_file():
    pass

def test_enum_type():
    assert_contains(run_haplotype_caller("validation_strictness: LENIENT").stderr, "Strictness is LENIENT")

def test_list_type():
    run_with_larger_intervals = run_haplotype_caller(filetext=ht_caller_base_text+"\nintervals: [chr22:10591400-10591500, chr22:10591500-10591645]")

    assert_contains(run_with_larger_intervals.stderr, "Processing 246 bp from intervals")

def test_default_used():
    pass

"""
The entry point for testing
"""
def test():
    test_integers()

if __name__ == "__main__":
    test()