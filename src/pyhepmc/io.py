"""
HepMC3 IO classes.

This module contains various Reader and Writer classes, which have
pythonic interfaces. They act as context managers and close the file
automatically. The Readers can be iterated over and yield events.

The :func:`open` function is even easier to use. It can read any
supported file and will auto-detect the format. It can be used for
reading and writing.
"""
from ._core import (
    GenEvent,
    ReaderAscii,
    ReaderAsciiHepMC2,
    ReaderLHEF,
    ReaderHEPEVT,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
    UnparsedAttribute,
)
from pathlib import PurePath
import typing as _tp

__all__ = [
    "open",
    "ReaderAscii",
    "ReaderAsciiHepMC2",
    "ReaderLHEF",
    "ReaderHEPEVT",
    "WriterAscii",
    "WriterAsciiHepMC2",
    "WriterHEPEVT",
    "UnparsedAttribute",
]

_open = open


class _Iter:
    def __init__(self, parent: _tp.Any):
        self.parent = parent

    def __next__(self) -> GenEvent:
        evt = self.parent.read()
        if evt is None:
            raise StopIteration
        return evt

    def __iter__(self) -> "_Iter":
        return self

    next = __next__


def _enter(self: _Iter) -> _Iter:
    return self


def _exit(self: _tp.Any, type: Exception, value: str, tb: _tp.Any) -> bool:
    self.close()
    return False


def _iter(self: _tp.Any) -> _Iter:
    return _Iter(self)


def _read(self: _tp.Any) -> _tp.Union[GenEvent, None]:
    evt = GenEvent()
    success = self.read_event(evt)
    if self.failed():  # usually EOF
        return None
    return evt if success else None


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

_Filename = _tp.Union[str, PurePath]


class _WrappedWriter:
    # Wrapper for Writer, to be used by `open`

    def __init__(
        self, filename: _Filename, precision: _tp.Optional[int], Writer: _tp.Any
    ):
        self._writer: _tp.Any = None
        self._init = (filename, precision, Writer)

    @staticmethod
    def _maybe_convert(event: _tp.Any) -> GenEvent:
        if isinstance(event, GenEvent):
            return event
        if hasattr(event, "to_hepmc3"):
            return event.to_hepmc3()
        raise TypeError(
            "event must be an instance of GenEvent or "
            "convertible to it by providing a to_hepmc3() method"
        )

    def write(self, event: _tp.Any) -> None:
        evt = self._maybe_convert(event)

        if self._writer is None:
            # first call
            filename, precision, Writer = self._init
            if Writer is WriterHEPEVT:
                self._writer = Writer(filename)
            else:
                self._writer = Writer(filename, evt.run_info)
            if precision is not None and hasattr(self._writer, "precision"):
                self._writer.precision = precision

        self._writer.write_event(evt)
        if self._writer.failed():
            raise IOError("writing GenEvent failed")

    def close(self) -> None:
        if self._writer is not None:
            self._writer.close()

    __enter__ = _enter
    __exit__ = _exit


def open(
    filename: _Filename,
    mode: str = "r",
    precision: int = None,
    format: str = None,
) -> _tp.Any:
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

    Raises
    ------
    IOError if reading or writing fails.
    """
    if mode == "r":
        if format is None:
            # auto-detect
            with _open(filename, "r") as f:
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
