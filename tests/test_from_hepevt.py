import pyhepmc as hep
import numpy as np
import pytest


def test_no_vertex_info():
    px = py = pz = en = m = np.linspace(0, 1, 4)

    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    parents = [(0, 0), (1, 1), (0, 0), (0, 0)]
    hev = hep.GenEvent()
    hev.from_hepevt(0, px, py, pz, en, m, pid, sta, parents)
    assert len(hev.vertices) == 1
    assert len(hev.particles) == 4


def test_parents_range_exceeding_particle_range():
    px = py = pz = en = m = np.linspace(0, 1, 6)
    pid = np.arange(6) + 1
    sta = np.zeros(6, dtype=np.int32)
    parents = [(0, 0), (1, 1), (2, 0), (3, 5), (4, 10), (3, 5)]
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(0, px, py, pz, en, m, pid, sta, parents)


def test_invalid_length_of_parents():
    px = py = pz = en = m = np.linspace(0, 1, 3)
    pid = np.arange(3) + 1
    sta = np.zeros(3, dtype=np.int32)
    parents = [(0, 0), (1, 2)]
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(0, px, py, pz, en, m, pid, sta, parents)


def test_inverted_parents_range():
    px = py = pz = en = m = vx = vy = vz = vt = np.linspace(0, 1, 4)
    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    # inverted range is not an error (2, 1) will be converted to (1, 2)
    parents = [(0, 0), (2, 1), (3, 3), (3, 3)]
    hev = hep.GenEvent()
    hev.from_hepevt(0, px, py, pz, en, m, pid, sta, parents)
    expected = [[0, 1], [2]]
    got = [[p.id - 1 for p in v.particles_in] for v in hev.vertices]
    assert expected == got


@pytest.mark.parametrize("bad", ([-4, 1], [1, -4]))
def test_negative_parents_range(bad):
    px = py = pz = en = m = vx = vy = vz = vt = np.linspace(0, 1, 4)
    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    # inverted range is not an error (2, 1) will be converted to (1, 2)
    parents = [(0, 0), bad, (3, 3), (3, 3)]
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(0, px, py, pz, en, m, pid, sta, parents)
