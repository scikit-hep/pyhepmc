import pytest
import pyhepmc_ng as hep
import numpy as np


def prepare_event():
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
        ichildren = [q.id for q in p.children]
        chi[i] = (min(ichildren), max(ichildren)) if ichildren else (0, 0)
        pm[i,:4] = p.momentum
        pm[i,4] = p.generated_mass
        v[i] = p.production_vertex.position if p.production_vertex else (0, 0, 0, 0)
    return h


def test_hepevt():
    evt = prepare_event()
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
    evt.particles = (hep.GenParticle(),)
    evt.particles[0].momentum = (1, 2, 3, 4)
    evt.particles[0].pid = 5
    evt.vertices = (hep.GenVertex(),)
    evt.vertices[0].position = (1, 2, 3, 4)
    assert evt.particles == [hep.GenParticle((1, 2, 3, 4), 5),]
    assert evt.vertices == [hep.GenVertex((1, 2, 3, 4)),]


def test_read_write_stream():
    evt1 = prepare_event()

    oss = hep.stringstream()
    with hep.WriterAscii(oss) as f:
        f.write_event(evt1)

    assert str(oss) == """HepMC::Version 3.0.0
HepMC::IO_GenEvent-START_EVENT_LISTING
E 1 4 8
U GEV MM
P 1 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 7.0000000000000000e+03 7.0000000000000000e+03 9.3799999999999994e-01 1
P 2 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 -7.0000000000000000e+03 7.0000000000000000e+03 9.3799999999999994e-01 2
V -1 0 [1] @ 1.0000000000000000e+00 1.0000000000000000e+00 1.0000000000000000e+00 1.0000000000000000e+00
P 3 -1 1 7.5000000000000000e-01 -1.5690000000000000e+00 3.2191000000000003e+01 3.2238000000000000e+01 0.0000000000000000e+00 3
V -2 0 [2] @ 2.0000000000000000e+00 2.0000000000000000e+00 2.0000000000000000e+00 2.0000000000000000e+00
P 4 -2 -2 -3.0470000000000002e+00 -1.9000000000000000e+01 -5.4628999999999998e+01 5.7920000000000002e+01 0.0000000000000000e+00 4
V -3 0 [3,4] @ 3.0000000000000000e+00 3.0000000000000000e+00 3.0000000000000000e+00 3.0000000000000000e+00
P 5 -3 -24 1.5169999999999999e+00 -2.0680000000000000e+01 -2.0605000000000000e+01 8.5924999999999997e+01 8.0799000000000007e+01 5
P 6 -3 22 -3.8130000000000002e+00 1.1300000000000000e-01 -1.8330000000000000e+00 4.2329999999999997e+00 0.0000000000000000e+00 6
V -4 0 [5] @ 4.0000000000000000e+00 4.0000000000000000e+00 4.0000000000000000e+00 4.0000000000000000e+00
P 7 -4 1 -2.4449999999999998e+00 2.8815999999999999e+01 6.0819999999999999e+00 2.9552000000000000e+01 1.0000000000000000e-02 7
P 8 -4 -2 3.9620000000000002e+00 -4.9497999999999998e+01 -2.6687000000000001e+01 5.6372999999999998e+01 6.0000000000000001e-03 8
HepMC::IO_GenEvent-END_EVENT_LISTING

"""

    evt2 = hep.GenEvent()
    assert evt1 != evt2
    with hep.ReaderAscii(oss) as f:
        f.read_event(evt2)

    assert evt1.particles == evt2.particles
    assert evt1.vertices == evt2.vertices
    assert evt1 == evt2


def test_pythonic_read_write():
    evt1 = prepare_event()

    oss = hep.stringstream()
    with hep.open(oss, "w") as f:
        f.write(evt1)

    evt2 = None
    with hep.open(oss) as f:
        evt2 = f.read()

    assert evt1.particles == evt2.particles
    assert evt1.vertices == evt2.vertices
    assert evt1 == evt2


def test_failed_read_file():
    with pytest.raises(IOError):
        with hep.ReaderAscii("test_failed_read_file.dat") as f:
            f.read()


def test_read_empty_stream():
    oss = hep.stringstream()
    with hep.ReaderAscii(oss) as f:
        evt = hep.GenEvent()
        ok = f.read_event(evt)
        assert ok == True # reading empty stream is ok in HepMC


def test_read_write_file():
    evt1 = prepare_event()

    with hep.WriterAscii("test_read_write_file.dat") as f:
        f.write_event(evt1)

    evt2 = hep.GenEvent()
    assert evt1 != evt2
    with hep.ReaderAscii("test_read_write_file.dat") as f:
        ok = f.read_event(evt2)
        assert ok

    assert evt1.particles == evt2.particles
    assert evt1.vertices == evt2.vertices
    assert evt1 == evt2

    import os
    os.unlink("test_read_write_file.dat")


def test_fill_genevent_from_hepevt():
    evt1 = prepare_event()
    h = prepare_hepevt(evt1)
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
    assert evt1.particles == evt2.particles
    assert evt1.vertices == evt2.vertices
    assert evt1 == evt2


def test_fill_genevent_from_hepevt_ptr():
    evt1 = prepare_event()
    h = prepare_hepevt(evt1)
    evt2 = hep.GenEvent()
    hep.fill_genevent_from_hepevent_ptr(evt2, h.ptr, h.max_size)
    assert evt1.particles == evt2.particles
    assert evt1.vertices == evt2.vertices
    assert evt1 == evt2
