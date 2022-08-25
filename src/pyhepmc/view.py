from graphviz import Digraph
from particle import Particle, ParticleNotFound, InvalidParticle
from pyhepmc._prettify import db as _prettify
from pyhepmc import Units
import numpy as np


def to_dot(evt, style=None):
    d = Digraph(name="event %i" % evt.event_number)
    d.node_attr["shape"] = "point"
    d.graph_attr["rankdir"] = "LR"
    d.graph_attr["size"] = "8,100"
    d.graph_attr["ratio"] = "compress"

    GeV = 1 if evt.momentum_unit == Units.GEV else 1e3

    for v in evt.vertices:
        d.node(f"{v.id}", tooltip=f"{v.position} mm\nstatus={v.status}")

    enmax = max(p.momentum.e / GeV for p in evt.particles)
    for p in evt.particles:
        style = "solid"

        en = p.momentum.e / GeV
        penwidth = str(max(0.5, 4 * en / enmax))

        unit = "GeV"
        if en > 1e2:
            en /= 1e3
            unit = "TeV"
        elif en < 1e-2:
            en *= 1e3
            unit = "MeV"

        try:
            pdb = Particle.from_pdgid(p.pid)
            pname = pdb.name
            pname = _prettify.get(pdb.pdgid, pname)
            tooltip = f"{pdb.name} [{int(pdb.pdgid)}]"
            quarks = pdb.quarks
            if quarks:
                tooltip += f"\n{quarks}"
            tooltip += f"\nQ = {pdb.charge:.3g}"
            if pdb.mass:
                tooltip += f"\nm = {pdb.mass:.4g} MeV/c2"
            if pdb.ctau and np.isfinite(pdb.ctau):
                tooltip += f"\ncτ = {pdb.ctau:.3g} mm"
            color = "black" if quarks else "goldenrod"
            # if not quarks:  # boson or lepton
            if pdb.charge == 0:
                style = "dashed"
        except ParticleNotFound:
            pname = f"Internal({p.pid})"
            tooltip = pname
            color = "dodgerblue"
            penwidth = "7"
        except InvalidParticle:
            pname = f"Invalid({p.pid})"
            tooltip = pname
            color = "gainsboro"
            penwidth = "7"

        label = f"{pname} {en:.2g} {unit}"

        if 1000 <= p.pid < 10000:  # diquark
            color = "black"

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

        if not p.production_vertex or p.production_vertex.id == 0 and p.end_vertex:
            # initial particle which is not also final state is beam particle
            edir = "forward"
        elif p.status == 1:  # final state
            edir = "forward"
        else:  # intermediate
            edir = "none"

        d.edge(
            vin,
            vout,
            dir=edir,
            label=label,
            color=color,
            style=style,
            tooltip=tooltip,
            labeltooltip=tooltip,
            penwidth=penwidth,
        )

    return d
