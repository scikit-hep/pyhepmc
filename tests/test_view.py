import pytest
from test_basic import make_evt
import pyhepmc
from pyhepmc import view
from pathlib import Path
import io
import os
import numpy as np

CDIR = Path(__file__).parent
RESULT_DIR = CDIR / "fig"
REFERENCE_DIR = CDIR / "data"
RESULT_DIR.mkdir(exist_ok=True)

DOT_IS_AVAILABLE = bool(view.SUPPORTED_FORMATS)
PARTICLE_IS_AVAILABLE = True
try:
    import particle  # noqa
except ModuleNotFoundError:
    PARTICLE_IS_AVAILABLE = False


@pytest.fixture
def evt():
    return make_evt()


@pytest.fixture
def graph():
    return view.to_dot(make_evt())


def test_to_dot_1(graph):
    s = str(graph)
    assert s.startswith('digraph "dummy-1.0\nevent number = 1')
    assert "in_1" in s
    assert "in_2" in s
    assert "in_3" not in s
    assert "out_6" in s
    assert "out_7" in s
    assert "out_8" in s


def test_to_dot_2():
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
    if PARTICLE_IS_AVAILABLE:
        assert "Invalid(0)" in s
        assert "Internal(91)" in s
    else:
        assert "PDGID(0)" in s


def test_to_dot_3(evt):
    d = view.to_dot(evt, size=(5, 6))
    assert d.graph_attr["size"] == "5,6"


def test_Digraph_pipe(graph):
    if DOT_IS_AVAILABLE:
        with pytest.raises(ValueError):
            graph.pipe(format="12345678")

        assert graph._repr_png_() == graph.pipe(format="png")
    else:
        with pytest.raises(FileNotFoundError):
            graph.pipe(format="png")


@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
def test_Digraph_repr_png(graph):
    assert graph._repr_png_() == graph.pipe(format="png")


@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
def test_Digraph_repr(graph):
    from pyhepmc._graphviz import Digraph, Block

    s = repr(graph)
    graph2 = eval(s, {"Digraph": Digraph, "Block": Block})
    assert graph == graph2
    graph2.graph_attr["foo"] = "bar"
    assert graph != graph2


@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
def test_repr_html(graph, evt):
    assert evt._repr_html_() == graph._repr_html_()


@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
@pytest.mark.parametrize("ext", view.SUPPORTED_FORMATS)
def test_savefig_1(evt, ext):
    fname = RESULT_DIR / f"test_savefig_1.{ext}"
    view.savefig(evt, fname)

    with io.BytesIO() as f2:
        g = view.to_dot(evt)
        view.savefig(g, f2, format=ext)
        f2.flush()
        f2.seek(0)
        with open(fname, "rb") as f1:
            # Both buffers should be almost equal.
            # They may differ in the creation date,
            # which should be less than 150 bytes
            a1 = np.frombuffer(f1.read(), np.uint8)
            a2 = np.frombuffer(f2.read(), np.uint8)
            size = min(len(a1), len(a2))
            assert size > 0
            assert np.sum(a1[:size] != a2[:size]) < 150


def test_savefig_2(evt):
    with pytest.raises(ValueError):
        view.savefig(evt, "foo")

    with pytest.raises(ValueError):
        view.savefig(evt, "foo.foo")

    with pytest.raises(ValueError):
        with io.BytesIO() as f:
            view.savefig(evt, f)


@pytest.mark.skipif("CI" in os.environ, reason="does not work on CI")
@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
@pytest.mark.parametrize("ext", ("pdf", "png", "svg"))
def test_savefig_3(evt, ext):
    pytest.importorskip("particle")
    testing = pytest.importorskip("matplotlib.testing")
    compare = pytest.importorskip("matplotlib.testing.compare")
    testing.set_font_settings_for_testing()
    testing.set_reproducibility_for_testing()
    fname = f"test_savefig_3.{ext}"
    expected = REFERENCE_DIR / fname
    actual = RESULT_DIR / fname
    view.savefig(evt, actual)
    assert compare.compare_images(expected, actual, 1e-3) is None


@pytest.mark.skipif(not DOT_IS_AVAILABLE, reason="requires dot")
def test_savefig_4(evt):
    with io.BytesIO() as f:
        g = view.to_dot(evt)
        with pytest.warns(RuntimeWarning):
            view.savefig(g, f, format="png", color_hadron="green")
