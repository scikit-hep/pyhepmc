import pytest
from test_basic import evt  # noqa
import pyhepmc

view = pytest.importorskip("pyhepmc.view")  # depends on graphviz and particle


def test_dot(evt):  # noqa
    d = view.to_dot(evt)
    s = str(d)
    assert s.startswith('digraph "dummy-1.0\nevent number = 1')
    assert "in_1" in s
    assert "in_2" in s
    assert "in_3" not in s
    assert "out_6" in s
    assert "out_7" in s
    assert "out_8" in s


def test_dot_2():
    ev = pyhepmc.GenEvent()
    # unknown particle
    p = pyhepmc.GenParticle((0, 0, 0, 1e-3), pid=91, status=1)
    ev.add_particle(p)
    # invalid particle
    q = pyhepmc.GenParticle((0, 0, 0, 1e-3), pid=0, status=1)
    ev.add_particle(q)
    v = pyhepmc.GenVertex()
    v.add_particle_in(p)
    v.add_particle_out(q)
    ev.add_vertex(v)
    d = view.to_dot(ev)
    s = str(d)
    assert "Internal" in s
    assert "Invalid" in s


def test_dot_3(evt):  # noqa
    d = view.to_dot(evt, size=(5, 6))
    assert d.graph_attr["size"] == "5,6"


def test_repr_html(evt):  # noqa
    d = view.to_dot(evt)
    assert d._repr_image_svg_xml() == evt._repr_html_()
