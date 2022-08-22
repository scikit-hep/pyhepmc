from ._core import (
    GenEvent,
    ReaderAscii,
    ReaderAsciiHepMC2,
    ReaderLHEF,
    ReaderHEPEVT,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
)
from pathlib import PurePath
import typing as _tp


class _Iter:
    def __init__(self, parent):
        self.parent = parent

    def __next__(self):
        evt = self.parent.read()
        if evt is None:
            raise StopIteration
        return evt

    next = __next__


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


# Wrapper for Writer, to be used by `open`
class _WrappedWriter:
    def __init__(self, filename, precision, Writer):
        self._writer = (filename, precision, Writer)

    def write(self, event):
        if not isinstance(event, GenEvent):
            if hasattr(event, "to_hepmc3"):
                event = event.to_hepmc3()
            else:
                raise TypeError(
                    "event must be an instance of GenEvent or "
                    "convertible to it by providing a to_hepmc3() method"
                )
        if isinstance(self._writer, tuple):
            # first call
            filename, precision, Writer = self._writer
            if Writer is WriterHEPEVT:
                self._writer = Writer(filename)
            else:
                self._writer = Writer(filename, event.run_info)
            if precision is not None and hasattr(self._writer, "precision"):
                self._writer.precision = precision
        self._writer.write_event(event)

    def close(self):
        if not isinstance(self._writer, tuple):
            self._writer.close()

    __enter__ = _enter
    __exit__ = _exit


def pyhepmc_open(
    filename: _tp.Union[str, PurePath],
    mode: str = "r",
    precision: int = None,
    format: str = None,
):
    """
    Open HepMC files for reading or writing.

    Parameters
    ----------
    filename : str or Path
        Filename to open for reading or writing. When writing to existing files,
        the contents are replaced.
    mode : str, optional
        Must be either "r" (default) or "w", to indicate whether to open for reading
        or writing.
    precision : int or None, optional
        How many digits of precision to use when writing to a file. Can be used to
        improve the compression rate.
    format : str or None, optional
        Which format to use for reading or writing. If None (default), autodetect
        format when reading (this is fast and thus safe to use), and use the latest
        HepMC3 format when writing. Allowed values: "HepMC3", "HepMC2", "LHEF",
        "HEPEVT". "LHEF" is not supported for writing.
    """
    if mode == "r":
        if format is None:
            # auto-detect
            with open(filename, "r") as f:
                header = f.read(256)
            if "HepMC::Asciiv3" in header:
                Reader = ReaderAscii
            elif "HepMC::IO_GenEvent" in header:
                Reader = ReaderAsciiHepMC2
            elif "<LesHouchesEvents" in header:
                Reader = ReaderLHEF
            else:
                # this one has no header
                Reader = ReaderHEPEVT
        else:
            Reader = {
                "hepmc3": ReaderAscii,
                "hepmc2": ReaderAsciiHepMC2,
                "lhef": ReaderLHEF,
                "hepevt": ReaderHEPEVT,
            }.get(format.lower(), None)
            if Reader is None:
                raise ValueError(f"format {format} not recognized for reading")
        return Reader(str(filename))
    elif mode == "w":
        if format is None:
            Writer = WriterAscii
        else:
            Writer = {
                "hepmc3": WriterAscii,
                "hepmc2": WriterAsciiHepMC2,
                "hepevt": WriterHEPEVT,
            }.get(format.lower(), None)
            if Writer is None:
                raise ValueError(f"format {format} not recognized for writing")
        return _WrappedWriter(str(filename), precision, Writer)
    raise ValueError("mode must be r or w")
