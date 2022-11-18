import os
import pyhepmc as hep
import pyhepmc.io as io
import pytest
from test_basic import evt  # noqa
from pyhepmc._core import stringstream, pyiostream
from pathlib import Path
import numpy as np
import typing
import gzip
from sys import version_info
import subprocess as subp

if version_info >= (3, 9):
    list_type = list
else:
    list_type = typing.List


def test_pystream_1():
    fn = str(Path(__file__).parent / "sibyll21.dat")
    with open(fn, "rb") as f:
        with pyiostream(f, 1000) as s:
            with io.ReaderAscii(s) as r:
                ev1 = r.read()
    with io.ReaderAscii(fn) as r:
        ev2 = r.read()

    assert ev1.particles == ev2.particles
    assert ev1.vertices == ev2.vertices
    assert ev1.run_info == ev2.run_info


def test_pystream_2():
    fn = str(Path(__file__).parent / "sibyll21.dat")
    fn2 = "sibyll21.dat.gz"

    with open(fn, "rb") as f:
        with gzip.open(fn2, "w") as f2:
            f2.write(f.read())

    with gzip.open(fn2) as f:
        with pyiostream(f, 1000) as s:
            with io.ReaderAscii(s) as r:
                ev1 = r.read()

    with io.ReaderAscii(fn) as r:
        ev2 = r.read()

    assert ev1 == ev2

    os.unlink(fn2)


def test_pystream_3(evt):  # noqa
    fn = "test_pystream_3.dat.gz"
    with gzip.open(fn, "w") as f:
        with pyiostream(f, 1000) as s:
            with io.WriterAscii(s) as w:
                w.write(evt)

    with gzip.open(fn) as f:
        with pyiostream(f, 1000) as s:
            with io.ReaderAscii(s) as r:
                evt2 = r.read()

    assert evt == evt2

    os.unlink(fn)


def test_read_event_write_event(evt):  # noqa
    oss = stringstream()
    with io.WriterAscii(oss) as f:
        f.write_event(evt)

    evt2 = hep.GenEvent()
    evt3 = hep.GenEvent()
    assert evt != evt2
    with io.ReaderAscii(oss) as f:
        assert f.read_event(evt2)
        assert not f.failed()
        success = f.read_event(evt3)
        assert success  # for EOF success is true and failed() is true
        assert f.failed()

    assert evt.event_number == evt2.event_number
    assert evt.momentum_unit == evt2.momentum_unit
    assert evt.length_unit == evt2.length_unit
    assert evt.particles == evt2.particles
    assert evt.vertices == evt2.vertices
    assert evt == evt2


def test_pythonic_read_write_from_stream(evt):  # noqa
    oss = stringstream()
    with io.WriterAscii(oss) as f:
        f.write(evt)

    with io.ReaderAscii(oss) as f:
        n = 0
        for evt2 in f:
            assert evt.particles == evt2.particles
            assert evt.vertices == evt2.vertices
            assert evt.run_info == evt2.run_info
            assert evt == evt2
            n += 1
            break
        assert n == 1

        for evt2 in f:
            n += 1
        assert n == 1


def test_failed_read_file():
    with io.ReaderAscii("test_failed_read_file.dat") as f:
        with pytest.raises(IOError):
            f.read()

    n = 0
    with io.ReaderAscii("test_failed_read_file.dat") as f:
        with pytest.raises(IOError):
            for ev in f:
                n += 1
    assert n == 0


def test_failed_read_file_2():
    fn = str(Path(__file__).parent / "broken.dat")
    with io.ReaderAscii(fn) as f:
        with pytest.raises(IOError):
            f.read()

    n = 0
    with io.ReaderAscii(fn) as f:
        with pytest.raises(IOError):
            for ev in f:
                n += 1
    assert n == 0


def test_read_empty_stream():
    oss = stringstream()
    with io.ReaderAscii(oss) as f:
        ev = hep.GenEvent()
        success = f.read_event(ev)
        # reading empty stream is EOF
        assert success
        assert f.failed()

    with io.ReaderAscii(oss) as f:
        ev = f.read()
        # reading empty stream is EOF
        assert ev is None
        assert f.failed()


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
    filename = "test_read_write_file.dat"
    with hep.open(filename, "w", precision=3) as f:
        f.write(evt)

    with hep.open(filename) as f:
        for i, evt2 in enumerate(f):
            assert i == 0
            pass

    assert evt != evt2

    with hep.open(filename, "w") as f:
        f.write(evt)

    with hep.open(filename) as f:
        for i, evt3 in enumerate(f):
            assert i == 0
            pass

    assert evt == evt3

    os.unlink(filename)


def test_open_3(evt):  # noqa
    filename = Path("test_read_write_file.dat")

    with hep.open(filename, "w") as f:
        with pytest.raises(TypeError):
            f.write(None)

        with pytest.raises(TypeError):
            f.write("foo")

    class Foo:
        def __init__(self, evt):
            self.event = evt
            self.run_info = evt.run_info

        def to_hepmc3(self, event=None):
            if event is None:
                event = self.event
            assert event.run_info is self.run_info
            return event

    foo = Foo(evt)

    with hep.open(filename, "w") as f:
        f.write(foo)

    with hep.open(filename) as f:
        evt2 = f.read()

    assert evt == evt2

    filename.unlink()


def test_open_4():
    filename = "test_open_4.dat"

    with hep.open(filename, "w") as f:
        for i in range(3):
            ev = hep.GenEvent()
            ev.event_number = i + 1
            for k in range(i):
                ev.add_particle(hep.GenParticle((1, 2, 3, 4), 1, 1))
            f.write(ev)

    with hep.open(filename) as f:
        n = 0
        for ev in f:
            n += 1
            assert ev.event_number == n
            assert len(ev.particles) == n - 1
        assert n == 3

    # iterator is itself iterable
    with hep.open(filename) as f:
        fiter = iter(f)
        n = 0
        for ev in fiter:
            n += 1
        assert n == 3

    os.unlink(filename)


def test_open_5():
    fn = Path(__file__).parent / "pp.lhe"
    n = 0
    with hep.open(fn) as f:
        for ev in f:
            n += 1
    assert n == 1


def test_open_failures():
    fn = Path(__file__).parent / "pp.lhe"
    n = 0
    with hep.open(fn, format="hepmc3") as f:
        # ReaderAscii just skips unreadable parts of file
        for ev in f:
            n += 1
    assert n == 0

    with pytest.raises(ValueError, match="format"):
        with hep.open(fn, format="foo") as f:
            pass

    with pytest.raises(ValueError, match="format"):
        with hep.open("test.dat", "w", format="foo") as f:
            pass

    with pytest.raises(ValueError, match="mode"):
        with hep.open("test.dat", "x") as f:
            pass

    with pytest.raises(ValueError, match="mode"):
        with hep.open("test.dat", "rb") as f:
            pass


@pytest.mark.skipif(
    "CIBW" in os.environ,
    reason=(
        "does not work in cibuildwheel, "
        "although it works in a manually set-up docker"
    ),
)
def test_open_on_readonly_file():
    foo = Path("foo.dat")
    foo.touch(mode=0o000)  # not writeable

    with pytest.raises(IOError):
        with hep.open(foo, "w") as f:
            f.write(hep.GenEvent())

    foo.chmod(mode=0o666)
    foo.unlink()


def test_open_broken():
    fn = Path(__file__).parent / "broken.dat"
    n = 0
    with hep.open(fn) as f:
        with pytest.raises(IOError):
            for ev in f:
                n += 1
    assert n == 0


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
            t = list_type[int]
        elif k == "9":
            t = list_type[float]
        else:
            t = type(v)

        v2 = evt2.attributes[k].astype(t)

        assert v == v2
        # UnparsedAttribute is replaced with parsed Attribute
        v3 = evt2.attributes[k]
        assert v == v3

    os.unlink(filename)


@pytest.mark.parametrize("format", ["hepmc3", "hepmc2", "hepevt"])
def test_roundtrip(format):
    ev = hep.GenEvent()
    ev.run_info = hep.GenRunInfo()

    fn = "test_roundtrip.dat"

    with io.open(fn, "w", format=format) as f:
        f.write(ev)

    with io.open(fn, "r", format=format) as f:
        ev2 = f.read()

    os.unlink(fn)

    assert ev.particles == ev2.particles
    assert ev.vertices == ev2.vertices

    if format == "hepevt":
        pytest.xfail(
            reason="issue in HepMC3, see https://gitlab.cern.ch/hepmc/HepMC3/-/issues/21"
        )

    assert ev == ev2


@pytest.mark.parametrize("zip", ["gz", "bz2", "xz"])
def test_zip(zip):
    ev = hep.GenEvent()
    ev.run_info = hep.GenRunInfo()

    fn = f"test_zip.{zip}"

    with io.open(fn, "w") as f:
        f.write(ev)

    try:
        out = subp.check_output(["file", fn], text=True)
        assert "compressed" in out.lower()
        assert {"gz": "gzip", "bz2": "bzip2", "xz": "xz"}[zip] in out.lower()
    except FileNotFoundError:
        pass

    with io.open(fn, "r") as f:
        ev2 = f.read()

    os.unlink(fn)

    assert ev == ev2
