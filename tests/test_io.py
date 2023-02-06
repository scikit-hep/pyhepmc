import os
import pyhepmc as hep
import pyhepmc.io as io
import pytest
from test_basic import make_evt
from pyhepmc._core import stringstream, pyiostream
from io import BytesIO
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

# this only does something if pyhepmc is compiled in debug mode
hep.Setup.print_warnings = True


@pytest.fixture()
def evt():
    return make_evt()


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
            for evt in f:
                f2.write(evt)

    ev1 = []
    with gzip.open(fn2) as f:
        with pyiostream(f, 1000) as s:
            with io.ReaderAscii(s) as r:
                for evt in r:
                    ev1.append(evt)

    assert len(ev1) == 1

    ev2 = []
    with io.ReaderAscii(fn) as r:
        for evt in r:
            ev2.append(evt)

    assert ev1 == ev2

    os.unlink(fn2)


def test_pystream_3(evt):
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


@pytest.mark.parametrize("size", (100, 1))
def test_pystream_4(size):
    s = b"\r\n1\r\n\r\n22\r\n333\r\n"
    io = BytesIO(s)
    pio = pyiostream(io, size)
    assert pio.getline() == b""
    assert pio.getline() == b"1"
    assert pio.getline() == b""
    assert pio.getline() == b"22"
    assert pio.getline() == b"333"
    assert pio.getline() == b""
    assert pio.getline() == b""


def test_pystream_5():
    import sys

    io = sys.stdout.buffer
    with pyiostream(io, 100) as pio:
        pio.write(b"foo")


def test_read_event_write_event(evt):
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


def test_pythonic_read_write_from_stream(evt):
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
    with io.ReaderAscii("file_does_not_exist.dat") as f:
        evt = f.read()

    assert evt is None

    n = 0
    with io.ReaderAscii("file_does_not_exist.dat") as f:
        for ev in f:
            n += 1
    assert n == 0


def test_failed_read_file_2():
    fn = str(Path(__file__).parent / "broken.dat")
    with io.ReaderAscii(fn) as f:
        event = f.read()

    assert event is None

    n = 0
    with io.ReaderAscii(fn) as f:
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
def test_open_1(evt, format):
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


def test_open_2(evt):
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


def test_open_3(evt):
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
            for k in range(ev.event_number):
                ev.add_particle(hep.GenParticle((1, 2, 3, 4), 1, 1))
            f.write(ev)

    with hep.open(filename) as f:
        n = 0
        for ev in f:
            n += 1
            assert ev.event_number == n
            assert len(ev.particles) == n
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


def test_open_6(evt, capsys):
    import sys

    fn = "test_open_6.dat"

    with hep.open(fn, "w") as f:
        f.write(evt)

    with open(fn, "rb") as f:
        content = f.read().decode()

    with hep.open(sys.stdout, "w") as f:
        f.write(evt)

    c = capsys.readouterr().out
    assert c == content

    os.unlink(fn)


def test_open_7():
    fn = str(Path(__file__).parent / "sibyll21.dat")

    with open(fn, "r") as f:
        with hep.open(f, "r") as f2:
            evt = f2.read()

    assert len(evt.particles) == 23
    assert len(evt.vertices) == 7


def test_open_last_event_issue():
    fn = str(Path(__file__).parent / "last_event_issue.hepmc")

    n = 0
    with io.open(fn) as f:
        while True:
            event = f.read()
            if event is None:
                break
            n += 1
            assert len(event.particles) > 0

    assert n == 1


def test_ReaderAscii_last_event_issue():
    fn = str(Path(__file__).parent / "last_event_issue.hepmc")

    n = 0
    evt = hep.GenEvent()
    with io.ReaderAscii(fn) as f:
        while not f.failed():
            if f.read_event(evt):
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


def test_open_standalone(evt):  # noqa
    filename = "test_open_standalone.dat"

    f = hep.open(filename, "w")
    f.write(evt)
    f.flush()
    f.close()

    f2 = hep.open(filename)
    evt2 = f2.read()
    f2.close()

    assert evt2 == evt

    f3 = hep.io.HepMCFile(filename)
    for evt3 in f3:
        pass
    f3.close()

    assert evt3 == evt

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
def test_roundtrip(evt, format):
    fn = "test_roundtrip.dat"

    if format != "hepmc3":
        # only HepMC3 support non-empty GenRunInfo
        evt.run_info = hep.GenRunInfo()
    # HepMC3 adds "0" to weight_names upon reading event if weight_names is empty
    evt.run_info.weight_names = ["0"]

    with io.open(fn, "w", format=format) as f:
        f.write(evt)

    with io.open(fn, "r", format=format) as f:
        evt2 = f.read()

    os.unlink(fn)

    assert evt == evt2


@pytest.mark.parametrize("zip", ["gz", "bz2", "xz"])
def test_zip(evt, zip):
    fn = f"test_zip.{zip}"
    # HepMC3 adds "0" to weight_names upon reading event if weight_names is empty
    evt.run_info.weight_names = ["0"]

    with io.open(fn, "w") as f:
        f.write(evt)

    try:
        out = subp.check_output(["file", fn], text=True)
        assert "compressed" in out.lower()
        assert {"gz": "gzip", "bz2": "bzip2", "xz": "xz"}[zip] in out.lower()
    except FileNotFoundError:
        pass

    with io.open(fn, "r") as f:
        evt2 = f.read()

    os.unlink(fn)

    assert evt == evt2
