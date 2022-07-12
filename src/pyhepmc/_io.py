from ._core import (
    GenEvent,
    ReaderAscii,
    ReaderAsciiHepMC2,
    ReaderLHEF,
    ReaderHEPEVT,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
    GenRunInfo,
)


class _Iter:
    def __init__(self, parent):
        self.parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        evt = self.parent.read()
        if evt is None:
            raise StopIteration
        return evt


_Iter.next = _Iter.__next__


def _enter(self):
    return self


def _exit(self, type, value, tb):
    self.close()
    return False


def _iter(self):
    return _Iter(self)


def _read(self):
    evt = GenEvent()
    ok = self.read_event(evt)
    return evt if ok and not self.failed() else None


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


def pyhepmc_open(filename, mode="r", precision=None):
    if mode == "r":
        with open(filename, "r") as f:
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
