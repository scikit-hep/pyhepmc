from ._bindings import *
from ._io import _enter, _exit, _iter, _read
from ._version import version as __version__
import ctypes
import warnings
from numpy import VisibleDeprecationWarning

warnings.warn(
    """
The pyhepmc-ng package is continued as the package pyhepmc.
Please install pyhepmc, pyhepmc-ng is no longer updated.""",
    VisibleDeprecationWarning,
)

# save original open because it is overwritten
builtin_open = open


# add pythonic interface to IO classes
ReaderAscii.__enter__ = _enter
ReaderAscii.__exit__ = _exit
ReaderAscii.__iter__ = _iter
ReaderAscii.read = _read

ReaderAsciiHepMC2.__enter__ = _enter
ReaderAsciiHepMC2.__exit__ = _exit
ReaderAsciiHepMC2.__iter__ = _iter
ReaderAsciiHepMC2.read = _read

ReaderLHEF.__enter__ = _enter
ReaderLHEF.__exit__ = _exit
ReaderLHEF.__iter__ = _iter
ReaderLHEF.read = _read

ReaderHEPEVT.__enter__ = _enter
ReaderHEPEVT.__exit__ = _exit
ReaderHEPEVT.__iter__ = _iter
ReaderHEPEVT.read = _read

WriterAscii.__enter__ = _enter
WriterAscii.__exit__ = _exit
WriterAscii.write = WriterAscii.write_event

WriterAsciiHepMC2.__enter__ = _enter
WriterAsciiHepMC2.__exit__ = _exit
WriterAsciiHepMC2.write = WriterAsciiHepMC2.write_event

WriterHEPEVT.__enter__ = _enter
WriterHEPEVT.__exit__ = _exit
WriterHEPEVT.write = WriterHEPEVT.write_event


# pythonic wrapper for AsciiWriter, to be used by `open`
class WrappedAsciiWriter:
    def __init__(self, filename, precision=None):
        self._writer = (filename, precision)

    def write(self, object):
        if isinstance(self._writer, tuple):
            filename, precision = self._writer
            if isinstance(object, GenRunInfo):
                self._writer = self.WriterAscii(filename, object)
                if precision is not None:
                    self._writer.precision = precision
                self._writer.write_run_info()
                return
            else:
                self._writer = WriterAscii(filename)
                if precision is not None:
                    self._writer.precision = precision

        if isinstance(object, GenRunInfo):
            raise RuntimeError("GenRunInfo must be written first")

        self._writer.write_event(object)

    def close(self):
        self._writer.close()

    __enter__ = _enter
    __exit__ = _exit


def open(filename, mode="r", precision=None):
    if mode == "r":
        with builtin_open(filename, "r") as f:
            header = f.read(256)
        if "HepMC::Asciiv3" in header:
            return ReaderAscii(filename)
        if "HepMC::IO_GenEvent" in header:
            return ReaderAsciiHepMC2(filename)
        if "<LesHouchesEvents" in header:
            return ReaderLHEF(filename)
        return ReaderHEPEVT(filename)

    elif mode == "w":
        return WrappedAsciiWriter(filename, precision)
    raise ValueError("mode must be r or w")


_hepevt_buffer = HEPEVT()


def fill_genevent_from_hepevt(evt, **kwargs):
    """
    Fills GenEvent from HEPEVT data.

    Parameters
    ----------
    event_number : int
        Current Event Number. Starts with 1.
    p : array(float) N x 4
        Array of 4-vectors (px, py, py, e).
    m : array(float) N
        Array of generated masses (virtual masses).
    v : array(float) N x 4
        Array of 4-vectors (x, y, z, t).
    pid : array(int) N
        Array of PDG IDs.
    parents : array(int) N x 2
        Array of (parent first index, parent last index). Indices start at 1.
    children : array(int) N x 2 (optional)
        Array of (child first index, child last index). Indices start at 1. May be none.
    status : array(int) N
        Array of particle status. See HEPMC3 docs for definition.
    momentum_scaling : float (optional)
        Momentum coordinates are stored in units of this number.
    vertex_scaling : float (optional)
        Vertex coordinates are stored in units of this number.

    Notes
    -----
    The current implementation copies the input into an internal buffer. This is not as efficient as possible, but currently the only way to use the HepMC3 C++ code with input data which does not have exactly the memory layout of the HEPEVT struct defined in HepMC3/HEPEVT_Wrapper.h.

    Calling this function is not thread-safe.
    """
    event_number = kwargs["event_number"]
    p = kwargs["p"]
    m = kwargs["m"]
    v = kwargs["v"]
    pid = kwargs["pid"]
    parents = kwargs["parents"]
    children = kwargs.get("children", 0)
    status = kwargs["status"]
    momentum_scaling = kwargs.get("momentum_scaling", 1.0)
    vertex_scaling = kwargs.get("vertex_scaling", 1.0)

    global _hepevt_buffer
    n = pid.shape[0]
    if n > _hepevt_buffer.max_size:
        raise ValueError(
            (
                "Number of particles in event (%i) exceeds HepMC3 buffer size (%i).\n"
                'Change the line `define_macros={"HEPMC3_HEPEVT_NMXHEP": 50000}` in setup.py\n'
                "to a larger value and (re)compile pyhepmc_ng from scratch."
            )
            % (n, _hepevt_buffer.max_size)
        )
    _hepevt_buffer.event_number = event_number
    _hepevt_buffer.nentries = n
    _hepevt_buffer.pm()[:n, :4] = p / momentum_scaling
    _hepevt_buffer.pm()[:n, 4] = m / momentum_scaling
    _hepevt_buffer.v()[:n] = v / vertex_scaling
    _hepevt_buffer.pid()[:n] = pid
    _hepevt_buffer.parents()[:n] = parents
    _hepevt_buffer.children()[:n] = children
    _hepevt_buffer.status()[:n] = status

    evt.clear()
    _hepevt_buffer.to_genevent(evt)
