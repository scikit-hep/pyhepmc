from graphviz import Digraph
from particle import Particle, ParticleNotFound, InvalidParticle
from pyhepmc._prettify import db as _prettify
from pyhepmc import Units
import numpy as np


def to_dot(evt, style=None):
    d = Digraph(name="event %i" % evt.event_number)
    d.node_attr["shape"] = "point"
    d.graph_attr["rankdir"] = "LR"
    d.graph_attr["size"] = "7,7"
    d.graph_attr["ratio"] = "compress"

    GeV = 1 if evt.momentum_unit == Units.GEV else 1e3
    gray = "#a0a0a0"

    for v in evt.vertices:
        d.node(f"{v.id}", height="0.02", color=gray, tooltip=f"status={v.status}")

    for p in evt.particles:
        try:
            pdb = Particle.from_pdgid(p.pid)
            charge = pdb.charge
            pname = pdb.name
            pname = _prettify.get(pdb.pdgid, pname)
            tooltip = pdb.name
            if pdb.quarks:
                tooltip += f" ({pdb.quarks})"
            tooltip += f"\nQ = {pdb.charge:.3g}"
            if pdb.mass:
                tooltip += f"\nm = {pdb.mass:.4g} MeV/c2"
            if pdb.ctau and np.isfinite(pdb.ctau):
                tooltip += f"\ncτ = {pdb.ctau:.3g} mm"
        except ParticleNotFound:
            pname = f"Internal({p.pid})"
            charge = 0
            tooltip = pname
        except InvalidParticle:
            pname = f"Invalid({p.pid})"
            charge = 0
            tooltip = pname
        en = p.momentum.e / GeV
        unit = "GeV"
        if en > 1e2:
            en /= 1e3
            unit = "TeV"
        elif en < 1e-2:
            en *= 1e3
            unit = "MeV"

        label = f"{pname} {en:.2g} {unit}"

        # do not connect initial particles to root vertex
        if p.production_vertex and p.production_vertex.id != 0:
            vin = f"{p.production_vertex.id}"
        else:
            vin = f"in_{p.id}"
            d.node(vin, style="invis")

        if p.end_vertex:
            vout = f"{p.end_vertex.id}"
        else:
            vout = f"out_{p.id}"
            d.node(vout, style="invis")

        style = "solid" if charge else "dashed"
        if not p.production_vertex or p.production_vertex.id == 0 and p.end_vertex:
            # initial particle which is not also final state is beam particle
            style = "bold"
            edir = "forward"
            color = None
        elif p.status == 1:  # final state
            edir = "forward"
            color = None
        else:  # intermediate
            edir = "none"
            color = gray

        d.edge(
            vin,
            vout,
            label=label,
            dir=edir,
            style=style,
            color=color,
            fontcolor=color,
            tooltip=tooltip,
            labeltooltip=tooltip,
        )

    return d
