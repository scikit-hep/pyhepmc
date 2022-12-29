"""
pyhepmc is a pythonic and Jupyter-friendly Python API for HepMC3.

Differences between HepMC3 C++ and pyhepmc
------------------------------------------

- The pyhepmc API uses properties where the C++ API uses setters/getters
  (where possible).
- Sequences with matching types and lengths are implicitly
  convertible to :class:`FourVector` und :class:`ToolInfo`.
- In addition to the C++ Reader/Writer classes, we offer an easy to use
  :func:`open`. It can read and write any supported HepMC3 format,
  including compressed files (gzip, bzip2, lzma are supported).
- Attributes for :class:`GenRunInfo`, :class:`GenEvent`, :class:`GenParticle`,
  :class:`GenVertex` can be accessed via a dict-like view returned by the
  ``attributes`` property. The view automatically converts between native C++
  types to native Python types.
- The ``Print`` class is missing, but :func:`listing` and :func:`content`
  are present as free functions.
- The member functions ``delta_X`` of :class:`FourVector` are free functions
  with two arguments.
- ``HEPEVT_Wrapper`` and friends are missing, use :meth:`GenEvent.from_hepevt`
  instead.
- ``ReaderGZ`` and ``WriterGZ`` are missing, since :func:`open` offers this
  functionality.
- API marked as deprecated in HepMC3 is not available in Python.
- pyhepmc offers event visualization and renders in Jupyter notebooks if all
  required extra packages are installed, see :func:`pyhepmc.view.to_dot`.

Missing functionality
---------------------

- Not yet implemented: ``GenParticleData``, ``GenVertexData``, ``ReaderMT``.
  These will be added in the future.

"""
from sys import version_info
from pyhepmc._core import (
    Units,
    FourVector,
    GenEvent,
    GenParticle,
    GenVertex,
    GenHeavyIon,
    GenRunInfo,
    GenPdfInfo,
    GenCrossSection,
    HEPRUPAttribute,
    HEPEUPAttribute,
    equal_vertex_sets,
    equal_particle_sets,
    content,
    listing,
    _Setup_print_errors,
    _Setup_set_print_errors,
    _Setup_print_warnings,
    _Setup_set_print_warnings,
    _Setup_debug_level,
    _Setup_set_debug_level,
    delta_phi,
    delta_eta,
    delta_r2_eta,
    delta_r_eta,
    delta_r2_rap,
    delta_r_rap,
    delta_rap,
)
from pyhepmc.io import open as open  # noqa: F401
import pyhepmc._attributes  # noqa, keep this for its side effects
from typing import Any
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyhepmc")
except PackageNotFoundError:
    # package is not installed
    pass

__all__ = (
    "Units",
    "FourVector",
    "GenEvent",
    "GenParticle",
    "GenVertex",
    "GenHeavyIon",
    "GenRunInfo",
    "GenPdfInfo",
    "GenCrossSection",
    "HEPRUPAttribute",
    "HEPEUPAttribute",
    "equal_vertex_sets",
    "equal_particle_sets",
    "content",
    "listing",
    "Setup",
    "delta_phi",
    "delta_eta",
    "delta_r2_eta",
    "delta_r_eta",
    "delta_r2_rap",
    "delta_r_rap",
    "delta_rap",
    "open",
)


class _SetupMeta(type):
    @property
    def print_errors(cls) -> bool:
        "Whether to print errors or not."
        return _Setup_print_errors()  # type:ignore

    @property
    def print_warnings(cls) -> bool:
        "Whether to print warnings or not."
        return _Setup_print_warnings()  # type:ignore

    @property
    def debug_level(cls) -> int:
        "Access debug level."
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


try:
    from pyhepmc.view import to_dot

    def _genevent_repr_html(self: GenEvent) -> Any:
        g = to_dot(self)
        return g._repr_image_svg_xml()

    GenEvent._repr_html_ = _genevent_repr_html
except ModuleNotFoundError:  # pragma: no cover
    pass  # pragma: no cover


if version_info >= (3, 8):
    from typing import get_origin, get_args
else:

    def get_origin(pytype):  # type: ignore  # pragma: no cover
        if hasattr(pytype, "__origin__"):  # pragma: no cover
            return pytype.__origin__  # pragma: no cover
        return None  # pragma: no cover

    def get_args(pytype):  # type: ignore # pragma: no cover
        return pytype.__args__  # pragma: no cover


def __getattr__(name: str) -> Any:
    from . import io
    import warnings
    from numpy import VisibleDeprecationWarning

    if name in dir(io):
        warnings.warn(
            f"importing {name} from pyhepmc is deprecated, please import from pyhepmc.io",
            category=VisibleDeprecationWarning,
            stacklevel=2,
        )
        return getattr(io, name)

    raise AttributeError
