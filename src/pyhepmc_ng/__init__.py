from ._bindings import *
from ._io import _enter, _exit, _iter, _read
from ._version import version as __version__
import ctypes


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


def fill_genevent_from_hepevent_ptr(evt, ptr_as_int, max_size,
                                    int_type=ctypes.c_int,
                                    float_type=ctypes.c_double,
                                    hep_status_decoder=None,
                                    momentum_unit = 1,
                                    length_unit = 1):
    # struct HEPEVT                      // Fortran common block HEPEVT
    # {
    #     int        nevhep;             // Event number
    #     int        nhep;               // Number of entries in the event
    #     int        isthep[NMXHEP];     // Status code
    #     int        idhep [NMXHEP];     // PDG ID
    #     int        jmohep[NMXHEP][2];  // Idx of first and last mother
    #     int        jdahep[NMXHEP][2];  // Idx of first and last daughter
    #     momentum_t phep  [NMXHEP][5];  // Momentum: px, py, pz, e, m
    #     momentum_t vhep  [NMXHEP][4];  // Vertex: x, y, z, t
    # };

    IntArray = int_type * max_size
    Int2 = int_type * 2
    Int2Array = Int2 * max_size
    Float4 = float_type * 4
    Float5 = float_type * 5
    Float4Array = Float4 * max_size
    Float5Array = Float5 * max_size

    class HEPEVT(ctypes.Structure):
        _fields_ = (
                ("event_number", int_type),
                ("nentries", int_type),
                ("status", IntArray),
                ("pid", IntArray),
                ("parents", Int2Array),
                ("children", Int2Array),
                ("pm", Float5Array),
                ("v", Float4Array)
            )

    h = ctypes.cast(ptr_as_int, ctypes.POINTER(HEPEVT))[0]

    event_number = h.event_number
    n = h.nentries

    import numpy as np

    status = np.asarray(h.status)[:n]
    pm = np.asarray(h.pm)

    if hep_status_decoder is None:
        particle_status = status
        vertex_status = np.zeros_like(status)
    else:
        particle_status, vertex_status = hep_status_decoder(status)

    fill_genevent_from_hepevt(evt,
                              event_number,
                              pm[:n,:4],
                              pm[:n,4],
                              h.v[:n],
                              h.pid[:n],
                              h.parents[:n],
                              h.children[:n],
                              particle_status,
                              vertex_status,
                              momentum_unit,
                              length_unit)
    return evt
