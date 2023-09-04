"""
HepMC3 IO classes.

This module contains various Reader and Writer classes, which have
pythonic interfaces. They act as context managers and close the file
automatically. The Readers can be iterated over and yield events.

The :func:`open` function is even easier to use. It can read any
supported file and will auto-detect the format. It can be used for
reading and writing.
"""
from __future__ import annotations
from ._core import (
    GenEvent,
    ReaderAscii as ReaderAsciiBase,
    ReaderAsciiHepMC2 as ReaderAsciiHepMC2Base,
    ReaderLHEF as ReaderLHEFBase,
    ReaderHEPEVT as ReaderHEPEVTBase,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
    UnparsedAttribute,
    pyiostream,
)
from pathlib import PurePath
from typing import Union, Any, Optional, Callable

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


def _enter(self: Any) -> Any:
    return self


def _exit_close(self: Any, type: Exception, value: str, tb: Any) -> bool:
    self.close()
    return False


def _exit_flush(self: Any, type: Exception, value: str, tb: Any) -> bool:
    self.flush()
    return False


def _read_event_lhef_patch(self: Any, evt: GenEvent) -> bool:
    failed = self._read_event_unpatched(evt)
    if failed and self.failed():  # probably EOF
        return True
    return not failed


class _Iter:
    def __init__(self, reader: Any):
        self.reader = reader

    def __next__(self) -> GenEvent:
        evt = self.reader.read()
        if evt is None:
            raise StopIteration
        return evt

    def __iter__(self) -> "_Iter":
        return self

    next = __next__


class ReaderMixin:
    def read(self) -> Optional[GenEvent]:
        assert hasattr(self, "failed")
        assert hasattr(self, "read_event")
        if self.failed():
            # usually this means EOF was reached previously
            return None
        evt = GenEvent()
        success = self.read_event(evt)
        # workaround for bug in HepMC3, which reports success even if
        # the next section of the file does not contain any event data
        if len(evt.particles) == 0:
            success = False
        return evt if success else None

    def __iter__(self: Any) -> _Iter:
        return _Iter(self)

    __enter__ = _enter
    __exit__ = _exit_close


# add contextmanager interface to IO classes
class ReaderAscii(ReaderAsciiBase, ReaderMixin):  # type:ignore
    pass


class ReaderAsciiHepMC2(ReaderAsciiHepMC2Base, ReaderMixin):  # type:ignore
    pass


class ReaderLHEF(ReaderLHEFBase, ReaderMixin):  # type:ignore
    _read_event_unpatched = ReaderLHEFBase.read_event
    read_event = _read_event_lhef_patch


class ReaderHEPEVT(ReaderHEPEVTBase, ReaderMixin):  # type:ignore
    pass


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


Filename = Union[str, PurePath]


class _WrappedWriter:
    # Wrapper for Writer, to be used by `open`

    def __init__(
        self,
        iostream: Any,
        precision: Optional[int],
        Writer: Any,
    ):
        self._writer: Any = None
        self._init = (iostream, precision, Writer)
        self._event = None

    def _maybe_convert(self, event: Any) -> GenEvent:
        if isinstance(event, GenEvent):
            return event
        if hasattr(event, "to_hepmc3"):
            # reuse GenEvent to not recreate GenRunInfo repeatedly
            self._event = event.to_hepmc3(self._event)
            return self._event
        raise TypeError(
            "event must be an instance of GenEvent or "
            "convertible to it by providing a to_hepmc3() method"
        )

    def write(self, event: Any) -> None:
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


class HepMCFile:
    """
    HepMC file for reading or writing.

    Parameters
    ----------
    fileobj : str or Path or IO object
        Filename to open for reading or writing or file object. When writing to
        existing files, the contents are replaced. When the filename ends with the
        suffixes ".gz", ".bz2", or ".xz", the contents are transparently compressed
        and decompressed.
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

    _reader: Optional[ReaderMixin]
    _writer: Optional[Union[WriterAscii, WriterAsciiHepMC2, WriterHEPEVT]]

    def __init__(
        self,
        fileobj: Filename,
        mode: str = "r",
        precision: int = None,
        format: str = None,
    ):
        open_file: Optional[Callable[[], Any]] = None
        if hasattr(fileobj, "read") and hasattr(fileobj, "write"):
            if hasattr(fileobj, "buffer"):
                self._file = fileobj.buffer
            else:
                self._file = fileobj
            self._close_file = False
        else:
            fn = str(fileobj)

            if fn.endswith(".gz"):
                import gzip

                open = gzip.open
            elif fn.endswith(".bz2"):
                import bz2

                open = bz2.open  # type:ignore
            elif fn.endswith(".xz"):
                import lzma

                open = lzma.open  # type:ignore
            else:
                from builtins import open  # type:ignore

                mode += "b"

            open_file = lambda: open(fn, mode)  # noqa: E731

            self._close_file = True

        if mode.startswith("r"):
            if open_file:
                self._file = open_file()
            self._ios = pyiostream(self._file)

            Reader: Optional[Any] = None
            if format is None:
                # auto-detect
                if not self._file.seekable():
                    raise ValueError("cannot detect format, file is not seekable")
                header = self._file.read(256)
                assert isinstance(header, bytes)  # for mypy
                self._file.seek(0)
                if b"HepMC::Asciiv3" in header:
                    Reader = ReaderAscii
                elif b"HepMC::IO_GenEvent" in header:
                    Reader = ReaderAsciiHepMC2
                elif b"<LesHouchesEvents" in header:
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
                    raise ValueError(f"format {format!r} not recognized for reading")

            self._reader = Reader(self._ios)
            self._writer = None

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
                    raise ValueError(f"format {format!r} not recognized for writing")

            if open_file:
                self._file = open_file()
            self._ios = pyiostream(self._file)
            self._reader = None
            self._writer = _WrappedWriter(self._ios, precision, Writer)
        else:
            raise ValueError(f"mode must be 'r' or 'w', got {mode!r}")

    __enter__ = _enter
    __exit__ = _exit_close

    def __iter__(self) -> Any:
        assert self._reader is not None
        return self._reader.__iter__()

    def flush(self) -> None:
        if not self._writer:
            raise IOError("File opened for reading")
        self._ios.flush()
        self._file.flush()

    def read(self) -> GenEvent:
        if not self._reader:
            raise IOError("File openened for writing")
        return self._reader.read()

    def write(self, event: GenEvent) -> None:
        if not self._writer:
            raise IOError("File openened for reading")
        self._writer.write(event)

    def close(self) -> None:
        if self._reader:
            self._reader.close()  # type:ignore
        if self._writer:
            self._writer.close()
        self._ios.flush()
        if self._close_file:
            self._file.close()


def open(
    fileobj: Filename,
    mode: str = "r",
    precision: int = None,
    format: str = None,
) -> Any:
    """
    Open HepMC files for reading or writing.

    See HepMCFile.
    """
    return HepMCFile(fileobj, mode, precision, format)
