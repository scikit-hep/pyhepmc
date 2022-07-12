# import pytest
import pyhepmc as hep


def test_genruninfo():
    ri = hep.GenRunInfo()
    ri.tools = [("foo", "1.0", "bar")]
    ri.weight_names = ["a", "b", "c"]
    assert repr(ri) == (
        "GenRunInfo(tools=[ToolInfo(name='foo', version='1.0', description='bar')], "
        "weight_names=['a', 'b', 'c'], attributes={})"
    )
