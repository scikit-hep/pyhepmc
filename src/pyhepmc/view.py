from graphviz import Digraph
from particle import Particle, ParticleNotFound
from pyhepmc._prettify import db as _prettify
from pyhepmc import Units


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

    vi = 0
    vo = 0
    for p in evt.particles:
        try:
            pdb = Particle.from_pdgid(p.pid)
            charge = pdb.charge
            pname = pdb.name
            pname = _prettify.get(pdb.pdgid, pname)
            tooltip = str(pdb)
        except ParticleNotFound:
            pname = f"Internal({p.pid})"
            charge = 0
            tooltip = ""
        en = p.momentum.e / GeV
        unit = "GeV"
        if en > 1e2:
            en /= 1e3
            unit = "TeV"
        elif en < 1e-2:
            en *= 1e3
            unit = "MeV"

        label = f" {pname} {en:.2g} {unit}"
        style = "solid" if charge else "dashed"
        if not p.parents:  # initial particles
            vid = f"in_{vi}"
            vi += 1
            d.node(vid, style="invis")
            assert p.end_vertex
            d.edge(
                vid,
                f"{p.end_vertex.id}",
                label=label,
                arrowsize="1",
                style="bold",
                tooltip=tooltip,
            )
        elif not p.children:  # final state particles
            vid = f"out_{vo}"
            vo += 1
            d.node(vid, style="invis")
            assert p.production_vertex
            d.edge(
                f"{p.production_vertex.id}",
                vid,
                label=label,
                style=style,
                tooltip=tooltip,
            )
        else:
            # intermediate particles
            d.edge(
                f"{p.production_vertex.id}",
                f"{p.end_vertex.id}",
                label=label,
                color=gray,
                fontcolor=gray,
                style=style,
                dir="none",
                tooltip=tooltip,
            )

    return d
