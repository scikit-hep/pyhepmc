from __future__ import print_function
from . cpp import *


def print_tree(event):
    momentum_unit = event.momentum_unit
    momentum_unit_value = 1.0 if momentum_unit == Units.GEV else 1e3
    def visitor(level, p, momentum_unit):
        indent = "  " * level
        v = p.end_vertex
        if v:
            pin = v.particles_in
        else:
            pin = [p]
        s = "+".join(("p[%i](%i, %.3g, %.3g)"%(p.id, p.pid, p.momentum.z/momentum_unit, p.momentum.e/momentum_unit) for p in pin))
        print(indent+s)
        for pi in p.children:
            visitor(level + 1, pi, momentum_unit)

    for p in event.particles:
        if len(p.parents) == 0:
            visitor(0, p, momentum_unit_value)

