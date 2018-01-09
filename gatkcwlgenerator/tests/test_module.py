from os import sys, path
# Use fix from https://stackoverflow.com/a/19190695 to import from the base directory
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

import gatkcwlgenerator as cwl_gen

from cwltool.main import main as cwltool_main

import subprocess
import os
from os import path
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import tempfile
import pytest

import requests

import contextlib
import io

"""
Download example data to be used in CWL integration tests
"""
@pytest.fixture(scope="module")
def example_data():
    if not os.path.isfile("cwl-example-data/chr22_cwl_test.cram"):
        from six.moves.urllib.request import urlopen
        import tarfile
        print("Downloading and extracting cwl-example-data")
        tgz = urlopen("https://cwl-example-data.cog.sanger.ac.uk/chr22_cwl_test.tgz")
        tar = tarfile.open(fileobj=tgz, mode="r|gz")
        tar.extractall(path="cwl-example-data")
        tar.close()
        tgz.close()

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
            stdout.decode(),
            stderr.decode()
        ))

    return CommandOutput(stdout.decode(), stderr.decode(), exitcode)

class CommandOutput():
    def __init__(self, stdout, stderr, exitcode):
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.chdir(base_dir) # Need to be in the base directory for the cwl-runner to pick up the correct files

default_args = """
reference_sequence:
   class: File
   #path: /path/to/fasta/ref/file
   path: {0}/cwl-example-data/chr22_cwl_test.fa
refIndex:
   class: File
   #path: /path/to/index/file
   path: {0}/cwl-example-data/chr22_cwl_test.fa.fai
refDict:
   class: File
   #path: /path/to/dict/file
   path: {0}/cwl-example-data/chr22_cwl_test.fa.dict
input_file: #must be BAM or CRAM
   class: File
   #path: /path/to/input/file
   path: {0}/cwl-example-data/chr22_cwl_test.cram
out: out.gvcf.gz""".format(base_dir)

def run_haplotype_caller(extra_info, haplotypeCaller_location, interval=1, filetext=None, expect_failure=False):
    return run_tool("HaplotypeCaller", extra_info, haplotypeCaller_location, interval, filetext, expect_failure)

def run_tool(toolname, extra_info, tool_location, interval=1, filetext=None, expect_failure=False):
    """
    Runs a cwl tool with the specified data
    """
    if filetext is None:
        extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)
        filetext = default_args + "\n" + extra_info

    # NOTE: we're not using cwltool.factory.Factory, as recommended
    # due to https://github.com/common-workflow-language/cwltool/issues/596
    # also, we can't use cwltool_main's stdout and stderr parameters, due to
    # https://github.com/common-workflow-language/cwltool/issues/597.
    # Redirecting stdout and stderr to a temporary file is the best option, as
    # this means filenumbers can be read in the POpen function in cwltool.

    with tempfile.NamedTemporaryFile("w+") as new_stdout:
        with tempfile.NamedTemporaryFile("w+") as new_stderr:
            with tempfile.NamedTemporaryFile("w+") as tmp_file:
                tmp_file.write(filetext)
                tmp_file.flush()

                with contextlib.redirect_stdout(new_stdout):
                    with contextlib.redirect_stderr(new_stderr):
                        exit_code = cwltool_main([
                            tool_location,
                            tmp_file.name
                        ])

            new_stderr.seek(0)
            new_stdout.seek(0)

            new_stdout_text = new_stdout.read()
            new_stderr_text = new_stderr.read()

    if exit_code != 0 and not expect_failure:
        raise AssertionError("cwltool failed with exit code {}\nstdout:\n{}\nstderr:\n{}".format(
            exit_code,
            new_stdout_text,
            new_stderr_text
        ))

    return CommandOutput(new_stdout_text, new_stderr_text, exit_code)

# Unit tests

supported_versions = ["3.5-0", "3.6-0", "3.7-0", "3.8-0"] #  "4.beta.6"

@pytest.mark.parametrize("version", supported_versions)
class TestGenerateCWL:
    def test_get_json_links(self, version):
        json_links = cwl_gen.get_json_links(version)
        for link_type, links in json_links.__dict__.items():
            assert links, "There are no links of type '{}' in gatk version {}".format(
                    link_type,
                    version
                )

    def test_no_arguments_in_annotator(self, version):
        # If arguments are in annotator modules, we probably need to add them to the CWL file
        for url in cwl_gen.get_json_links(version).annotator_urls:
            ann_json = requests.get(url).json()
            assert not ann_json["arguments"]

# Integration tests


def test_generate_v4():
    os.environ['PYTHONPATH'] = "."
    run_command("python -m gatkcwlgenerator -v 4.beta.6 --dev")

@pytest.fixture(scope="module", params=supported_versions)
def cwl_files(request, tmpdir_factory):
    version = request.param
    output_dir = tmpdir_factory.mktemp("HaplotypeCaller")

    cwl_gen.gatk_cwl_generator(
        dev=True,
        version=version,
        out=str(output_dir)
    )

    return path.join(str(output_dir), "cwl")

@pytest.fixture(scope="session")
def HaplotypeCallerFile(tmpdir_factory):
    output_dir = tmpdir_factory.mktemp("HaplotypeCaller")
    cwl_gen.gatk_cwl_generator(
        dev=True,
        version="3.5-0",
        out=str(output_dir),
        include="HaplotypeCaller"
    )

    return path.join(str(output_dir), "cwl", "HaplotypeCaller.cwl")

@pytest.fixture(scope="session")
def echoHalotypeCaller(tmpdir_factory):
    output_dir = tmpdir_factory.mktemp("test_annotations")

    cwl_gen.gatk_cwl_generator(
        dev=True,
        no_docker=True,
        version="3.5-0",
        gatk_command="echo",
        out=str(output_dir),
        include="HaplotypeCaller"
    )

    return path.join(str(output_dir), "cwl", "HaplotypeCaller.cwl")

class TestTagsOutput:
    def test_non_array_tags(self, echoHalotypeCaller, tmpdir):
        test_file = tmpdir.mkdir("test_non_array_tags").join("test_file")
        test_file.write("test")
        extra_text = \
"""alleles:
    class: File
    path: {}
alleles_tags:
    - tag1
    - tag2""".format(test_file)

        output = run_haplotype_caller(extra_text, echoHalotypeCaller)

        assert "--alleles:tag1,tag2 " in output.stderr

    def test_array_tags(self, echoHalotypeCaller, tmpdir):
        test_file = tmpdir.mkdir("test_array_tags").join("test_file")
        test_file.write("test")
        extra_text = \
"""activeRegionIn:
    - class: File
      path: {0}
    - class: File
      path: {0}
activeRegionIn_tags:
    - - tag1
      - tag2
    - tag3""".format(test_file)

        output = run_haplotype_caller(extra_text, echoHalotypeCaller)

        assert "--activeRegionIn:tag1,tag2 " in output.stderr

        assert "--activeRegionIn:tag3 " in output.stderr

class TestGeneratedCWLFiles:
    def _is_cwlfile_valid(self, file_location):
        try:
            run_command("cwl-runner --validate " + file_location)
            print("Validated " + file_location)
        except AssertionError as e:
            return e

    def test_are_cwl_files_valid(self, cwl_files):
        thread_pool = ThreadPool(4)
        results = thread_pool.map(
            self._is_cwlfile_valid,
            [path.join(cwl_files, file_name) for file_name in os.listdir(cwl_files)]
        )

        exceptions = []
        for result in results:
            if isinstance(result, AssertionError):
                print(result)
                exceptions.append(result)

        if exceptions:
            raise AssertionError("Not all cwl files are valid:\n" + "\n\n".join(exceptions))

    def test_haplotype_caller(self, HaplotypeCallerFile):
        run_command("cwl-runner {} examples/HaplotypeCaller_inputs.yml".format(HaplotypeCallerFile))

    # Test if the haplotype caller accepts all the correct types

    def test_boolean_type(self, HaplotypeCallerFile):
        assert "ThreadEfficiencyMonitor" in run_haplotype_caller("monitorThreadEfficiency: True", HaplotypeCallerFile).stderr

    def test_integers_type(self, HaplotypeCallerFile):
        assert "42 data thread" in run_haplotype_caller("num_threads: 42", HaplotypeCallerFile, expect_failure=True).stderr

    def test_string_type(self, HaplotypeCallerFile):
        assert "Specified name does not exist in input bam files" in \
            run_haplotype_caller("sample_name: invalid_sample_name", HaplotypeCallerFile, expect_failure=True).stderr

    def test_file_type(self, HaplotypeCallerFile):
        BQSR_arg = """
BQSR:
   class: File
   path: {0}/cwl-example-data/chr22_cwl_test.fa
""".format(base_dir)
        assert "Bad input: The GATK report has an unknown/unsupported version in the header" in \
            run_haplotype_caller(BQSR_arg, HaplotypeCallerFile, expect_failure=True).stderr

    def test_enum_type(self, HaplotypeCallerFile):
        assert "Strictness is LENIENT" in run_haplotype_caller("validation_strictness: LENIENT", HaplotypeCallerFile).stderr

    def test_list_type(self, HaplotypeCallerFile):
        run_with_larger_intervals = run_haplotype_caller(extra_info="", cwl_files_location=HaplotypeCallerFile,
            filetext=default_args + "\nintervals: [chr22:10591400-10591500, chr22:10591500-10591645]")

        assert "Processing 246 bp from intervals" in run_with_larger_intervals.stderr
