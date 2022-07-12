import os
import pyhepmc as hep
import pytest
from test_basic import evt  # noqa


def test_read_write(evt):  # noqa
    oss = hep.stringstream()
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
    oss = hep.stringstream()
    with hep.WriterAscii(oss) as f:
        f.write(evt)

    with hep.ReaderAscii(oss) as f:
        for i, evt2 in enumerate(f):
            assert i == 0
            assert evt.particles == evt2.particles
            assert evt.vertices == evt2.vertices
            assert evt == evt2


def test_failed_read_file():
    with hep.ReaderAscii("test_failed_read_file.dat") as f:
        assert f.read() is None


def test_read_empty_stream(evt):  # noqa
    oss = hep.stringstream()
    with hep.ReaderAscii(oss) as f:
        evt = hep.GenEvent()
        ok = f.read_event(evt)
        assert ok is True  # reading empty stream is ok in HepMC


def test_open(evt):  # noqa
    with hep.open("test_read_write_file.dat", "w") as f:
        f.write(evt)

    with hep.open("test_read_write_file.dat") as f:
        evt2 = f.read()

    assert evt == evt2

    os.unlink("test_read_write_file.dat")


@pytest.mark.parametrize(
    "writer", (hep.WriterAscii, hep.WriterAsciiHepMC2, hep.WriterHEPEVT)
)
def test_open_with_writer(evt, writer):  # noqa
    filename = f"test_open_{writer.__name__}.dat"
    with writer(filename) as f:
        f.write(evt)

    with hep.open(filename) as f:
        evt2 = f.read()

        # ReaderHEPEVT adds arbitrary weight to evt2, so we must add that to evt as well
        if isinstance(writer, hep.WriterHEPEVT):
            evt.run_info = hep.GenRunInfo(weight_names=["0"])
            evt.weights = [1]
        assert evt.run_info == evt2.run_info
        assert evt == evt2

    os.unlink(filename)
