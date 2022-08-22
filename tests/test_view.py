import pytest
from test_basic import evt  # noqa
import pyhepmc

view = pytest.importorskip("pyhepmc.view")  # depends on graphviz and particle


def test_dot(evt):  # noqa
    d = view.to_dot(evt)
    s = str(d)
    assert s.startswith('digraph "event 1')
    assert "in_0" in s
    assert "in_1" in s
    assert "out_0" in s
    assert "out_1" in s
    assert "out_2" in s


def test_dot_2():
    ev = pyhepmc.GenEvent()
    # unknown particle
    p = pyhepmc.GenParticle((0, 0, 0, 1e-3), pid=91, status=1)
    ev.add_particle(p)
    v = pyhepmc.GenVertex()
    v.add_particle_in(p)
    ev.add_vertex(v)
    d = view.to_dot(ev)
    s = str(d)
    assert "Internal" in s
