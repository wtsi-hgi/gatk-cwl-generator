from gatkcwlgenerator.gatk_argument_to_cwl import get_depth_of_coverage_outputs

def test_get_depth_of_coverage_outputs():
    doc_outputs = get_depth_of_coverage_outputs()

    assert len(doc_outputs) > 10
