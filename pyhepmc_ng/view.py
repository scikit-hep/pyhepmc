from graphviz import Digraph
from particletools.tables import PYTHIAParticleData
pdg = PYTHIAParticleData()


def to_dot(evt, style=None):
    d = Digraph(name="event %i" % evt.event_number)
    # d.graph_attr['rotate'] = '90'
    # d.graph_attr['splines'] = 'line'
    d.node_attr['shape'] = 'point'

    for v in evt.vertices:
        d.node('%i'%v.id)

    # additional nodes for incoming and outgoing particles
    vi = 0
    vo = 0
    for p in evt.particles:
        try:
            pname = pdg.name(p.pid)
        except:
            pname = "Unknown(%i)" % p.pid
        label = '%s\n%.2g GeV'%(pname, p.momentum.e/1e3)
        if not p.parents:
            vid = 'in_%i'%vi
            vi += 1
            d.node(vid, style='invis')
            assert p.end_vertex
            d.edge(vid, '%i'%p.end_vertex.id,
                   label=label)
            continue
        if not p.children:
            vid = 'out_%i'%vo
            vo += 1
            d.node(vid, style='invis')
            assert p.production_vertex
            d.edge('%i'%p.production_vertex.id, vid,
                   label=label)
            continue
        d.edge('%i'%p.production_vertex.id, '%i'%p.end_vertex.id,
               label=label)

    return d