import pyhepmc


def test_all():
    assert pyhepmc.Setup.print_errors
    assert pyhepmc.Setup.print_warnings
    assert pyhepmc.Setup.debug_level == 5

    pyhepmc.Setup.print_errors = False
    assert not pyhepmc.Setup.print_errors
    assert pyhepmc.Setup.print_warnings

    pyhepmc.Setup.print_warnings = False
    assert not pyhepmc.Setup.print_errors
    assert not pyhepmc.Setup.print_warnings

    pyhepmc.Setup.debug_level = 10
    assert pyhepmc.Setup.debug_level == 10
