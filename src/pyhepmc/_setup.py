from pyhepmc._core import (
    _Setup_print_errors,
    _Setup_set_print_errors,
    _Setup_print_warnings,
    _Setup_set_print_warnings,
    _Setup_debug_level,
    _Setup_set_debug_level,
)
from typing import Any


class _SetupMeta(type):
    @property
    def print_errors(cls) -> bool:
        """Whether to print errors or not."""
        return _Setup_print_errors()  # type:ignore

    @property
    def print_warnings(cls) -> bool:
        """Whether to print warnings or not."""
        return _Setup_print_warnings()  # type:ignore

    @property
    def debug_level(cls) -> int:
        """Access debug level."""
        return _Setup_debug_level()  # type:ignore

    def __setattr__(self, name: str, value: Any) -> None:
        attr = {
            "print_errors": _Setup_set_print_errors,
            "print_warnings": _Setup_set_print_warnings,
            "debug_level": _Setup_set_debug_level,
        }
        fn = attr.get(name, None)
        if fn is None:
            raise AttributeError
        fn(value)


class Setup(metaclass=_SetupMeta):
    """
    Imitates the Setup namespace.

    You can directly read and write to the attributes of this class
    without creating an instance. They manipulate the corresponding
    global values in the HepMC3 C++ library.
    """

    __slots__ = ("print_errors", "print_warnings", "debug_level")
