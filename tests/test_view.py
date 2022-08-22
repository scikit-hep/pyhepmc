import pytest
from test_basic import evt  # noqa

view = pytest.importorskip("pyhepmc.view")  # depends on graphviz and particle


def test_dot(tmpdir, evt):  # noqa
    import os

    os.chdir(str(tmpdir))
    d = view.to_dot(evt)
    s = str(d)
    assert s.startswith('digraph "event 1')
    assert "in_0" in s
    assert "in_1" in s
    assert "out_0" in s
    assert "out_1" in s
    assert "out_2" in s
