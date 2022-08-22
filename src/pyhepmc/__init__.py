from ._core import (  # noqa
    Units,
    FourVector,
    GenEvent,
    GenParticle,
    GenVertex,
    GenHeavyIon,
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

try:
    from .view import to_dot

    def _genevent_repr_html(self):
        g = to_dot(self)
        return g._repr_image_svg_xml()

    GenEvent._repr_html_ = _genevent_repr_html
except ModuleNotFoundError:
    pass
