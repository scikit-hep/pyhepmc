import pytest
import pyhepmc_ng as hep
import numpy as np
import os


@pytest.fixture()
def evt():
    #
    # In this example we will place the following event into HepMC "by hand"
    #
    #     name status pdg_id  parent Px       Py    Pz       Energy      Mass
    #  1  !p+!    3   2212    0,0    0.000    0.000 7000.000 7000.000    0.938
    #  2  !p+!    3   2212    0,0    0.000    0.000-7000.000 7000.000    0.938
    #=========================================================================
    #  3  !d!     3      1    1,1    0.750   -1.569   32.191   32.238    0.000
    #  4  !u~!    3     -2    2,2   -3.047  -19.000  -54.629   57.920    0.000
    #  5  !W-!    3    -24    3,4    1.517   -20.68  -20.605   85.925   80.799
    #  6  !gamma! 1     22    3,4   -3.813    0.113   -1.833    4.233    0.000
    #  7  !d!     1      1    5,5   -2.445   28.816    6.082   29.552    0.010
    #  8  !u~!    1     -2    5,5    3.962  -49.498  -26.687   56.373    0.006

    # now we build the graph, which will looks like
    #                       p7                         #
    # p1                   /                           #
    #   \v1__p3      p5---v4                           #
    #         \_v3_/       \                           #
    #         /    \        p8                         #
    #    v2__p4     \                                  #
    #   /            p6                                #
    # p2                                               #
    #                                                  #

    #
    # Finally, the event gets a weight.
    #
    evt = hep.GenEvent(hep.Units.GEV, hep.Units.MM)
    evt.event_number = 1

    #                         px      py       pz        e   pdgid status
    p1 = hep.GenParticle((   0.0,    0.0,  7000.0,  7000.0), 2212,  1)
    p1.generated_mass = 0.938
    p2 = hep.GenParticle((   0.0,    0.0, -7000.0,  7000.0), 2212,  2)
    p2.generated_mass = 0.938
    p3 = hep.GenParticle(( 0.750, -1.569,  32.191,  32.238),    1,  3)
    p3.generated_mass = 0
    p4 = hep.GenParticle((-3.047,  -19.0, -54.629,  57.920),   -2,  4)
    p4.generated_mass = 0
    p5 = hep.GenParticle(( 1.517, -20.68, -20.605,  85.925),  -24,  5)
    p5.generated_mass = 80.799
    p6 = hep.GenParticle((-3.813,  0.113,  -1.833,   4.233),   22,  6)
    p6.generated_mass = 0
    p7 = hep.GenParticle((-2.445, 28.816,   6.082,  29.552),    1,  7)
    p7.generated_mass = 0.01
    p8 = hep.GenParticle(( 3.962,-49.498, -26.687,  56.373),   -2,  8)
    p8.generated_mass = 0.006
    evt.add_particle(p1)
    evt.add_particle(p2)
    evt.add_particle(p3)
    evt.add_particle(p4)
    evt.add_particle(p5)
    evt.add_particle(p6)
    evt.add_particle(p7)
    evt.add_particle(p8)

    # make sure vertex is not optimized away by WriterAscii
    v1 = hep.GenVertex((1.0, 1.0, 1.0, 1.0));
    v1.add_particle_in (p1)
    v1.add_particle_out(p3)
    evt.add_vertex(v1)

    # make sure vertex is not optimized away by WriterAscii
    v2 = hep.GenVertex((2.0, 2.0, 2.0, 2.0))
    v2.add_particle_in (p2)
    v2.add_particle_out(p4)
    evt.add_vertex(v2)

    # make sure vertex is not optimized away by WriterAscii
    v3 = hep.GenVertex((3.0, 3.0, 3.0, 3.0))
    v3.add_particle_in(p3)
    v3.add_particle_in(p4)
    v3.add_particle_out(p5)
    v3.add_particle_out(p6)
    evt.add_vertex(v3)

    # make sure vertex is not optimized away by WriterAscii
    v4 = hep.GenVertex((4.0, 4.0, 4.0, 4.0))
    v4.add_particle_in (p5)
    v4.add_particle_out(p7)
    v4.add_particle_out(p8)
    evt.add_vertex(v4)

    evt.weights = [1.0]
    evt.run_info = hep.GenRunInfo()
    evt.run_info.weight_names = ["0"]

    return evt


def prepare_hepevt(evt):
    particles = evt.particles
    h = hep.HEPEVT()
    h.event_number = evt.event_number
    h.nentries = len(evt.particles)
    pid = h.pid()
    sta = h.status()
    par = h.parents()
    chi = h.children()
    pm = h.pm()
    v = h.v()
    for i,p in enumerate(particles):
        sta[i] = p.status
        pid[i] = p.pid
        iparent = [q.id for q in p.parents]
        par[i] = (min(iparent), max(iparent)) if iparent else (0, 0)
        children = p.children
        ichildren = [q.id for q in children]
        chi[i] = (min(ichildren), max(ichildren)) if ichildren else (0, 0)
        pm[i,:4] = p.momentum
        pm[i,4] = p.generated_mass
        v[i] = p.production_vertex.position if p.production_vertex else (0, 0, 0, 0)
    return h


def test_hepevt(evt):
    particles = evt.particles

    h = prepare_hepevt(evt)
    assert h.event_number == evt.event_number
    assert h.nentries == len(evt.particles)
    pid = h.pid()
    sta = h.status()
    par = h.parents()
    chi = h.children()
    pm = h.pm()
    v = h.v()
    for i,p in enumerate(particles):
        assert sta[i] == p.status
        assert pid[i] == p.pid
        iparent = [q.id for q in p.parents]
        if iparent:
            assert tuple(par[i]) == (min(iparent), max(iparent))
        ichildren = [q.id for q in p.children]
        if ichildren:
            assert tuple(chi[i]) == (min(ichildren), max(ichildren))
        assert np.allclose(pm[i,:4], p.momentum)
        if p.production_vertex:
            assert np.allclose(v[i], p.production_vertex.position)
    assert str(h) == """ Event No.: 1
  Nr   Type   Parent(s)  Daughter(s)      Px       Py       Pz       E    Inv. M.
    1   2212   0 -    0     3 -    3     0.00     0.00  7000.00  7000.00     0.94
    2   2212   0 -    0     4 -    4     0.00     0.00 -7000.00  7000.00     0.94
    3      1   1 -    1     5 -    6     0.75    -1.57    32.19    32.24     0.00
    4     -2   2 -    2     5 -    6    -3.05   -19.00   -54.63    57.92     0.00
    5    -24   3 -    4     7 -    8     1.52   -20.68   -20.61    85.92    80.80
    6     22   3 -    4     0 -    0    -3.81     0.11    -1.83     4.23     0.00
    7      1   5 -    5     0 -    0    -2.44    28.82     6.08    29.55     0.01
    8     -2   5 -    5     0 -    0     3.96   -49.50   -26.69    56.37     0.01
"""


def test_sequence_access():
    evt = hep.GenEvent()
    evt.add_particle(hep.GenParticle())
    evt.particles[0].momentum = (1, 2, 3, 4)
    evt.particles[0].pid = 5
    evt.add_vertex(hep.GenVertex())
    evt.vertices[0].position = (1, 2, 3, 4)
    assert len(evt.particles) == 1
    assert evt.particles[0].id == 1
    assert evt.particles[0].pid == 5
    assert evt.particles[0].momentum == (1, 2, 3, 4)
    assert len(evt.vertices) == 1
    assert evt.vertices[0].id == -1
    assert evt.vertices[0].position == (1, 2, 3, 4)
    assert repr(evt) == "GenEvent(momentum_unit=1, length_unit=0, event_number=0, particles=[GenParticle(FourVector(1, 2, 3, 4), status=0, id=1, production_vertex=0, end_vertex=-1)], vertices=[GenVertex(FourVector(1, 2, 3, 4), status=0, id=-1, particles_in=[], particles_out=[])], run_info=None)"


def test_weights():
    evt = hep.GenEvent()
    assert evt.weights == []
    with pytest.raises(RuntimeError, match=".*requires the event to have a GenRunInfo"):
        evt.weight_names
    evt.run_info = hep.GenRunInfo()
    evt.run_info.weight_names = ["a", "b"]
    evt.weights = [2, 3]
    assert evt.weight(1) == 3
    assert evt.weight("a") == 2
    with pytest.raises(IndexError):
        evt.weight(2)
    with pytest.raises(RuntimeError, match="no weight with given name"):
        evt.set_weight("c", 4)


def test_fill_genevent_from_hepevt(evt):
    h = prepare_hepevt(evt)
    evt2 = hep.GenEvent()
    hep.fill_genevent_from_hepevt(evt2,
                                  h.event_number,
                                  h.pm()[:,:4] * 2,
                                  h.pm()[:,4] * 2,
                                  h.v() * 5,
                                  h.pid(),
                                  h.parents(),
                                  h.children(),
                                  h.status(),             # particle status
                                  np.zeros_like(h.pid()), # vertex status
                                  2, 5)
    # hepevt has no run_info, so we add it articially
    evt2.run_info = evt.run_info
    assert evt == evt2


def test_fill_genevent_from_hepevt_ptr(evt):
    h = prepare_hepevt(evt)
    evt2 = hep.GenEvent()
    hep.fill_genevent_from_hepevent_ptr(evt2, h.ptr, h.max_size)
    # hepevt has no run_info, so we add it articially
    evt2.run_info = evt.run_info
    assert evt == evt2
