try:
    # make pyhepmc importable even if it is not installed yet for setup.cfg
    from ._core import *  # noqa
    from ._io import (  # noqa
        ReaderAscii,
        ReaderAsciiHepMC2,
        ReaderLHEF,
        ReaderHEPEVT,
        WriterAscii,
        WriterAsciiHepMC2,
        WriterHEPEVT,
        fill_genevent_from_hepevt,
        pyhepmc_open as open,
    )
except ImportError:  # pragma: no cover
    pass  # pragma: no cover

from ._version import version as __version__  # noqa
