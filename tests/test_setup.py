import pyhepmc
from pyhepmc._core import _Setup_print_errors, _Setup_print_warnings, _Setup_debug_level
import pytest


def test_all():
    assert pyhepmc.Setup.print_errors
    assert pyhepmc.Setup.print_warnings
    assert pyhepmc.Setup.debug_level == 5

    pyhepmc.Setup.print_errors = False
    assert _Setup_print_errors() is False

    pyhepmc.Setup.print_warnings = False
    assert _Setup_print_warnings() is False

    pyhepmc.Setup.debug_level = 10
    assert _Setup_debug_level() == 10

    with pytest.raises(AttributeError):
        pyhepmc.Setup.foo = 1
