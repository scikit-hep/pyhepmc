# DO NOT EDIT: created by generate_docs.py
# flake8: noqa
autodoc = {
    "FourVector": """Generic 4-vector.

Interpretation of its content depends on accessors used: it's much simpler to do this than to distinguish between space and momentum vectors via the type system (especially given the need for backward compatibility with hepmc2). be sensible and don't call energy functions on spatial vectors! to avoid duplication, most definitions are only implemented on the spatial function names, with the energy-momentum functions as aliases.

This is not intended to be a fully featured 4-vector, but does contain the majority of common non-boosting functionality, as well as a few support operations on 4-vectors.

The implementations in this class are fully inlined.""",
    "FourVector.__init__": """Default constructor.

Sets all fourvector fields.

Copy constructor.""",
    "FourVector.abs_eta": """Absolute pseudorapidity.""",
    "FourVector.abs_rap": """Absolute rapidity.""",
    "FourVector.e": """Energy component of momentum.""",
    "FourVector.eta": """Pseudorapidity.""",
    "FourVector.interval": """Spacetime invariant interval s^2 = t^2 - x^2 - y^2 - z^2.""",
    "FourVector.is_zero": """Check if the length of this vertex is zero.""",
    "FourVector.length": """Magnitude of spatial (x, y, z) 3-vector.""",
    "FourVector.length2": """Squared magnitude of (x, y, z) 3-vector.""",
    "FourVector.m": """Invariant mass. returns -sqrt(-m) if e^2 - p^2 is negative.""",
    "FourVector.m2": """Squared invariant mass m^2 = e^2 - px^2 - py^2 - pz^2.""",
    "FourVector.p3mod": """Magnitude of p3 = (px, py, pz) vector.""",
    "FourVector.p3mod2": """Squared magnitude of p3 = (px, py, pz) vector.""",
    "FourVector.perp": """Magnitude of (x, y) vector.""",
    "FourVector.perp2": """Squared magnitude of (x, y) vector.""",
    "FourVector.phi": """Azimuthal angle.""",
    "FourVector.pt": """Transverse momentum.""",
    "FourVector.pt2": """Squared transverse momentum px^2 + py^2.""",
    "FourVector.px": """X-component of momentum.""",
    "FourVector.py": """Y-component of momentum.""",
    "FourVector.pz": """Z-component of momentum.""",
    "FourVector.rap": """Rapidity.""",
    "FourVector.rho": """Magnitude of spatial (x, y, z) 3-vector, for hepmc2 compatibility.""",
    "FourVector.t": """Time component of position/displacement.""",
    "FourVector.theta": """Polar angle w.r.t. z direction.""",
    "FourVector.x": """X-component of position/displacement.""",
    "FourVector.y": """Y-component of position/displacement.""",
    "FourVector.z": """Z-component of position/displacement.""",
    "GenEvent": """Stores event-related information.

Manages event-related information. contains lists of genparticle and genvertex objects.""",
    "GenEvent.__init__": """Event constructor without a run.

Constructor with associated run.

Copy constructor.""",
    "GenEvent.add_particle": """Add particle.""",
    "GenEvent.add_vertex": """Add vertex.""",
    "GenEvent.beams": """Vector of beam particles.""",
    "GenEvent.clear": """Remove contents of this event.""",
    "GenEvent.cross_section": """Get cross-section information.""",
    "GenEvent.event_number": """Get event number.

Set event number.""",
    "GenEvent.event_pos": """Vertex representing the overall event position.""",
    "GenEvent.heavy_ion": """Get heavy ion generator additional information.""",
    "GenEvent.length_unit": """Get length unit.""",
    "GenEvent.momentum_unit": """Get momentum unit.""",
    "GenEvent.pdf_info": """Get pdf information.""",
    "GenEvent.remove_particle": """Remove particle from the event.

This function will remove whole sub-tree starting from this particle if it is the only incoming particle of this vertex. it will also production vertex of this particle if this vertex has no more outgoing particles.""",
    "GenEvent.remove_vertex": """Remove vertex from the event.

This will remove all sub-trees of all outgoing particles of this vertex.""",
    "GenEvent.reserve": """Reserve memory for particles and vertices.

Helps optimize event creation when size of the event is known beforehand.""",
    "GenEvent.run_info": """Get a pointer to the the genruninfo object.

Set the genruninfo object by smart pointer.""",
    "GenEvent.set_units": """Change event units converts event from current units to new ones.""",
    "GenEvent.vertices": """Get/set list of vertices.""",
    "GenEvent.weight": """Get event weight accessed by index (or the canonical/first one if there is no argument) it's the user's responsibility to ensure that the given index exists!.

Get event weight accessed by weight name requires there to be an attached genruninfo, otherwise will throw an exception

it's the user's responsibility to ensure that the given name exists!.

Get event weight accessed by weight name requires there to be an attached genruninfo, otherwise will throw an exception

it's the user's responsibility to ensure that the given name exists!.""",
    "GenEvent.weight_names": """Get event weight names, if there are some requires there to be an attached genruninfo with registered weight names, otherwise will throw an exception.""",
    "GenEvent.weights": """Get event weight values as a vector.

Get event weights as a vector (non-const).""",
    "GenHeavyIon": """Stores additional information about heavy ion generator.

This is an example of event attribute used to store heavy ion information.""",
    "GenHeavyIon.__init__": """Empty default constructor.""",
    "GenParticle": """Stores particle-related information.""",
    "GenParticle.__init__": """Default constructor.

Constructor based on particle data.""",
    "GenParticle.children": """Convenience access to immediate outgoing particles via end vertex.

Less efficient than via the vertex since return must be by value (in case there is no vertex).""",
    "GenParticle.in_event": """Check if this particle belongs to an event.""",
    "GenParticle.production_vertex": """Get production vertex (const version).

Get production vertex.""",
    "GenParticle.unset_generated_mass": """Declare that generated mass is not set.""",
    "GenRunInfo": """Stores run-related information.

Manages run-related information. contains run-wide attributes.""",
    "GenRunInfo.ToolInfo": """Interrnal struct for keeping track of tools.""",
    "GenRunInfo.ToolInfo.description": """Other information about how the tool was used in the run.""",
    "GenRunInfo.ToolInfo.name": """The name of the tool.""",
    "GenRunInfo.ToolInfo.version": """The version of the tool.""",
    "GenRunInfo.__init__": """Default constructor.

Copy constructor.""",
    "GenRunInfo.attributes": """Get a copy of the list of attributes.

To avoid thread issues, this is returns a copy. better solution may be needed.""",
    "GenRunInfo.tools": """The vector of tools used to produce this run.""",
    "GenRunInfo.weight_names": """Get the vector of weight names.

Set the names of the weights in this run.

For consistency, the length of the vector should be the same as the number of weights in the events in the run.""",
    "GenVertex": """Stores vertex-related information.""",
    "GenVertex.__init__": """Default constructor.

Constructor based on vertex data.""",
    "GenVertex.add_particle_in": """Add incoming particle.""",
    "GenVertex.add_particle_out": """Add outgoing particle.""",
    "GenVertex.has_set_position": """Check if position of this vertex is set.""",
    "GenVertex.id": """Get the vertex unique identifier.

This is not the same as id() in hepmc v2, which is now status().

Set the vertex identifier.""",
    "GenVertex.in_event": """Check if this vertex belongs to an event.""",
    "GenVertex.parent_event": """Get parent event.""",
    "GenVertex.particles_in": """Get list of incoming particles.""",
    "GenVertex.particles_out": """Get list of outgoing particles.""",
    "GenVertex.position": """Get vertex position.

Returns the position of this vertex. if a position is not set on this vertex, the production vertices of ancestors are searched to find the inherited position. fourvector(0,0,0,0) is returned if no position information is found.

Set vertex position.""",
    "GenVertex.remove_particle_in": """Remove incoming particle.""",
    "GenVertex.remove_particle_out": """Remove outgoing particle.""",
    "GenVertex.status": """Get vertex status code.

Set vertex status code.""",
    "ReaderAscii": """Genevent i/o parsing for structured text files.""",
    "ReaderAscii.__init__": """Constructor.

The ctor to read from stream.

The ctor to read from stream. useful for temp. streams.""",
    "ReaderAscii.close": """Close file stream.

Todoimplicit cast to bool = !failed()?.""",
    "ReaderAscii.failed": """Return status of the stream.

Todono-arg version returning genevent?.""",
    "ReaderAscii.read_event": """Load event from file.

Parameters
----------
evt:
    Event to be filled.""",
    "ReaderAsciiHepMC2": """Parser for hepmc2 i/o files.""",
    "ReaderAsciiHepMC2.__init__": """Default constructor.

The ctor to read from stream.

The ctor to read from temp stream.""",
    "ReaderAsciiHepMC2.close": """Close file stream.""",
    "ReaderAsciiHepMC2.failed": """Return status of the stream.""",
    "ReaderAsciiHepMC2.read_event": """Implementation of reader::read_event.""",
    "ReaderHEPEVT": """Genevent i/o parsing and serialization for hepevt files.""",
    "ReaderHEPEVT.__init__": """Default constructor.

The ctor to read from stream.

The ctor to read from temp stream.""",
    "ReaderHEPEVT.close": """Close file stream.""",
    "ReaderHEPEVT.failed": """Get stream error state.""",
    "ReaderHEPEVT.read_event": """Read event from file.""",
    "ReaderLHEF": """Genevent i/o parsing and serialization for lhef files.""",
    "ReaderLHEF.__init__": """The ctor to read from stream.

Constructor.

The ctor to read from temp stream.""",
    "ReaderLHEF.close": """Close.""",
    "ReaderLHEF.failed": """State.""",
    "ReaderLHEF.read_event": """Reading event.""",
    "WriterAscii": """Genevent i/o serialization for structured text files.""",
    "WriterAscii.__init__": """Constructor.

If file already exists, it will be cleared before writing.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterAscii.close": """Close file stream.""",
    "WriterAscii.failed": """Return status of the stream.""",
    "WriterAscii.precision": """Return output precision.

Set output precision.

So far available range is [2,24]. default is 16.""",
    "WriterAscii.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterAscii.write_run_info": """Write the genruninfo object to file.""",
    "WriterAsciiHepMC2": """Genevent i/o serialization for structured text files.""",
    "WriterAsciiHepMC2.__init__": """Constructor.

If file already exists, it will be cleared before writing.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterAsciiHepMC2.close": """Close file stream.""",
    "WriterAsciiHepMC2.failed": """Return status of the stream.""",
    "WriterAsciiHepMC2.precision": """Return output precision.

Set output precision.

Available range is [2,24]. default is 16.""",
    "WriterAsciiHepMC2.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterAsciiHepMC2.write_run_info": """Write the genruninfo object to file.""",
    "WriterHEPEVT": """Genevent i/o serialization for hepevt files.""",
    "WriterHEPEVT.__init__": """Default constructor.

If file exists, it will be overwritten.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterHEPEVT.close": """Close file stream.""",
    "WriterHEPEVT.failed": """Get stream error state flag.""",
    "WriterHEPEVT.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
}
