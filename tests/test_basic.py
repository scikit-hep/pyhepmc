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
    p2 = hep.GenParticle((   0.0,    0.0, -7000.0,  7000.0), 2212,  2)
    p3 = hep.GenParticle(( 0.750, -1.569,  32.191,  32.238),    1,  3)
    p4 = hep.GenParticle((-3.047,  -19.0, -54.629,  57.920),   -2,  4)
    p5 = hep.GenParticle(( 1.517, -20.68, -20.605,  85.925),  -24,  5)
    p6 = hep.GenParticle((-3.813,  0.113,  -1.833,   4.233),   22,  6)
    p7 = hep.GenParticle((-2.445, 28.816,   6.082,  29.552),    1,  7)
    p8 = hep.GenParticle(( 3.962,-49.498, -26.687,  56.373),   -2,  8)
    evt.add_particle(p1)
    evt.add_particle(p2)
    evt.add_particle(p3)
    evt.add_particle(p4)
    evt.add_particle(p5)
    evt.add_particle(p6)
    evt.add_particle(p7)
    evt.add_particle(p8)

    v1 = hep.GenVertex();
    v1.add_particle_in (p1)
    v1.add_particle_out(p3)
    v1.status = 4 # make sure vertex is not optimized away by WriterAscii
    evt.add_vertex(v1)

    v2 = hep.GenVertex()
    v2.add_particle_in (p2)
    v2.add_particle_out(p4)
    v2.status = 4 # make sure vertex is not optimized away by WriterAscii
    evt.add_vertex(v2)

    v3 = hep.GenVertex()
    v3.add_particle_in(p3)
    v3.add_particle_in(p4)
    v3.add_particle_out(p5)
    v3.add_particle_out(p6)
    evt.add_vertex(v3)

    v4 = hep.GenVertex()
    v4.add_particle_in (p5)
    v4.status = 4 # make sure vertex is not optimized away by WriterAscii
    v4.add_particle_out(p7)
    v4.add_particle_out(p8)
    evt.add_vertex(v4)

    return evt


def prepare_hepevt():
    evt = prepare_event()
    particles = evt.particles

    h = hep.HEPEVT()
    h.event_number = 1
    h.nentries = 8
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

    h = prepare_hepevt()
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
    1   2212   0 -    0     3 -    3     0.00     0.00  7000.00  7000.00     0.00
    2   2212   0 -    0     4 -    4     0.00     0.00 -7000.00  7000.00     0.00
    3      1   1 -    1     5 -    6     0.75    -1.57    32.19    32.24     0.06
    4     -2   2 -    2     5 -    6    -3.05   -19.00   -54.63    57.92     0.34
    5    -24   3 -    4     7 -    8     1.52   -20.68   -20.61    85.92    80.80
    6     22   3 -    4     0 -    0    -3.81     0.11    -1.83     4.23     0.08
    7      1   5 -    5     0 -    0    -2.44    28.82     6.08    29.55    -0.10
    8     -2   5 -    5     0 -    0     3.96   -49.50   -26.69    56.37    -0.17
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
P 1 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 7.0000000000000000e+03 7.0000000000000000e+03 0.0000000000000000e+00 1
P 2 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 -7.0000000000000000e+03 7.0000000000000000e+03 0.0000000000000000e+00 2
V -1 4 [1]
P 3 -1 1 7.5000000000000000e-01 -1.5690000000000000e+00 3.2191000000000003e+01 3.2238000000000000e+01 6.2465990744549081e-02 3
V -2 4 [2]
P 4 -2 -2 -3.0470000000000002e+00 -1.9000000000000000e+01 -5.4628999999999998e+01 5.7920000000000002e+01 3.3845236001575724e-01 4
V -3 0 [3,4]
P 5 -3 -24 1.5169999999999999e+00 -2.0680000000000000e+01 -2.0605000000000000e+01 8.5924999999999997e+01 8.0799603408680156e+01 5
P 6 -3 22 -3.8130000000000002e+00 1.1300000000000000e-01 -1.8330000000000000e+00 4.2329999999999997e+00 8.1621075709617186e-02 6
V -4 4 [5]
P 7 -4 1 -2.4449999999999998e+00 2.8815999999999999e+01 6.0819999999999999e+00 2.9552000000000000e+01 -9.9503768772913739e-02 7
P 8 -4 -2 3.9620000000000002e+00 -4.9497999999999998e+01 -2.6687000000000001e+01 5.6372999999999998e+01 -1.7403447934355551e-01 8
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
    with hep.WriterAscii(oss) as f:
        f.write(evt1)

    evt2 = None
    with hep.ReaderAscii(oss) as f:
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
