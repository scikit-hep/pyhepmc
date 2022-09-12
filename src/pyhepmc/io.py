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
    pyiostream,
)
import contextlib
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
        evt = GenEvent()
        success = self.parent.read_event(evt)
        if self.parent.failed():
            if success:  # indicates EOF
                raise StopIteration
            raise IOError("error reading event")
        return evt

    def __iter__(self) -> "_Iter":
        return self

    next = __next__


def _enter(self: _tp.Any) -> _tp.Any:
    return self


def _exit_close(self: _tp.Any, type: Exception, value: str, tb: _tp.Any) -> bool:
    self.close()
    return False


def _exit_flush(self: _tp.Any, type: Exception, value: str, tb: _tp.Any) -> bool:
    self.flush()
    return False


def _iter(self: _tp.Any) -> _Iter:
    return _Iter(self)


def _read(self: _tp.Any) -> _tp.Optional[GenEvent]:
    evt = GenEvent()
    success = self.read_event(evt)
    if self.failed():
        if success:  # indicates EOF
            return None
        raise IOError("error reading event")
    return evt if success else None


def _read_event_lhef_patch(self: _tp.Any, evt: GenEvent) -> bool:
    failed = ReaderLHEF_read_event(self, evt)
    if failed and self.failed():  # probably EOF
        return True
    return not failed


# add contextmanager interface to IO classes
ReaderAscii.__enter__ = _enter
ReaderAscii.__exit__ = _exit_close
ReaderAscii.__iter__ = _iter
ReaderAscii.read = _read

ReaderAsciiHepMC2.__enter__ = _enter
ReaderAsciiHepMC2.__exit__ = _exit_close
ReaderAsciiHepMC2.__iter__ = _iter
ReaderAsciiHepMC2.read = _read

ReaderLHEF.__enter__ = _enter
ReaderLHEF.__exit__ = _exit_close
ReaderLHEF.__iter__ = _iter
ReaderLHEF_read_event = ReaderLHEF.read_event
ReaderLHEF.read_event = _read_event_lhef_patch
ReaderLHEF.read = _read

ReaderHEPEVT.__enter__ = _enter
ReaderHEPEVT.__exit__ = _exit_close
ReaderHEPEVT.__iter__ = _iter
ReaderHEPEVT.read = _read

WriterAscii.__enter__ = _enter
WriterAscii.__exit__ = _exit_close
WriterAscii.write = WriterAscii.write_event

WriterAsciiHepMC2.__enter__ = _enter
WriterAsciiHepMC2.__exit__ = _exit_close
WriterAsciiHepMC2.write = WriterAsciiHepMC2.write_event

WriterHEPEVT.__enter__ = _enter
WriterHEPEVT.__exit__ = _exit_close
WriterHEPEVT.write = WriterHEPEVT.write_event

pyiostream.__enter__ = _enter
pyiostream.__exit__ = _exit_flush


_Filename = _tp.Union[str, PurePath]


class _WrappedWriter:
    # Wrapper for Writer, to be used by `open`

    def __init__(
        self,
        iostream: _tp.Any,
        precision: _tp.Optional[int],
        Writer: _tp.Any,
    ):
        self._writer: _tp.Any = None
        self._init = (iostream, precision, Writer)

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
            iostream, precision, Writer = self._init
            if Writer is WriterHEPEVT:
                self._writer = Writer(iostream)
            else:
                self._writer = Writer(iostream, evt.run_info)
            if precision is not None and hasattr(self._writer, "precision"):
                self._writer.precision = precision

        self._writer.write_event(evt)
        if self._writer.failed():
            raise IOError("writing GenEvent failed")

    def close(self) -> None:
        if self._writer is not None:
            self._writer.close()

    __enter__ = _enter
    __exit__ = _exit_close


@contextlib.contextmanager
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
        the contents are replaced. When the filename ends with the suffixes ".gz",
        ".bz2", or ".xz", the contents are transparently compressed/decompressed.
    mode : str, optional
        Must be either "r" (default) or "w", to indicate whether to open for reading
        or writing.
    precision : int or None, optional
        How many digits of precision to use when writing to a file. Can be used to
        improve the compression rate.
    format : str or None, optional
        Which format to use for reading or writing. If None (default), autodetect
        format when reading (this is fast and thus safe to use), and use the latest
        HepMC3 format when writing. Allowed values (case-insensitive): "HepMC3",
        "HepMC2", "LHEF", "HEPEVT". "LHEF" is not supported for writing.

    Raises
    ------
    IOError if reading or writing fails.
    """
    fn = str(filename)

    if fn.endswith(".gz"):
        import gzip

        op = gzip.open
    elif fn.endswith(".bz2"):
        import bz2

        op = bz2.open  # type:ignore

    elif fn.endswith(".xz"):
        import lzma

        op = lzma.open  # type:ignore
    else:
        op = _open  # type:ignore
        mode += "b"

    if mode.startswith("r"):
        if format is None:
            # auto-detect
            with op(fn, mode) as f:
                chunk = f.read(256)
            assert isinstance(chunk, bytes)
            header = chunk.decode()
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
        with op(fn, mode) as f:
            with pyiostream(f) as io:
                with Reader(io) as r:
                    yield r
    elif mode.startswith("w"):
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
        with op(fn, mode) as f:
            with pyiostream(f) as io:
                with _WrappedWriter(io, precision, Writer) as w:
                    yield w
    else:
        raise ValueError(f"mode must be r or w, got {mode}")
