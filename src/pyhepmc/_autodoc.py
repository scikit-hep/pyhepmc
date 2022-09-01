# DO NOT EDIT: created by generate_docs.py
# flake8: noqa
autodoc = {
    "AssociatedParticle": """Attribute class allowing eg. a GenParticle to refer to another GenParticle.""",
    "AssociatedParticle.__init__": """Default constructor.

Constructor initializing attribute value.""",
    "AssociatedParticle.associatedId": """get id of the associated particle.""",
    "AssociatedParticle.event": """return the GenEvent to which this Attribute belongs, if at all.""",
    "AssociatedParticle.from_string": """Implementation of Attribute::from_string.""",
    "AssociatedParticle.init": """Optionally initialize the attribute after from_string.""",
    "AssociatedParticle.is_parsed": """Check if this attribute is parsed.""",
    "AssociatedParticle.particle": """return the GenParticle to which this Attribute belongs, if at all.""",
    "AssociatedParticle.to_string": """Implementation of Attribute::to_string.""",
    "AssociatedParticle.unparsed_string": """Get unparsed string.""",
    "AssociatedParticle.vertex": """return the GenVertex to which this Attribute belongs, if at all.""",
    "FourVector": """Generic 4-vector.

Interpretation of its content depends on accessors used: it's much simpler to do this than to distinguish between space and momentum vectors via the type system (especially given the need for backward compatibility with HepMC2). Be sensible and don't call energy functions on spatial vectors! To avoid duplication, most definitions are only implemented on the spatial function names, with the energy-momentum functions as aliases.

This is not intended to be a fully featured 4-vector, but does contain the majority of common non-boosting functionality, as well as a few support operations on 4-vectors.

The implementations in this class are fully inlined.""",
    "FourVector.__init__": """Default constructor.

Accesss all FourVector fields.

Copy constructor.""",
    "FourVector.abs_eta": """Absolute pseudorapidity.""",
    "FourVector.abs_rap": """Absolute rapidity.""",
    "FourVector.eta": """Pseudorapidity.""",
    "FourVector.interval": """Spacetime invariant interval s^2 = t^2 - x^2 - y^2 - z^2.""",
    "FourVector.is_zero": """Check if the length of this vertex is zero.""",
    "FourVector.length": """Magnitude of spatial (x, y, z) 3-vector.""",
    "FourVector.length2": """Squared magnitude of (x, y, z) 3-vector.""",
    "FourVector.m": """Invariant mass. Returns -sqrt(-m) if e^2 - P^2 is negative.""",
    "FourVector.m2": """Squared invariant mass m^2 = E^2 - px^2 - py^2 - pz^2.""",
    "FourVector.p3mod": """Magnitude of p3 = (px, py, pz) vector.""",
    "FourVector.p3mod2": """Squared magnitude of p3 = (px, py, pz) vector.""",
    "FourVector.perp": """Magnitude of (x, y) vector.""",
    "FourVector.perp2": """Squared magnitude of (x, y) vector.""",
    "FourVector.phi": """Azimuthal angle.""",
    "FourVector.pt": """Transverse momentum.""",
    "FourVector.pt2": """Squared transverse momentum px^2 + py^2.""",
    "FourVector.rap": """Rapidity.""",
    "FourVector.rho": """Magnitude of spatial (x, y, z) 3-vector, for HepMC2 compatibility.""",
    "FourVector.theta": """Polar angle w.r.t. z direction.""",
    "GenCrossSection": """Stores additional information about cross-section.

This is an example of event attribute used to store cross-section information.

This class is meant to be used to pass, on an event by event basis, the current best guess of the total cross section. It is expected that the final cross section will be stored elsewhere.

double cross_section; // cross section in pb.
double cross_section_error; // error associated with this cross section.
long accepted_events; ///< The number of events generated so far.
long attempted_events; ///< The number of events attempted so far.

In addition, several cross sections and related info can be included in case of runs with mulltiple weights.

The units of cross_section and cross_section_error are expected to be pb.""",
    "GenCrossSection.accepted_events": """Access the number of accepted events.""",
    "GenCrossSection.attempted_events": """Access the number of attempted events.""",
    "GenCrossSection.event": """return the GenEvent to which this Attribute belongs, if at all.""",
    "GenCrossSection.from_string": """Implementation of Attribute::from_string.""",
    "GenCrossSection.init": """Optionally initialize the attribute after from_string.""",
    "GenCrossSection.is_parsed": """Check if this attribute is parsed.""",
    "GenCrossSection.is_valid": """Verify that the instance contains non-zero information.""",
    "GenCrossSection.particle": """return the GenParticle to which this Attribute belongs, if at all.""",
    "GenCrossSection.set_cross_section": """Set all fields.""",
    "GenCrossSection.to_string": """Implementation of Attribute::to_string.""",
    "GenCrossSection.unparsed_string": """Get unparsed string.""",
    "GenCrossSection.vertex": """return the GenVertex to which this Attribute belongs, if at all.""",
    "GenEvent": """Stores event-related information.

Manages event-related information. Contains lists of GenParticle and GenVertex objects.""",
    "GenEvent.__init__": """Event constructor without a run.

Constructor with associated run.

Copy constructor.""",
    "GenEvent.add_attributes": """Add multiple attributes to event.

This will overwrite existing attributes if attributes with the same names are present.""",
    "GenEvent.add_beam_particle": """Add particle to root vertex.""",
    "GenEvent.add_particle": """Add particle.""",
    "GenEvent.add_tree": """Add whole tree in topological order.

This function will find the beam particles (particles that have no production vertices or their production vertices have no particles) and will add the whole decay tree starting from these particles.

Any particles on this list that do not belong to the tree will be ignored.""",
    "GenEvent.add_vertex": """Add vertex.""",
    "GenEvent.attribute": """Get attribute of type T.""",
    "GenEvent.attribute_as_string": """Get attribute of any type as string.""",
    "GenEvent.attribute_names": """Get list of attribute names.""",
    "GenEvent.attributes": """Get a copy of the list of attributes.

To avoid thread issues, this is returns a copy. Better solution may be needed.""",
    "GenEvent.beams": """Vector of beam particles.""",
    "GenEvent.boost": """Boost event using x,y,z components of v as velocities.""",
    "GenEvent.clear": """Remove contents of this event.""",
    "GenEvent.event_pos": """Vertex representing the overall event position.""",
    "GenEvent.length_unit": """Get length unit.""",
    "GenEvent.momentum_unit": """Get momentum unit.""",
    "GenEvent.particles": """Access list of particles.""",
    "GenEvent.particles_empty": """Particles empty, HepMC2 compatiility.""",
    "GenEvent.particles_size": """Particles size, HepMC2 compatiility.""",
    "GenEvent.read_data": """Fill GenEvent based on GenEventData.""",
    "GenEvent.reflect": """Change sign of axis.""",
    "GenEvent.remove_attribute": """Remove attribute.""",
    "GenEvent.remove_particle": """Remove particle from the event.

This function will remove whole sub-tree starting from this particle if it is the only incoming particle of this vertex. It will also production vertex of this particle if this vertex has no more outgoing particles.""",
    "GenEvent.remove_particles": """Remove a set of particles.

This function follows rules of GenEvent::remove_particle to remove a list of particles from the event.""",
    "GenEvent.remove_vertex": """Remove vertex from the event.

This will remove all sub-trees of all outgoing particles of this vertex.""",
    "GenEvent.reserve": """Reserve memory for particles and vertices.

Helps optimize event creation when size of the event is known beforehand.""",
    "GenEvent.rotate": """Rotate event using x,y,z components of v as rotation angles.""",
    "GenEvent.set_units": """Change event units Converts event from current units to new ones.""",
    "GenEvent.shift_position_by": """Shift position of all vertices in the event by delta.""",
    "GenEvent.shift_position_to": """Shift position of all vertices in the event to op.""",
    "GenEvent.vertices": """Access list of vertices.""",
    "GenEvent.vertices_empty": """Vertices empty, HepMC2 compatiility.""",
    "GenEvent.vertices_size": """Vertices size, HepMC2 compatiility.""",
    "GenEvent.weight": """Access event weight accessed by index (or the canonical/first one if there is no argument) It's the user's responsibility to ensure that the given index exists!.

Access event weight accessed by weight name Requires there to be an attached GenRunInfo, otherwise will throw an exception

It's the user's responsibility to ensure that the given name exists!.

Access event weight accessed by weight name Requires there to be an attached GenRunInfo, otherwise will throw an exception

It's the user's responsibility to ensure that the given name exists!.""",
    "GenEvent.weight_names": """Get event weight names, if there are some Requires there to be an attached GenRunInfo with registered weight names, otherwise will throw an exception.""",
    "GenEvent.weights": """Access event weight values as a vector.

Access event weights as a vector.""",
    "GenEvent.write_data": """Fill GenEventData object.""",
    "GenEventData": """Stores serializable event information.""",
    "GenEventData.attribute_id": """Attribute owner id.""",
    "GenEventData.attribute_name": """Attribute name.""",
    "GenEventData.attribute_string": """Attribute serialized as string.""",
    "GenEventData.event_number": """Event number.""",
    "GenEventData.event_pos": """Event position.""",
    "GenEventData.length_unit": """Length unit.""",
    "GenEventData.links1": """First id of the vertex links.

If this id is positive - it is the incoming particle id of a vertex which id is written in GenEventData::links2.

If this id is negative - it's the id of a vertex which outgoing particle id is written in GenEventData::links2.

The links1[i] points to links2[i]. In case links1[i] is particle, links2[i] is end vertex. In case links2[i] is vertex, links2[i] is outgoing particle. An example of usage is given in documentation.""",
    "GenEventData.links2": """Second id of the vertex links.""",
    "GenEventData.momentum_unit": """Momentum unit.""",
    "GenEventData.particles": """Particles.""",
    "GenEventData.vertices": """Vertices.""",
    "GenEventData.weights": """Weights.""",
    "GenHeavyIon": """Stores additional information about Heavy Ion generator.

This is an example of event attribute used to store Heavy Ion information.""",
    "GenHeavyIon.N_Nwounded_collisions": """Collisions with a diffractively excited target nucleon.

The number of single diffractive nucleon-nucleon collisions where the target nucleon is excited. A negative value means that the information is not available.""",
    "GenHeavyIon.Ncoll": """the number of inelastic nucleon-nucleon collisions.

Note that a one participating nucleon can be involved in many inelastic collisions, and that inelastic also includes diffractive excitation. A negative value means that the information is not available.""",
    "GenHeavyIon.Ncoll_hard": """the number of hard nucleon-nucleon collisions.

Model-dependent. Usually the number of nucleon-nucleon collisions containing a special signal process. A negative value means that the information is not available.""",
    "GenHeavyIon.Npart_proj": """the number of participating nucleons in the projectile.

The number of nucleons in the projectile participating in an inelastic collision (see Ncoll). A negative value means that the information is not available.""",
    "GenHeavyIon.Npart_targ": """the number of participating nucleons in the target.

The number of nucleons in the target participating in an inelastic collision (see Ncoll). A negative value means that the information is not available.""",
    "GenHeavyIon.Nspec_proj_n": """The number of spectator neutrons in the projectile.

ie. those that thave not participated in any inelastic nucleon-nucleon collision. A negative value indicatess that the information is not available.""",
    "GenHeavyIon.Nspec_proj_p": """The number of spectator protons in the projectile.

ie. those that thave not participated in any inelastic nucleon-nucleon collision. A negative value indicatess that the information is not available.""",
    "GenHeavyIon.Nspec_targ_n": """The number of spectator neutrons in the target.

ie. those that thave not participated in any inelastic nucleon-nucleon collision. A negative value indicatess that the information is not available.""",
    "GenHeavyIon.Nspec_targ_p": """The number of spectator protons in the target.

ie. those that thave not participated in any inelastic nucleon-nucleon collision. A negative value indicatess that the information is not available.""",
    "GenHeavyIon.Nwounded_N_collisions": """Collisions with a diffractively excited projectile nucleon.

The number of single diffractive nucleon-nucleon collisions where the projectile nucleon is excited. A negative value means that the information is not available.""",
    "GenHeavyIon.Nwounded_Nwounded_collisions": """Non-diffractive or doubly diffractive collisions.

The number of nucleon-nucleon collisions where both projectile and target nucleons are wounded. A negative value means that the information is not available.""",
    "GenHeavyIon.__init__": """Empty default constructor.""",
    "GenHeavyIon.centrality": """The centrality.

The generated centrality in percentiles, where 0 is the maximally central and 100 is the minimally central. A negative value means that the information is not available.""",
    "GenHeavyIon.eccentricities": """Eccentricities.

Calculated to different orders. The key of the map specifies the order, and the value gives the corresponding eccentricity.""",
    "GenHeavyIon.eccentricity": """The eccentricity.

HEPMC3_DEPRECATED("Use eccentricities insted.").""",
    "GenHeavyIon.event": """return the GenEvent to which this Attribute belongs, if at all.""",
    "GenHeavyIon.event_plane_angle": """The event plane angle.

The angle wrt. the x-axix of the impact parameter vector (pointing frm the target to the projectile). A positive number between 0 and two pi. A negative value means that the information is not available.""",
    "GenHeavyIon.forceoldformat": """force writing in old format for compatibility purposes.

HEPMC3_DEPRECATED("This should really not be needed");.""",
    "GenHeavyIon.from_string": """Implementation of Attribute::from_string.""",
    "GenHeavyIon.impact_parameter": """The impact parameter.

The impact parameter given in units of femtometer. A negative value means that the information is not available.""",
    "GenHeavyIon.init": """Optionally initialize the attribute after from_string.""",
    "GenHeavyIon.is_parsed": """Check if this attribute is parsed.""",
    "GenHeavyIon.is_valid": """Verify that the instance contains non-zero information.

HEPMC3_DEPRECATED("Each filed now have default values meaning
that they have not been set").""",
    "GenHeavyIon.participant_plane_angles": """Participant plane angles.

calculated to different orders. The key of the map specifies the order, and the value gives to the angle wrt. the event plane.""",
    "GenHeavyIon.particle": """return the GenParticle to which this Attribute belongs, if at all.""",
    "GenHeavyIon.set": """Set all fields.

HEPMC3_DEPRECATED("Set individual fields directly instead.").

Set all fields.""",
    "GenHeavyIon.sigma_inel_NN": """The assumed inelastic nucleon-nucleon cross section.

in units of millibarn. As used in a Glauber calculation to simulate the distribution in Ncoll. A negative value means that the information is not available.""",
    "GenHeavyIon.spectator_neutrons": """Total number of spectator neutrons.

HEPMC3_DEPRECATED("Use Nspec_proj_n and Nspec_targ_n instead.").""",
    "GenHeavyIon.spectator_protons": """Total number of spectator protons.

HEPMC3_DEPRECATED("Use Nspec_proj_p and Nspec_targ_p instead.").""",
    "GenHeavyIon.to_string": """Implementation of Attribute::to_string.""",
    "GenHeavyIon.unparsed_string": """Get unparsed string.""",
    "GenHeavyIon.user_cent_estimate": """A user defined centrality estimator.

This variable may contain anything a generator feels is reasonable for estimating centrality. The value should be non-negative, and a low value corresponds to a low centrality. A negative value indicatess that the information is not available.""",
    "GenHeavyIon.vertex": """return the GenVertex to which this Attribute belongs, if at all.""",
    "GenParticle": """Stores particle-related information.""",
    "GenParticle.__init__": """Default constructor.

Constructor based on particle data.""",
    "GenParticle.add_attribute": """Add an attribute to this particle.

This will overwrite existing attribute if an attribute with the same name is present. The attribute will be stored in the parent_event(). false if there is no parent_event();.""",
    "GenParticle.attribute": """Get attribute of type T.""",
    "GenParticle.attribute_as_string": """Get attribute of any type as string.""",
    "GenParticle.attribute_names": """Get list of names of attributes assigned to this particle.""",
    "GenParticle.children": """Convenience access to immediate outgoing particles via end vertex.

Less efficient than via the vertex since return must be by value (in case there is no vertex).""",
    "GenParticle.end_vertex": """Access end vertex.""",
    "GenParticle.in_event": """Check if this particle belongs to an event.""",
    "GenParticle.parents": """Convenience access to immediate incoming particles via production vertex.

Less efficient than via the vertex since return must be by value (in case there is no vertex).""",
    "GenParticle.production_vertex": """Access production vertex.""",
    "GenParticle.remove_attribute": """Remove attribute.""",
    "GenParticle.set_momentum": """Set momentum.""",
    "GenParticle.set_pid": """Set PDG ID.""",
    "GenParticle.set_status": """Set status code.""",
    "GenParticle.unset_generated_mass": """Declare that generated mass is not set.""",
    "GenParticleData": """Stores serializable particle information.""",
    "GenParticleData.is_mass_set": """Check if generated mass is set.""",
    "GenParticleData.mass": """Generated mass (if set).""",
    "GenParticleData.momentum": """Momentum.""",
    "GenParticleData.pid": """PDG ID.""",
    "GenParticleData.status": """Status.""",
    "GenPdfInfo": """Stores additional information about PDFs.

This is an example of event attribute used to store PDF-related information.

Input parton flavour codes id1 & id2 are expected to obey the PDG code conventions, especially g = 21.

The contents of pdf1 and pdf2 are expected to be x*f(x). The LHAPDF set ids are the entries in the first column of http:///projects.hepforge.org/lhapdf/PDFsets.index.""",
    "GenPdfInfo.event": """return the GenEvent to which this Attribute belongs, if at all.""",
    "GenPdfInfo.from_string": """Implementation of Attribute::from_string.""",
    "GenPdfInfo.init": """Optionally initialize the attribute after from_string.""",
    "GenPdfInfo.is_parsed": """Check if this attribute is parsed.""",
    "GenPdfInfo.is_valid": """Verify that the instance contains non-zero information.""",
    "GenPdfInfo.particle": """return the GenParticle to which this Attribute belongs, if at all.""",
    "GenPdfInfo.parton_id": """Parton PDG ID.""",
    "GenPdfInfo.pdf_id": """LHAPDF ID code.""",
    "GenPdfInfo.scale": """Factorisation scale (in GEV).""",
    "GenPdfInfo.set": """Set all fields.""",
    "GenPdfInfo.to_string": """Implementation of Attribute::to_string.""",
    "GenPdfInfo.unparsed_string": """Get unparsed string.""",
    "GenPdfInfo.vertex": """return the GenVertex to which this Attribute belongs, if at all.""",
    "GenPdfInfo.x": """Parton momentum fraction.""",
    "GenPdfInfo.xf": """PDF value.""",
    "GenRunInfo": """Stores run-related information.

Manages run-related information. Contains run-wide attributes.""",
    "GenRunInfo.ToolInfo": """Interrnal struct for keeping track of tools.""",
    "GenRunInfo.ToolInfo.description": """Other information about how the tool was used in the run.""",
    "GenRunInfo.ToolInfo.name": """The name of the tool.""",
    "GenRunInfo.ToolInfo.version": """The version of the tool.""",
    "GenRunInfo.__init__": """Default constructor.

Copy constructor.""",
    "GenRunInfo.add_attribute": """add an attribute This will overwrite existing attribute if an attribute with the same name is present.""",
    "GenRunInfo.attribute": """Get attribute of type T.""",
    "GenRunInfo.attribute_as_string": """Get attribute of any type as string.""",
    "GenRunInfo.attribute_names": """Get list of attribute names.""",
    "GenRunInfo.attributes": """Get a copy of the list of attributes.

To avoid thread issues, this is returns a copy. Better solution may be needed.""",
    "GenRunInfo.has_weight": """Check if a weight name is present.""",
    "GenRunInfo.read_data": """Fill GenRunInfo based on GenRunInfoData.""",
    "GenRunInfo.remove_attribute": """Remove attribute.""",
    "GenRunInfo.tools": """The vector of tools used to produce this run.""",
    "GenRunInfo.weight_index": """Return the index corresponding to a weight name.

-1 if name was not found.""",
    "GenRunInfo.weight_indices": """Returns a copy of indices map.""",
    "GenRunInfo.write_data": """Fill GenRunInfoData object.""",
    "GenRunInfoData": """Stores serializable run information.""",
    "GenRunInfoData.attribute_name": """Attribute name.""",
    "GenRunInfoData.attribute_string": """Attribute serialized as string.""",
    "GenRunInfoData.tool_description": """Tool descriptions.""",
    "GenRunInfoData.tool_name": """Tool names.""",
    "GenRunInfoData.tool_version": """Tool versions.""",
    "GenRunInfoData.weight_names": """Weight names.""",
    "GenVertex": """Stores vertex-related information.""",
    "GenVertex.__init__": """Default constructor.

Constructor based on vertex data.""",
    "GenVertex.add_attribute": """Add event attribute to this vertex.

This will overwrite existing attribute if an attribute with the same name is present. The attribute will be stored in the parent_event(). false if there is no parent_event();.""",
    "GenVertex.add_particle_in": """Add incoming particle.""",
    "GenVertex.add_particle_out": """Add outgoing particle.""",
    "GenVertex.attribute": """Get attribute of type T.""",
    "GenVertex.attribute_as_string": """Get attribute of any type as string.""",
    "GenVertex.attribute_names": """Get list of names of attributes assigned to this particle.""",
    "GenVertex.data": """Get vertex data.""",
    "GenVertex.has_set_position": """Check if position of this vertex is set.""",
    "GenVertex.in_event": """Check if this vertex belongs to an event.""",
    "GenVertex.parent_event": """Access parent event.""",
    "GenVertex.particles_in": """Access list of incoming particles.""",
    "GenVertex.particles_in_size": """Number of incoming particles, HepMC2 compatiility.""",
    "GenVertex.particles_out": """Access list of outgoing particles.""",
    "GenVertex.particles_out_size": """Number of outgoing particles, HepMC2 compatiility.""",
    "GenVertex.remove_attribute": """Remove attribute.""",
    "GenVertex.remove_particle_in": """Remove incoming particle.""",
    "GenVertex.remove_particle_out": """Remove outgoing particle.""",
    "GenVertexData": """Stores serializable vertex information.""",
    "GenVertexData.is_zero": """Check if this struct fields are zero.""",
    "GenVertexData.position": """Position in time-space.""",
    "GenVertexData.status": """Vertex status.""",
    "Print": """Provides different printing formats.""",
    "Print.content": """Print content of all GenEvent containers.""",
    "Print.listing": """Print event in listing (HepMC2) format.""",
    "ReaderAscii": """GenEvent I/O parsing for structured text files.""",
    "ReaderAscii.__init__": """Constructor.

The ctor to read from stream.

The ctor to read from stream. Useful for temp. streams.""",
    "ReaderAscii.close": """Close file stream.""",
    "ReaderAscii.failed": """Return status of the stream.""",
    "ReaderAscii.options": """Access options.""",
    "ReaderAscii.read_event": """Load event from file.

Parameters
----------
evt:
    Event to be filled.""",
    "ReaderAscii.skip": """skip events.""",
    "ReaderAsciiHepMC2": """Parser for HepMC2 I/O files.""",
    "ReaderAsciiHepMC2.__init__": """Default constructor.

The ctor to read from stream.

The ctor to read from temp stream.""",
    "ReaderAsciiHepMC2.close": """Close file stream.""",
    "ReaderAsciiHepMC2.failed": """Return status of the stream.""",
    "ReaderAsciiHepMC2.options": """Access options.""",
    "ReaderAsciiHepMC2.read_event": """Implementation of Reader::read_event.""",
    "ReaderAsciiHepMC2.skip": """skip events.""",
    "ReaderGZ": """GenEvent I/O parsing for compressed files.""",
    "ReaderGZ.__init__": """Constructor.

The ctor to read from stdin.""",
    "ReaderGZ.close": """Close file stream.""",
    "ReaderGZ.failed": """Return status of the stream.""",
    "ReaderGZ.options": """Access options.""",
    "ReaderGZ.read_event": """Load event from file.

Parameters
----------
evt:
    Event to be filled.""",
    "ReaderGZ.skip": """skip events.""",
    "ReaderHEPEVT": """GenEvent I/O parsing and serialization for HEPEVT files.""",
    "ReaderHEPEVT.__init__": """Default constructor.

The ctor to read from stream.

The ctor to read from temp stream.""",
    "ReaderHEPEVT.close": """Close file stream.""",
    "ReaderHEPEVT.failed": """Get stream error state.""",
    "ReaderHEPEVT.hepevtbuffer": """Pointer to HEPEVT Fortran common block/C struct.""",
    "ReaderHEPEVT.options": """Access options.""",
    "ReaderHEPEVT.read_event": """Read event from file.""",
    "ReaderHEPEVT.read_hepevt_event_header": """Find and read event header line from file.""",
    "ReaderHEPEVT.read_hepevt_particle": """read particle from file.

Parameters
----------
i:
    Particle id.""",
    "ReaderHEPEVT.skip": """skip events.""",
    "ReaderLHEF": """GenEvent I/O parsing and serialization for LHEF files.""",
    "ReaderLHEF.__init__": """The ctor to read from stream.

Constructor.

The ctor to read from temp stream.""",
    "ReaderLHEF.close": """Close.""",
    "ReaderLHEF.failed": """State.""",
    "ReaderLHEF.options": """Access options.""",
    "ReaderLHEF.read_event": """Reading event.""",
    "ReaderLHEF.skip": """skip events.""",
    "ReaderMT": """Multithreader GenEvent I/O parsing.""",
    "ReaderMT.close": """Close file and/or stream.""",
    "ReaderMT.failed": """Get file and/or stream error state.""",
    "ReaderMT.options": """Access options.""",
    "ReaderMT.read_event": """Fill next event from input into evt.""",
    "ReaderMT.skip": """skip or fast forward reading of some events.""",
    "Setup": """Configuration for HepMC.

Contains macro definitions for printing debug output, feature deprecation, etc. Static class - configuration is shared among all HepMC events and program threads.""",
    "Setup.DOUBLE_EPSILON": """Default threshold for comparing double variables.""",
    "Units": """Stores units-related enums and conversion functions.

Manages units used by HepMC::GenEvent.""",
    "Units.LengthUnit": """Position units.""",
    "Units.MomentumUnit": """Momentum units.""",
    "Units.convert": """Convert FourVector to different momentum unit.

Convert FourVector to different length unit.""",
    "Units.length_unit": """Get length unit based on its name.""",
    "Units.momentum_unit": """Get momentum unit based on its name.""",
    "Units.name": """Access name of momentum unit.

Access name of length unit.""",
    "WriterAscii": """GenEvent I/O serialization for structured text files.""",
    "WriterAscii.__init__": """Constructor.

If file already exists, it will be cleared before writing.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterAscii.close": """Close file stream.""",
    "WriterAscii.failed": """Return status of the stream.""",
    "WriterAscii.options": """Access options.""",
    "WriterAscii.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterAscii.write_run_info": """Write the GenRunInfo object to file.""",
    "WriterAsciiHepMC2": """GenEvent I/O serialization for structured text files.""",
    "WriterAsciiHepMC2.__init__": """Constructor.

If file already exists, it will be cleared before writing.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterAsciiHepMC2.close": """Close file stream.""",
    "WriterAsciiHepMC2.failed": """Return status of the stream.""",
    "WriterAsciiHepMC2.options": """Access options.""",
    "WriterAsciiHepMC2.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterAsciiHepMC2.write_run_info": """Write the GenRunInfo object to file.""",
    "WriterGZ": """GenEvent I/O serialization for compressed files.""",
    "WriterGZ.__init__": """Constructor.

If file already exists, it will be cleared before writing.

Constructor from ostream.""",
    "WriterGZ.close": """Close file stream.""",
    "WriterGZ.failed": """Return status of the stream.""",
    "WriterGZ.options": """Access options.""",
    "WriterGZ.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterHEPEVT": """GenEvent I/O serialization for HEPEVT files.""",
    "WriterHEPEVT.__init__": """Default constructor.

If file exists, it will be overwritten.

Constructor from ostream.

Constructor from temp ostream.""",
    "WriterHEPEVT.close": """Close file stream.""",
    "WriterHEPEVT.failed": """Get stream error state flag.""",
    "WriterHEPEVT.options": """Access options.""",
    "WriterHEPEVT.vertices_positions_present": """get flag if vertex positions are available. The flag is deduced from m_options. If the m_options have the key "vertices_positions_are_absent" the result if false. True otherwise.

set flag if vertex positions are available. Effectively this adds or removes key "vertices_positions_are_absent" to/from the m_options.""",
    "WriterHEPEVT.write_event": """Write event to file.

Parameters
----------
evt:
    Event to be serialized.""",
    "WriterHEPEVT.write_hepevt_event_header": """Write event header to file.""",
    "WriterHEPEVT.write_hepevt_particle": """Write particle to file.

Parameters
----------
index:
    Particle to be serializediflong:
    Format of record.""",
    "delta_eta": """Pseudorapidity separation.""",
    "delta_phi": """Signed azimuthal angle separation in [-pi, pi].""",
    "delta_r2_eta": """R_eta^2-distance separation dR^2 = dphi^2 + deta^2.""",
    "delta_r2_rap": """R_rap^2-distance separation dR^2 = dphi^2 + drap^2.""",
    "delta_r_eta": """R_eta-distance separation dR = sqrt(dphi^2 + deta^2).""",
    "delta_r_rap": """R-rap-distance separation dR = sqrt(dphi^2 + drap^2).""",
    "delta_rap": """Rapidity separation.""",
}
