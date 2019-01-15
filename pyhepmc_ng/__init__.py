from . cpp import *
import ctypes
import numpy as np


class WriterWrapper:
    def __init__(self, filename, precision=None):
        self._handle = (filename, precision)

    def write(self, object):
        if isinstance(self._handle, WriterAscii):
            self._handle.write(object)
            return
        filename, precision = self._handle  
        if isinstance(object, GenRunInfo):          
            self._handle = WriterAscii(filename, object)
            if precision is not None:
                self._handle.precision = precision
            self._handle.write_run_info()
        else:
            self._handle = WriterAscii(filename)
            if precision is not None:
                self._handle.precision = precision
            self.write(object)

    def close(self):
        self._handle.close()

    def __enter__(self):
        return self
        
    def __exit__(self, type, value, tb):
        self.close()
        return False


def open(filename, mode="r", precision=None):
    if mode == "r":
        return ReaderAscii(filename)
    elif mode == "w":
        return WriterWrapper(filename, precision)


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