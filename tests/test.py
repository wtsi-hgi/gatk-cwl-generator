from os import sys, path
# Use fix from https://stackoverflow.com/a/19190695 to import from the base directory
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import CWL.GATKtools as GATKTools # TODO: Update this when I have better paths

from __future__ import print_function

import subprocess
import os
from os import path
import unittest
from multiprocessing import Process

# Assertions

def assert_contains(a, b, message=""):
    if not b in a:
        raise AssertionError("{}The text \"{}\" does not appear in:\n{}".format(message, b, a))

"""
Runs the specified command and reports it as an AssertionError if it fails (can override this with
expect_failure)
"""
def run_command(command, fail_message=None, expect_failure=False):
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcode = process.returncode

    if exitcode != 0 and not expect_failure:

        raise AssertionError("{}\"{}\" fails with exit code {}\nstdout:\n{}\nstderr:\n{}".format(
            "" if fail_message is None else fail_message + ": ",
            command,
            exitcode,
            stdout,
            stderr
        ))

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

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.chdir(base_dir) # Need to be in the base directory for the cwl-runner to pick up the correct files

"""
Runs the haplotype_caller tool with the specified data
"""
def run_haplotype_caller(extra_info="", interval=1, filetext=None, expect_failure=False):
    if filetext is None:
        extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)
        filetext = ht_caller_base_text + "\n" + extra_info

    f = open("tests/test_haplotypecaller_input.yml", "w")
    f.write(filetext)
    f.close()

    return run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl tests/test_haplotypecaller_input.yml", expect_failure=expect_failure)

# Unit tests

supported_versions = ["3.5-0", "current"]

class TestGenerateCWL(unittest.TestCase):
    def test_get_json_links(self):
        for version in supported_versions:
            json_links = GATKTools.generate_cwl.get_json_links(version)
            for links in json_links[1].items():
                self.assertTrue(links) # assert it's not empty

# Integration tests

class TestGeneratedCWLFiles(unittest.TestCase):
    base_cwl_path = path.join(base_dir, "cwlscripts/cwlfiles")

    def is_cwlfile_valid(self, cwl_file):
        run_command("cwl-runner --validate " + path.join(self.base_cwl_path, cwl_file))

    def test_are_cwl_files_valid(self):
        exceptions = []
        for cwl_file in os.listdir("cwlscripts/cwlfiles"):
            try:
                print("Validated " + cwl_file)
                run_command("cwl-runner --validate " + path.join(self.base_cwl_path, cwl_file))
            except AssertionError as e:
                print(e)
                exceptions.append(e)

        if exceptions:
            raise AssertionError("Not all cwl files are valid:\n" + "\n\n".join(exceptions))

    def test_haplotype_caller(self):
        run_command("cwl-runner cwlscripts/cwlfiles/HaplotypeCaller.cwl HaplotypeCaller_inputs.yml")

    # Test if the haplotype caller accepts all the correct types

    def test_boolean_type(self):
        assert_contains(run_haplotype_caller("monitorThreadEfficiency: True").stderr, "ThreadEfficiencyMonitor")

    def test_integers_type(self):
        assert_contains(run_haplotype_caller("num_threads: 42", expect_failure=True).stderr, "42 data thread")

    def test_string_type(self):
        assert_contains(run_haplotype_caller("sample_name: invalid_sample_name", expect_failure=True).stderr,
            "Specified name does not exist in input bam files")

    def test_file_type(self):
        assert_contains(run_haplotype_caller("BQSR: /data/chr22_cwl_test.fa", expect_failure=True).stderr, 
            "Bad input: The GATK report has an unknown/unsupported version in the header")

    def test_enum_type(self):
        assert_contains(run_haplotype_caller("validation_strictness: LENIENT").stderr, "Strictness is LENIENT")

    def test_list_type(self):
        run_with_larger_intervals = run_haplotype_caller(filetext=ht_caller_base_text +
            "\nintervals: [chr22:10591400-10591500, chr22:10591500-10591645]")

        assert_contains(run_with_larger_intervals.stderr, "Processing 246 bp from intervals")

    def test_default_used(self):
        assert_contains(run_haplotype_caller().stderr, "-indelHeterozygosity 1.25E-4")

"""
The entry point for testing
"""
def test():
    unittest.main()

if __name__ == "__main__":
    test()