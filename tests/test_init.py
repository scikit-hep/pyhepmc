import pyhepmc
import pyhepmc._core as core


def test_init():
    core_names = set()

    for name in dir(core):
        if name.startswith("_"):
            continue
        core_names.add(name)

    core_names.remove("stringstream")

    names = set()
    for name in dir(pyhepmc):
        if name.startswith("_"):
            continue
        names.add(name)

    assert core_names - names == set()
