# flake8: noqa
from ._autodoc import autodoc as doc

override = {
    "Units": "Units in which HepMC3 stores momentum and position.",
    "GenParticle.generated_mass": """Get or set generated mass.

This function will return mass as set by a generator/tool. If not set, it will return momentum().m().""",
    "GenParticle.parents": """Convenience access to immediate incoming particles via production vertex.

Less efficient than via the vertex since return must be by value (in case there is no vertex).
""",
    "equal_vertex_sets": "Whether two sets of vertices are equal. The vertices can have arbitrary order and their id() is ignored in the comparison. The sets are considered equal, if each vertex in one set compares equal to another vertex in the other set.",
    "equal_particle_sets": "Whether two sets of particles are equal. Algorithm is analog to :func:`equal_vertex_sets`.",
    "GenCrossSection": """Stores additional information about cross-section.

This is an example of event attribute used to store cross-section information.

This class is meant to be used to pass, on an event by event basis, the current best guess of the total cross section. it is expected that the final cross section will be stored elsewhere.

Several cross sections and related info can be included in case of runs with multiple weights.

The units of cross-sections are expected to be pb.""",
    "GenParticle.id": "Number which uniquely identifies this particle in the current event. This is not a particle ID, see :attr:`pid` for the PDG ID. The id is a persistent pointer to this particle.",
    "GenVertex.id": "Number which uniquely identifies this vertex in the current event. The id is a persistent pointer to this vertex.",
    "GenParticle.pid": "PDG ID of particle",
    "GenParticle.abs_pid": "Equivalent to abs(genparticle.pid)",
    "GenParticle.is_generated_mass_set": "See :attr:`generated_mass`.",
    "GenParticle.unset_generated_mass": "Declare that generated mass is not set. See :attr:`generated_mass`.",
    "GenEvent.from_hepevt": """
    Convert HEPEVT record to GenEvent.

    GenEvent is cleared and then filled with the information provided in the argument arrays. Recovering the particle history only requires either parents or children.
    If both are not None, parents are used.

    All particle arrays must have equal length.

    Parameters
    ----------
    event_number: int
        Event number, starting with zero.
    px : array-like
        X-component of momentum of particles in GeV.
    py : array-like
        Y-component of momentum of particles in GeV.
    pz : array-like
        Z-component of momentum of particles in GeV.
    en : array-like
        Energy of particles in GeV.
    m : array-like
        Generated mass of particles in GeV.
    pid : array-like
        PDG IDs of particles.
    status: array-like
        Status codes of particles.
    parents: array-like or None, optional
        Array of int with shape (N, 2). Start and stop index (inclusive) in the record for the parents of each particle in Fortran numbering (starting with 1). No parents for a particle are indicated by the pair (0, 0) or (-1, -1). Single parents are indicated either by (N, 0) or (N, N) with N > 0.
    children: array-like or None, optional
        Like parents but for the children of this particle.
    vx : array-like or None, optional
        X-component of location of production vertex of particles in mm.
    vy : array-like or None, optional
        Y-component of location of production vertex of particles in mm.
    vz : array-like or None, optional
        Z-component of location of production vertex of particles in mm.
    vt : array-like or None, optional
        Time (ct) of production vertex of particles in mm.
    """,
    "GenEvent.weight": """Get event weight accessed by index (or the canonical/first one if there is no argument) or name.

    Access by weight name requires a :class:`GenRunInfo` attached to the event, otherwise this will throw an exception.

    It's the user's responsibility to ensure that the index or name exists!""",
    "GenEvent.set_weight": """Set event weight accessed by index (or the canonical/first one if there is no argument) or name.

    Access by weight name requires a :class:`GenRunInfo` attached to the event, otherwise this will throw an exception.

    It's the user's responsibility to ensure that the index or name exists!""",
    "GenEvent.vertices": "",
    "GenEvent.weight_names": """Get event weight names.

    Access requires a :class:`GenRunInfo` attached to the event, otherwise this will throw an exception.""",
    "GenEvent.weights": """Access event weight values as a sequence.

    Can be used to set multiple weights by assigning a sequence.
    """,
    "GenEvent.beams": """Access beam particles as a sequence.

    HepMC3 considers every particle as a beam particles, which does not have another ancestor particle. Therefore, this is a read-only property.
    """,
    "GenEvent.cross_section": """
    Access to the :class:`GenCrossSection`.

    If this attribute is not set, returns None.
    """,
    "GenEvent.heavy_ion": """
    Access to the :class:`GenHeavyIon`.

    If this attribute is not set, returns None.
    """,
    "GenEvent.heavy_ion": """
    Access to the :class:`GenHeavyIon`.

    If this attribute is not set, returns None.
    """,
    "GenEvent.run_info": """
    Access to the :class:`GenRunInfo`.

    If this attribute is not set, returns None.
    """,
    "GenEvent.pdf_info": """
    Access to the :class:`GenPdfInfo`.

    If this attribute is not set, returns None.
    """,
    "GenEvent.vertices": "Access list of vertices.",
    "attributes": """Access attributes with a dict-like view.

    It is possible to read and write attributes. Primitive C++ types (and vectors therefore) are converted from/to native Python types.
    """,
    "UnparsedAttribute": """Unparsed attribute after deserialization.

    HepMC3 does not serialize the type of attributes, therefore the correct
    type cannot be restored upon deserialization (this is a limition of the HepMC3 C++
    library and its serialization format). Use the :meth:`astype` method to parse the
    attribute into a concrete type; this has important side-effects, see method
    description.
    """,
    "UnparsedAttribute.astype": """
    Convert unparsed attribute to concrete type.

    If the conversion is successful, the unparsed attribute is replaced with the parsed
    attribute, so this method has to be called only once. If the conversion fails, a
    TypeError is raised.

    Parameters
    ----------
    pytype: type
        Type of the attribute. Allowed values: bool, int, float, str, GenParticle,
        GenPdfInfo, GenHeavyIon, GenCrossSection, HEPRUPAttribute, HEPEUPAttribute,
        typing.List[int], typing.List[float], typing.List[str]. In Python-3.9+,
        typing.List can be replaced by list.
    """,
}

doc.update(override)
