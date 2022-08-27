# DO NOT EDIT: created by generate_docs.py
# flake8: noqa

from pyhepmc import (
    FourVector,
    GenEvent,
    GenHeavyIon,
    GenParticle,
    GenRunInfo,
    GenVertex,
    ReaderAscii,
    ReaderAsciiHepMC2,
    ReaderHEPEVT,
    ReaderLHEF,
    Units,
    WriterAscii,
    WriterAsciiHepMC2,
    WriterHEPEVT,
)

ReaderAsciiHepMC2.__doc__ = """Parser for HepMC2 I/O files."""

GenParticle.__doc__ = """Stores particle-related information."""

GenRunInfo.__doc__ = """Stores run-related information.

Manages run-related information. Contains run-wide attributes."""

ReaderAscii.__doc__ = """GenEvent I/O parsing for structured text files."""

WriterHEPEVT.__doc__ = """GenEvent I/O serialization for HEPEVT files."""

ReaderLHEF.__doc__ = """GenEvent I/O parsing and serialization for LHEF files."""

GenHeavyIon.__doc__ = """Stores additional information about Heavy Ion generator.

This is an example of event attribute used to store Heavy Ion information."""

FourVector.__doc__ = """Generic 4-vector.

Interpretation of its content depends on accessors used: it's much simpler to do this than to distinguish between space and momentum vectors via the type system (especially given the need for backward compatibility with HepMC2). Be sensible and don't call energy functions on spatial vectors! To avoid duplication, most definitions are only implemented on the spatial function names, with the energy-momentum functions as aliases.

This is not intended to be a fully featured 4-vector, but does contain the majority of common non-boosting functionality, as well as a few support operations on 4-vectors.

The implementations in this class are fully inlined."""

WriterAscii.__doc__ = """GenEvent I/O serialization for structured text files."""

GenEvent.__doc__ = """Stores event-related information.

Manages event-related information. Contains lists of GenParticle and GenVertex objects."""

WriterAsciiHepMC2.__doc__ = """GenEvent I/O serialization for structured text files."""

GenVertex.__doc__ = """Stores vertex-related information."""

Units.__doc__ = """Stores units-related enums and conversion functions.

Manages units used by HepMC::GenEvent."""

ReaderHEPEVT.__doc__ = """GenEvent I/O parsing and serialization for HEPEVT files."""
