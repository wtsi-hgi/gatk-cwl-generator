from gatkcwlgenerator.GATK_classes import GATKTool

def test_gatk_tool_override():
    gatk_tool = GATKTool(
        {
            "arguments": [{
                "name": "arg1",
                "prop": 1
            }]
        },
        [
            {
                "name": "arg1",
                "prop": 2,
            },
            {
                "name": "arg2",
                "prop": 1
            }
        ]
    )

    assert len(list(gatk_tool.arguments)) == 2

    assert gatk_tool.get_argument("arg1").dict.prop == 1
    assert gatk_tool.get_argument("arg2").dict.prop == 1
