import pytest
from test_basic import evt  # noqa
import pyhepmc
from matplotlib.testing.compare import compare_images, comparable_formats
from pathlib import Path
import io
import os
import numpy as np

view = pytest.importorskip("pyhepmc.view")  # depends on graphviz and particle

CDIR = Path(__file__).parent
RESULT_DIR = CDIR / "fig"
REFERENCE_DIR = CDIR / "data"
RESULT_DIR.mkdir(exist_ok=True)

TESTABLE_FORMATS = set(view.SUPPORTED_FORMATS) & set(comparable_formats())


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


@pytest.mark.parametrize("ext", view.SUPPORTED_FORMATS)
def test_savefig_1(evt, ext):  # noqa
    fname = RESULT_DIR / f"test_savefig_1.{ext}"
    view.savefig(evt, fname)

    with io.BytesIO() as f2:
        g = view.to_dot(evt)
        view.savefig(g, f2, format=ext)
        f2.seek(0)
        with open(fname, "rb") as f1:
            # Both buffers should be almost equal.
            # They may differ in the creation date,
            # which should be less than 64 bytes
            a1 = np.frombuffer(f1.read(), np.uint8)
            a2 = np.frombuffer(f2.read(), np.uint8)
            assert len(a1) > 0
            assert np.sum(a1 != a2) < 64


def test_savefig_2(evt):  # noqa
    with pytest.raises(ValueError):
        view.savefig(evt, "foo")

    with pytest.raises(ValueError):
        view.savefig(evt, "foo.foo")

    with pytest.raises(ValueError):
        with io.BytesIO() as f:
            view.savefig(evt, f)

    with io.BytesIO() as f:
        g = view.to_dot(evt)
        with pytest.warns(RuntimeWarning):
            view.savefig(g, f, format="png", color_hadron="green")


@pytest.mark.skipif("CI" in os.environ, reason="does not work on CI")
@pytest.mark.parametrize("ext", TESTABLE_FORMATS)
def test_savefig_3(evt, ext):  # noqa
    fname = f"test_savefig_3.{ext}"
    expected = REFERENCE_DIR / fname
    actual = RESULT_DIR / fname
    view.savefig(evt, actual)
    assert compare_images(expected, actual, 1e-3) is None
