"""
pyhepmc: a pythonic and Jupyter-friendly Python API for HepMC3

Differences between HepMC3 C++ and pyhepmc
------------------------------------------

- The pyhepmc API uses properties where the C++ API uses setters/getters
  (where possible).
- Sequences with matching types and lengths are implicitly
  convertible to :class:`FourVector` und :class:`ToolInfo`.
- In addition to the C++ Reader/Writer classes, we offer an easy to use
  :func:`open`. It can read any supported format and writes in HepMC3 format.
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
- API marked as deprecated in HepMC3 is not available in Python.
- pyhepmc offers event visualization and renders in Jupyter notebooks if all
  required extra packages are installed, see :func:`pyhepmc.view.to_dot`.

Missing functionality
---------------------

- Not yet implemented: ``GenParticleData``, ``GenVertexData``, ``ReaderMT``,
  ``ReaderGZ``, ``Setup``, ``WriterGZ``. These will be added in the future.
"""
# flake8: F401
from ._core import (  # noqa: F401
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
    delta_phi,
    delta_eta,
    delta_r2_eta,
    delta_r_eta,
    delta_r2_rap,
    delta_r_rap,
    delta_rap,
)
from .io import open as open  # noqa: F401
from ._version import __version__ as __version__  # noqa: F401
import typing as _tp
from . import _attributes  # noqa

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
    "delta_phi",
    "delta_eta",
    "delta_r2_eta",
    "delta_r_eta",
    "delta_r2_rap",
    "delta_r_rap",
    "delta_rap",
    "open",
)

try:
    from .view import to_dot as _to_dot

    def _genevent_repr_html(self: GenEvent) -> _tp.Any:
        g = _to_dot(self)
        return g._repr_image_svg_xml()

    GenEvent._repr_html_ = _genevent_repr_html
except ModuleNotFoundError:
    pass


def __getattr__(name: str) -> _tp.Any:
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
