import contextlib
import io
import os
import subprocess
import tempfile
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from os import path, sys

import pytest
import requests
from cwltool.main import main as cwltool_main

# Use fix from https://stackoverflow.com/a/19190695 to import from the base directory
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
import gatkcwlgenerator as cwl_gen


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

HAPLOTYPE_CALLER3_ARGS = """
reference_sequence:
   class: File
   path: {0}/cwl-example-data/chr22_cwl_test.fa
input_file: #must be BAM or CRAM
   class: File
   #path: /path/to/input/file
   path: {0}/cwl-example-data/chr22_cwl_test.cram
outFilename: out.gvcf.gz""".format(base_dir)

HAPLOTYPE_CALLER4_ARGS = """
input:
   class: File
   path: {0}/cwl-example-data/chr22_cwl_test.cram
reference:
   class: File
   path: {0}/cwl-example-data/chr22_cwl_test.fa
output-filename: out.gvcf.gz
""".format(base_dir)

def run_haplotype_caller(haplotypeCaller_location, extra_info="", interval=1, filetext=None, expect_failure=False, gatk4=False):
    return run_tool("HaplotypeCaller", haplotypeCaller_location, extra_info, interval, filetext, expect_failure, gatk4)

def run_tool(toolname, tool_location, extra_info="", interval=1, filetext=None, expect_failure=False, gatk4=False):
    """
    Runs a cwl tool with the specified data
    """
    if filetext is None:
        extra_info += "\nintervals: [chr22:10591400-{}]".format(10591400 + interval)
        filetext = (HAPLOTYPE_CALLER4_ARGS if gatk4 else HAPLOTYPE_CALLER3_ARGS) + "\n" + extra_info

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
                            "--leave-container",
                            "--leave-tmpdir",
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

supported_versions = ["3.5-0", "3.6-0", "3.7-0", "3.8-0", "4.0.0.0"]

@pytest.mark.skip(reason="""
The API for gatk is probably going to remain the same for specific versions.
As this takes a lot of time, it should be disabled generally and used
for testing added supporting versions for the first time.
""")
@pytest.mark.parametrize("version", supported_versions)
class TestGenerateCWL:
    def test_no_arguments_in_annotator(self, version):
        # If arguments are in annotator modules, we probably need to add them to the CWL file
        for url in cwl_gen.get_json_links(version).annotator_urls:
            ann_json = requests.get(url).json()
            assert not ann_json["arguments"]

# Integration tests


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

@pytest.fixture(scope="module", params=supported_versions)
def HaplotypeCaller_runner(request, tmpdir_factory):
    version = request.param

    output_dir = tmpdir_factory.mktemp("HaplotypeCaller")
    cwl_gen.gatk_cwl_generator(
        dev=True,
        version=version,
        out=str(output_dir),
        include="HaplotypeCaller"
    )

    file_location = path.join(str(output_dir), "cwl", "HaplotypeCaller.cwl")

    def closure(*nargs, **kwargs):
        return run_haplotype_caller(file_location, *nargs, gatk4=("4" in version), **kwargs)

    return closure

@pytest.fixture(scope="session")
def echo_HalotypeCaller_runner(tmpdir_factory):
    output_dir = tmpdir_factory.mktemp("EchoHaplotypeCaller")
    cwl_gen.gatk_cwl_generator(
        dev=True,
        no_docker=True,
        version="3.5-0",
        gatk_command="echo",
        out=str(output_dir),
        include="HaplotypeCaller"
    )

    file_location = path.join(str(output_dir), "cwl", "HaplotypeCaller.cwl")

    def closure(extra_text=""):
        return run_haplotype_caller(file_location, extra_text)

    return closure

class TestTagsOutput:
    def test_non_array_tags(self, echo_HalotypeCaller_runner, tmpdir):
        test_file = tmpdir.mkdir("test_non_array_tags").join("test_file")
        test_file.write("test")
        extra_text = \
f"""alleles:
    class: File
    path: {test_file}
alleles_tags:
    - tag1
    - tag2"""

        output = echo_HalotypeCaller_runner(extra_text)

        # NOTE: in this test (and tests below), we can't use the filename of test_file
        # as it changes in the docker container.
        assert "--alleles:tag1,tag2 " in output.stderr

    def test_array_tags(self, echo_HalotypeCaller_runner, tmpdir):
        test_file = tmpdir.mkdir("test_array_tags").join("test_file")
        test_file.write("test")
        extra_text = \
f"""activeRegionIn:
    - class: File
      path: {test_file}
    - class: File
      path: {test_file}
activeRegionIn_tags:
    - - tag1
      - tag2
    - tag3"""

        output = echo_HalotypeCaller_runner(extra_text)

        assert f"--activeRegionIn:tag1,tag2 " in output.stderr

        assert f"--activeRegionIn:tag3 " in output.stderr

def test_array_cmd_override(echo_HalotypeCaller_runner):
    output = echo_HalotypeCaller_runner("annotation: ['one', 'two']")

    assert "--annotation one" in output.stderr

    assert "--annotation two" in output.stderr

    output = echo_HalotypeCaller_runner("annotation: one")

    assert "--annotation one" in output.stderr


def _is_cwlfile_valid(file_location):
    try:
        run_command("cwl-runner --validate " + file_location)
        print("Validated " + file_location)
    except AssertionError as e:
        return e

def test_are_cwl_files_valid(cwl_files):
    thread_pool = ThreadPool(4)
    results = thread_pool.map(
        _is_cwlfile_valid,
        [path.join(cwl_files, file_name) for file_name in os.listdir(cwl_files)]
    )

    exceptions = []
    for result in results:
        if isinstance(result, AssertionError):
            print(result)
            exceptions.append(result)

    if exceptions:
        raise AssertionError("Not all cwl files are valid:\n" + "\n\n".join(exceptions))

def test_haplotype_caller(request, HaplotypeCaller_runner):
    HaplotypeCaller_runner()

@pytest.mark.skip("This takes too long, so skip it")
class TestGATKTypes:
    # Test if the haplotype caller accepts all the correct types
    def test_boolean_type(self, HaplotypeCaller_runner):
        assert "ThreadEfficiencyMonitor" in HaplotypeCaller_runner("monitorThreadEfficiency: True").stderr

    def test_integers_type(self, HaplotypeCaller_runner):
        assert "42 data thread" in HaplotypeCaller_runner("num_threads: 42", expect_failure=True).stderr

    def test_string_type(self, HaplotypeCaller_runner):
        assert "Specified name does not exist in input bam files" in \
            HaplotypeCaller_runner("sample_name: invalid_sample_name", expect_failure=True).stderr

    def test_file_type(self, HaplotypeCaller_runner):
        BQSR_arg = """
BQSR:
   class: File
   path: {0}/cwl-example-data/chr22_cwl_test.fa
""".format(base_dir)
        assert "Bad input: The GATK report has an unknown/unsupported version in the header" in \
            HaplotypeCaller_runner(BQSR_arg, expect_failure=True).stderr

    def test_enum_type(self, HaplotypeCaller_runner):
        assert "Strictness is LENIENT" in HaplotypeCaller_runner("validation_strictness: LENIENT").stderr

    def test_list_type(self, HaplotypeCaller_runner):
        run_with_larger_intervals = HaplotypeCaller_runner(extra_info="",
            filetext=HAPLOTYPE_CALLER3_ARGS + "\nintervals: [chr22:10591400-10591500, chr22:10591500-10591645]")

        assert "Processing 246 bp from intervals" in run_with_larger_intervals.stderr
