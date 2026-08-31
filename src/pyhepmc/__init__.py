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

- ``ReaderMT`` will not be implemented. If you want to use multi-threaded IO,
  it is better to use the high-level threading API of Python to achieve this.
  You can read the next GenEvent in a child thread from a file while you are
  processing the current event in the main thread.

"""

from importlib.metadata import version
from typing import Any

from pyhepmc import _attributes
from pyhepmc._core import (
    FourVector,
    GenCrossSection,
    GenEvent,
    GenEventData,
    GenHeavyIon,
    GenParticle,
    GenPdfInfo,
    GenRunInfo,
    GenVertex,
    HEPEUPAttribute,
    HEPRUPAttribute,
    Units,
    content,
    delta_eta,
    delta_phi,
    delta_r2_eta,
    delta_r2_rap,
    delta_r_eta,
    delta_r_rap,
    delta_rap,
    equal_particle_sets,
    equal_vertex_sets,
    listing,
)
from pyhepmc._setup import Setup
from pyhepmc.io import open as open
from pyhepmc.view import to_dot

__version__ = version("pyhepmc")

__all__ = (
    "FourVector",
    "GenCrossSection",
    "GenEvent",
    "GenEventData",
    "GenHeavyIon",
    "GenParticle",
    "GenParticleData",
    "GenPdfInfo",
    "GenRunInfo",
    "GenVertex",
    "GenVertexData",
    "HEPEUPAttribute",
    "HEPRUPAttribute",
    "Setup",
    "Units",
    "content",
    "delta_eta",
    "delta_phi",
    "delta_r2_eta",
    "delta_r2_rap",
    "delta_r_eta",
    "delta_r_rap",
    "delta_rap",
    "equal_particle_sets",
    "equal_vertex_sets",
    "listing",
    "open",
)

_attributes.install()

GenEvent._repr_html_ = lambda self: to_dot(self)._repr_html_()


def __getattr__(name: str) -> Any:
    import warnings

    from . import io

    if name in dir(io):
        warnings.warn(
            f"importing {name} from pyhepmc is deprecated, "
            "please import from pyhepmc.io",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return getattr(io, name)

    raise AttributeError
