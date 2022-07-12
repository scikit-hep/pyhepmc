import sys
import os
from pathlib import Path

module_dir = Path(__file__).parent
print(module_dir)
for p in module_dir.glob("*"):
    print(p)
# windows only loads dlls from "trusted" locations
if sys.platform.startswith("win"):
    os.add_dll_directory(module_dir)

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
from ._version import version as __version__  # noqa
