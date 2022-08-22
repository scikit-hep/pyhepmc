from ._core import (  # noqa
    GenEvent,
    Units,
    GenVertex,
    GenParticle,
    GenEvent,
    GenHeavyIon,
    FourVector,
    GenRunInfo,
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
from ._io import (  # noqa
    ReaderAscii,
    ReaderAsciiHepMC2,
    ReaderLHEF,
    ReaderHEPEVT,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
    pyhepmc_open as open,
)
from ._version import version as __version__  # noqa


def _GenEvent_repr_html(self):
    from .view import to_dot

    g = to_dot(self)
    return g._repr_image_svg_xml()


GenEvent._repr_html_ = _GenEvent_repr_html
