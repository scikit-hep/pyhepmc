from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from test_basic import make_evt

import pyhepmc as hep

N_THREADS = 8


@pytest.mark.parametrize("format", ("hepmc3", "hepmc2", "hepevt"))
def test_independent_objects_in_threads(tmp_path, format):
    barrier = Barrier(N_THREADS)

    def work(i):
        evt = make_evt()
        evt.event_number = i
        fn = tmp_path / f"event_{i}.dat"
        barrier.wait()
        for _ in range(20):
            with hep.open(fn, "w", format=format) as f:
                f.write(evt)
            with hep.open(fn, format=format) as f:
                evt2 = f.read()
            assert evt2.event_number == i
            assert len(evt2.particles) == len(evt.particles)
            assert len(evt2.vertices) == len(evt.vertices)
        return i

    with ThreadPoolExecutor(N_THREADS) as ex:
        assert sorted(ex.map(work, range(N_THREADS))) == list(range(N_THREADS))
