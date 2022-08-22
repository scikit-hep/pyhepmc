import os
import pyhepmc as hep
import pytest
from test_basic import evt  # noqa
from pyhepmc._core import stringstream
from pathlib import Path


def test_read_write(evt):  # noqa
    oss = stringstream()
    with hep.WriterAscii(oss) as f:
        f.write_event(evt)

    evt2 = hep.GenEvent()
    assert evt != evt2
    with hep.ReaderAscii(oss) as f:
        f.read_event(evt2)

    assert evt.event_number == evt2.event_number
    assert evt.momentum_unit == evt2.momentum_unit
    assert evt.length_unit == evt2.length_unit
    assert evt.particles == evt2.particles
    assert evt.vertices == evt2.vertices
    assert evt == evt2


def test_pythonic_read_write(evt):  # noqa
    oss = stringstream()
    with hep.WriterAscii(oss) as f:
        f.write(evt)

    with hep.ReaderAscii(oss) as f:
        for i, evt2 in enumerate(f):
            assert i == 0
            assert evt.particles == evt2.particles
            assert evt.vertices == evt2.vertices
            assert evt.run_info == evt2.run_info
            assert evt == evt2


def test_failed_read_file():
    with hep.ReaderAscii("test_failed_read_file.dat") as f:
        assert f.read() is None


def test_read_empty_stream(evt):  # noqa
    oss = stringstream()
    with hep.ReaderAscii(oss) as f:
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
    "writer", (hep.WriterAscii, hep.WriterAsciiHepMC2, hep.WriterHEPEVT)
)
def test_open_with_writer(evt, writer):  # noqa
    filename = f"test_open_{writer.__name__}.dat"
    with writer(filename) as f:
        f.write(evt)

    with hep.open(filename) as f:
        evt2 = f.read()

    if writer in (hep.WriterAsciiHepMC2, hep.WriterHEPEVT):
        # ToolInfo not stored in this format, so adding it manually
        evt2.run_info.tools = evt.run_info.tools

    assert evt == evt2

    os.unlink(filename)
