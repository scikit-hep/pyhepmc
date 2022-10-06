import pyhepmc as hep
import numpy as np
from pathlib import Path
import pytest

cdir = Path(__file__).parent


def test_parents_range_exceeding_particle_range():
    px = py = pz = en = m = np.linspace(0, 1, 6)
    pid = np.arange(6) + 1
    sta = np.zeros(6, dtype=np.int32)

    # invalid parents overlap
    parents = [(0, 0), (1, 1), (2, 0), (3, 5), (4, 10), (3, 5)]

    hev = hep.GenEvent()
    with pytest.raises(RuntimeError):
        hev.from_hepevt(0, px, py, pz, en, m, pid, sta, parents)
