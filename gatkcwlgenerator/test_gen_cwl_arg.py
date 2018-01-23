from .gen_cwl_arg import get_input_objects
from types import SimpleNamespace
from .GATK_classes import GATKArgument


def test_get_input_objects():
    input_ob = get_input_objects(GATKArgument(**
        {
            "summary": "Minimum probability for a locus to be considered active.",
            "name": "--active-probability-threshold",
            "synonyms": "NA",
            "type": "double",
            "required": "no",
            "fulltext": "",
            "defaultValue": "0.002",
            "minValue": "-Infinity",
            "maxValue": "Infinity",
            "minRecValue": "NA",
            "maxRecValue": "NA",
            "kind": "advanced",
            "options": []
        }),
        "HaplotypeCaller",
        "4.0.0.0"
    )

    assert len(input_ob) >= 1

    assert input_ob[0].to_dict() == {
        'doc': 'Minimum probability for a locus to be considered active.',
        'id': 'active-probability-threshold',
        'type': 'double?',
        'inputBinding': {
            'prefix': '--active-probability-threshold'
        }
    }
