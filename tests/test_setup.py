import pyhepmc


def test_all():
    print(pyhepmc.__version__)

    assert pyhepmc.print_errors()
    assert pyhepmc.print_warnings()

    pyhepmc.set_print_errors(False)
    assert not pyhepmc.print_errors()
    assert pyhepmc.print_warnings()

    pyhepmc.set_print_warnings(False)
    assert not pyhepmc.print_errors()
    assert not pyhepmc.print_warnings()
