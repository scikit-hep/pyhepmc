import pyhepmc


def test_all():
    assert pyhepmc.print_errors()
    assert pyhepmc.print_warnings()

    pyhepmc.set_print_errors(False)
    assert not pyhepmc.print_errors()
    assert pyhepmc.print_warnings()

    pyhepmc.set_print_warnings(False)
    assert not pyhepmc.print_errors()
    assert not pyhepmc.print_warnings()

    assert pyhepmc.debug_level() == 5
    pyhepmc.set_debug_level(10)
    assert pyhepmc.debug_level() == 10
