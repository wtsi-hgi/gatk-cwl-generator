from os import sys, path
# Use fix from https://stackoverflow.com/a/19190695 to import from the base directory
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import gatkcwlgenerator as cwl_gen

import subprocess
import os
from os import path
import unittest
from multiprocessing import Process

import requests

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

default_args = """
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

def run_haplotype_caller(extra_info="",interval=1, filetext=None, expect_failure=False):
    return run_tool("HaplotypeCaller", extra_info, interval, filetext, expect_failure)

"""
Runs the haplotype_caller tool with the specified data
"""
def run_tool(toolname, extra_info="",interval=1, filetext=None, expect_failure=False):
    if filetext is None:
        extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)
        filetext = "analysis_type: {}\n".format(toolname) + default_args + "\n" + extra_info

    f = open("tests/test_haplotypecaller_input.yml", "w")
    f.write(filetext)
    f.close()

    return run_command("cwl-runner cwl_files_3.5/cwl/{}.cwl tests/test_haplotypecaller_input.yml".format(toolname), expect_failure=expect_failure)

# Unit tests

class TestGenerateCWL(unittest.TestCase):
    supported_versions = ["3.5", "current"]
    def test_get_json_links(self):
        for version in self.supported_versions:
            json_links = cwl_gen.get_json_links(version)
            for link_type, links in json_links.__dict__.items():
                self.assertTrue(links, 
                    "There are no links of type '{}' in gatk version {}".format(
                        link_type,
                        version
                    ))

    def test_no_arguments_in_annotator(self):
        # If arguments are in annotator modules, we probably need to add them to the CWL file
        for version in self.supported_versions:
            for url in cwl_gen.get_json_links(version).annotator_urls:
                ann_json = requests.get(url).json()
                self.assertFalse(ann_json["arguments"])

# Integration tests

class TestRunsCorrectly(unittest.TestCase):
    supported_versions = ["3.5", "current", "4.beta-latest"]
    def test_runs(self):
        for version in self.supported_versions:
            run_command("python2 gatkcwlgenerator/main.py -v {} --dev".format(version))

class TestGeneratedCWLFiles(unittest.TestCase):
    base_cwl_path = path.join(base_dir, "cwl_files_3.5/cwl")

    def is_cwlfile_valid(self, cwl_file):
        run_command("cwl-runner --validate " + path.join(self.base_cwl_path, cwl_file))

    def test_are_cwl_files_valid(self):
        exceptions = []
        for cwl_file in os.listdir(self.base_cwl_path):
            try:
                print("Validated " + cwl_file)
                run_command("cwl-runner --validate " + path.join(self.base_cwl_path, cwl_file))
            except AssertionError as e:
                print(e)
                exceptions.append(e)

        if exceptions:
            raise AssertionError("Not all cwl files are valid:\n" + "\n\n".join(exceptions))

    def test_haplotype_caller(self):
        run_command("cwl-runner cwl_files_3.5/cwl/HaplotypeCaller.cwl examples/HaplotypeCaller_inputs.yml")

    # Test if the haplotype caller accepts all the correct types

    def test_boolean_type(self):
        self.assertIn("ThreadEfficiencyMonitor", run_haplotype_caller("monitorThreadEfficiency: True").stderr)

    def test_integers_type(self):
        self.assertIn("42 data thread", run_haplotype_caller("num_threads: 42", expect_failure=True).stderr)

    def test_string_type(self):
        self.assertIn("Specified name does not exist in input bam files", 
            run_haplotype_caller("sample_name: invalid_sample_name", expect_failure=True).stderr)

    def test_file_type(self):
        BQSR_arg = """
BQSR:
   class: File
   path: ../cwl-example-data/chr22_cwl_test.fa
"""
        self.assertIn("Bad input: The GATK report has an unknown/unsupported version in the header", 
            run_haplotype_caller(BQSR_arg, expect_failure=True).stderr)

    def test_enum_type(self):
        self.assertIn("Strictness is LENIENT", run_haplotype_caller("validation_strictness: LENIENT").stderr)

    def test_list_type(self):
        run_with_larger_intervals = run_haplotype_caller(
            filetext="analysis_type: HaplotypeCaller\n" + default_args + "\nintervals: [chr22:10591400-10591500, chr22:10591500-10591645]")

        self.assertIn("Processing 246 bp from intervals", run_with_larger_intervals.stderr)

"""
The entry point for testing
"""
def test():
    unittest.main()

if __name__ == "__main__":
    test()