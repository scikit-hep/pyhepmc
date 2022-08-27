from graphviz import Digraph
from pyhepmc._prettify import db as _prettify
from pyhepmc import Units
import numpy as np


def to_dot(evt, style=None):
    if evt.run_info:
        name = "\n".join(f"{t.name}-{t.version}" for t in evt.run_info.tools)
        name += "\n"
    else:
        name = ""
    name += f"event number = {evt.event_number}"

    d = Digraph(name=name)
    d.node_attr["shape"] = "point"
    d.graph_attr["rankdir"] = "LR"
    d.graph_attr["size"] = "8,100"

    GeV = 1 if evt.momentum_unit == Units.GEV else 1e3

    for v in evt.vertices:
        d.node(f"{v.id}", tooltip=f"{v.position} mm\nstatus = {v.status}")

    enmax = max(p.momentum.e / GeV for p in evt.particles)
    for p in evt.particles:
        en = p.momentum.e / GeV
        penwidth = str(max(0.5, 4 * en / enmax))

        unit = "GeV"
        if en > 1e2:
            en /= 1e3
            unit = "TeV"
        elif en < 1e-2:
            en *= 1e3
            unit = "MeV"

        color = "black"
        style = "solid"

        pname = _prettify.get(p.pid, None)
        if pname is None:
            if p.pid == 0:
                pname = "Invalid(0)"
                color = "gainsboro"
                penwidth = "7"
            else:
                pname = f"Internal({p.pid})"
                color = "dodgerblue"
                penwidth = "7"

        tooltip = f"{pname} [PDGID: {int(p.pid)}]"
        tooltip += f"\n{p.momentum} GeV"
        tooltip += f"\nm = {p.generated_mass:.4g} GeV"
        tooltip += f"\nstatus = {p.status}"

        try:
            from particle import Particle, ParticleNotFound, InvalidParticle

            pdb = Particle.from_pdgid(p.pid)
            quarks = pdb.quarks
            if quarks:
                tooltip += f"\nquarks = {quarks}"
            else:  # boson or lepton
                color = "goldenrod"
            tooltip += f"\nQ = {pdb.charge:.3g}"
            if pdb.ctau and np.isfinite(pdb.ctau):
                tooltip += f"\ncτ = {pdb.ctau:.3g} mm"
            if pdb.charge == 0:
                style = "dashed"
        except (ModuleNotFoundError, ParticleNotFound, InvalidParticle):
            pass

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
