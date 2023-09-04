import pyhepmc as hep
import numpy as np
import pytest


@pytest.mark.parametrize("fortran", (True, False))
def test_no_vertex_info(fortran):
    px = py = pz = en = m = np.linspace(0, 1, 4)

    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    # fortran style
    parents = [(0, -1), (1, 1), (0, 0), (0, 0)]
    if not fortran:
        parents = np.subtract(parents, 1)
    hev = hep.GenEvent()
    hev.from_hepevt(0, px, py, pz, en, m, pid, sta, parents, fortran=fortran)
    assert len(hev.vertices) == 1
    assert len(hev.particles) == 4


@pytest.mark.parametrize("fortran", (True, False))
def test_parents_range_exceeding_particle_range(fortran):
    px = py = pz = en = m = np.linspace(0, 1, 6)
    pid = np.arange(6) + 1
    sta = np.zeros(6, dtype=np.int32)
    # fortran style
    parents = [(0, 0), (1, 1), (2, 0), (3, 5), (4, 10), (3, 5)]
    if not fortran:
        parents = np.subtract(parents, 1)
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(
            0, px, py, pz, en, m, pid, sta, parents, fortran=fortran
        )


@pytest.mark.parametrize("fortran", (True, False))
def test_invalid_length_of_parents(fortran):
    px = py = pz = en = m = np.linspace(0, 1, 3)
    pid = np.arange(3) + 1
    sta = np.zeros(3, dtype=np.int32)
    # fortran style
    parents = [(0, 0), (1, 2)]
    if not fortran:
        parents = np.subtract(parents, 1)
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(
            0, px, py, pz, en, m, pid, sta, parents, fortran=fortran
        )


@pytest.mark.parametrize("fortran", (True, False))
def test_inverted_parents_range(fortran):
    px = py = pz = en = m = np.linspace(0, 1, 4)
    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    # inverted range is not an error (2, 1) will be converted to (1, 2)
    # fortran style
    parents = [(0, 0), (2, 1), (3, 3), (3, 3)]
    if not fortran:
        parents = np.subtract(parents, 1)
    hev = hep.GenEvent()
    hev.from_hepevt(0, px, py, pz, en, m, pid, sta, parents, fortran=fortran)
    expected = [[0, 1], [2]]
    got = [[p.id - 1 for p in v.particles_in] for v in hev.vertices]
    assert expected == got


@pytest.mark.parametrize("fortran", (True, False))
@pytest.mark.parametrize("bad", ([-4, 1], [1, -4]))
def test_negative_parents_range(bad, fortran):
    px = py = pz = en = m = np.linspace(0, 1, 4)
    pid = np.arange(4) + 1
    sta = np.zeros(4, dtype=np.int32)
    # inverted range is not an error (2, 1) will be converted to (1, 2)
    # fortran style
    parents = [(0, 0), bad, (3, 3), (3, 3)]
    if not fortran:
        parents = np.subtract(parents, 1)
    with pytest.raises(RuntimeError):
        hep.GenEvent().from_hepevt(
            0, px, py, pz, en, m, pid, sta, parents, fortran=fortran
        )
