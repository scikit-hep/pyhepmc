import pyhepmc
import pyhepmc.io
import pyhepmc._core as core


def test_init():
    core_names = set()

    for name in dir(core):
        if name.startswith("_"):
            continue
        core_names.add(name)

    core_names.remove("stringstream")
    core_names.remove("istream")
    core_names.remove("pyistream")
    core_names.remove("Attribute")
    core_names.remove("AttributesView")
    core_names.remove("Reader")
    core_names.remove("Writer")
    core_names.remove("RunInfoAttributesView")

    names = set()
    for name in dir(pyhepmc):
        if name.startswith("_"):
            continue
        names.add(name)
    for name in dir(pyhepmc.io):
        if name.startswith("_"):
            continue
        names.add(name)

    assert core_names - names == set()
