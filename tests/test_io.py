import os
import pyhepmc as hep
import pyhepmc.io as io
import pytest
from test_basic import evt  # noqa
from pyhepmc._core import stringstream
from pathlib import Path
import numpy as np
import typing


def test_read_write(evt):  # noqa
    oss = stringstream()
    with io.WriterAscii(oss) as f:
        f.write_event(evt)

    evt2 = hep.GenEvent()
    assert evt != evt2
    with io.ReaderAscii(oss) as f:
        f.read_event(evt2)

    assert evt.event_number == evt2.event_number
    assert evt.momentum_unit == evt2.momentum_unit
    assert evt.length_unit == evt2.length_unit
    assert evt.particles == evt2.particles
    assert evt.vertices == evt2.vertices
    assert evt == evt2


def test_pythonic_read_write(evt):  # noqa
    oss = stringstream()
    with io.WriterAscii(oss) as f:
        f.write(evt)

    with io.ReaderAscii(oss) as f:
        for i, evt2 in enumerate(f):
            assert i == 0
            assert evt.particles == evt2.particles
            assert evt.vertices == evt2.vertices
            assert evt.run_info == evt2.run_info
            assert evt == evt2


def test_failed_read_file():
    with io.ReaderAscii("test_failed_read_file.dat") as f:
        assert f.read() is None


def test_read_empty_stream(evt):  # noqa
    oss = stringstream()
    with io.ReaderAscii(oss) as f:
        evt = hep.GenEvent()
        ok = f.read_event(evt)
        assert ok is True  # reading empty stream is ok in HepMC


@pytest.mark.parametrize("format", ("hepmc3", "hepmc2", "hepevt"))
def test_open_1(evt, format):  # noqa
    with hep.open("test_read_write_file.dat", "w", format=format) as f:
        f.write(evt)

    with hep.open("test_read_write_file.dat", format=format) as f:
        evt2 = f.read()

    if format in ("hepmc2", "hepevt"):
        # ToolInfo not stored in this format, so adding it manually
        evt2.run_info.tools = evt.run_info.tools

    assert evt == evt2

    with hep.open("test_read_write_file.dat") as f:
        evt3 = f.read()

    if format in ("hepmc2", "hepevt"):
        # ToolInfo not stored in this format, so adding it manually
        evt3.run_info.tools = evt.run_info.tools

    assert evt == evt3

    os.unlink("test_read_write_file.dat")


def test_open_2(evt):  # noqa
    with hep.open("test_read_write_file.dat", "w", precision=3) as f:
        f.write(evt)

    with hep.open("test_read_write_file.dat") as f:
        evt2 = f.read()

    assert evt != evt2

    with hep.open("test_read_write_file.dat", "w") as f:
        f.write(evt)

    with hep.open("test_read_write_file.dat") as f:
        evt3 = f.read()

    assert evt == evt3

    os.unlink("test_read_write_file.dat")


def test_open_3(evt):  # noqa
    filename = Path("test_read_write_file.dat")

    with hep.open(filename, "w") as f:
        with pytest.raises(TypeError):
            f.write(None)

        with pytest.raises(TypeError):
            f.write("foo")

    class Foo:
        def to_hepmc3(self):
            return evt

    foo = Foo()

    with hep.open(filename, "w") as f:
        f.write(foo)

    with hep.open(filename) as f:
        evt2 = f.read()

    assert evt == evt2

    filename.unlink()


@pytest.mark.parametrize(
    "writer", (io.WriterAscii, io.WriterAsciiHepMC2, io.WriterHEPEVT)
)
def test_open_with_writer(evt, writer):  # noqa
    filename = f"test_open_{writer.__name__}.dat"
    with writer(filename) as f:
        f.write(evt)

    with hep.open(filename) as f:
        evt2 = f.read()

    if writer in (io.WriterAsciiHepMC2, io.WriterHEPEVT):
        # ToolInfo not stored in this format, so adding it manually
        evt2.run_info.tools = evt.run_info.tools

    assert evt == evt2

    os.unlink(filename)


def test_deprecated_import():
    with pytest.warns(np.VisibleDeprecationWarning):
        from pyhepmc import ReaderAscii  # noqa F401


def test_attributes():
    filename = "test_attributes.dat"

    evt = hep.GenEvent()  # noqa
    p = hep.GenParticle((1, 2, 3, 4), 5, 6)
    evt.add_particle(p)
    evt.attributes = {
        "1": True,
        "2": 2,
        "3": 3.3,
        "4": hep.GenPdfInfo(),
        "5": hep.GenHeavyIon(),
        "6": hep.GenCrossSection(),
        "7": p,
        "8": [1, 2],
        "9": [1.3, 2.4],
        # cannot test this yet
        # "8": hep.HEPRUPAttribute(),
        # "9": hep.HEPEUPAttribute(),
    }

    with io.open(filename, "w") as f:
        f.write(evt)

    with io.open(filename) as f:
        evt2 = f.read()

    with pytest.raises(TypeError):
        evt2.attributes["1"].astype(hep.GenPdfInfo)

    with pytest.raises(TypeError, match="untyped list"):
        evt2.attributes["8"].astype(list)

    for k, v in evt.attributes.items():
        if k == "8":
            t = typing.List[int]
        elif k == "9":
            t = typing.List[float]
        else:
            t = type(v)

        v2 = evt2.attributes[k].astype(t)

        assert v == v2
        # UnparsedAttribute is replaced with parsed Attribute
        v3 = evt2.attributes[k]
        assert v == v3

    os.unlink(filename)
