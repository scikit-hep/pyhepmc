# flake8: noqa
from ._autodoc import autodoc as doc

override = {
    "Units": "Units in which HepMC3 stores momentum and position.",
    "GenParticle.end_vertex": "Get end vertex.",
    "GenParticle.generated_mass": """Get or set generated mass.

This function will return mass as set by a generator/tool. If not set, it will return momentum().m().""",
    "GenParticle.parents": """Convenience access to immediate incoming particles via production vertex.

Less efficient than via the vertex since return must be by value (in case there is no vertex).
""",
}

doc.update(override)
