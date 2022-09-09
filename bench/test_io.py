import pyhepmc
from pyhepmc.io import ReaderAscii
from pyhepmc._core import pyiostream
from pathlib import Path


fn = str(Path(__file__).parent.parent / "tests" / "pythia6.dat")

with pyhepmc.open(fn) as f:
    evt = f.read()

with pyhepmc.open("bench.dat", "w") as f:
    for _ in range(4000):
        f.write(evt)


def test_ReaderAscii(benchmark):
    def run():
        with ReaderAscii("bench.dat") as r:
            while True:
                evt = r.read()
                if evt is None:
                    break

    benchmark(run)


def test_ReaderAscii_pyiostream(benchmark):
    def run():
        with open("bench.dat", "rb") as f:
            pis = pyiostream(f, 4096)
            with ReaderAscii(pis) as r:
                while True:
                    evt = r.read()
                    if evt is None:
                        break

    benchmark(run)
