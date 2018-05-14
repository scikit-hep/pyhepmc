import pyhepmc_ng as hep
import pytest


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
    #   \v1__p2      p5---v4                           #
    #         \_v3_/       \                           #
    #         /    \        p8                         #
    #    v2__p4     \                                  #
    #   /            p6                                #
    # p3                                               #
    #                                                  #
    evt = hep.GenEvent(hep.Units.GEV, hep.Units.MM)

    #                           px      py        pz       e      pdgid status
    p1 = hep.GenParticle( ( 0.0,    0.0,   7000.0,  7000.0  ), 2212,  3 )
    p2 = hep.GenParticle( ( 0.750, -1.569,   32.191,  32.238),    1,  3 )
    p3 = hep.GenParticle( ( 0.0,    0.0,  -7000.0,  7000.0  ), 2212,  3 )
    p4 = hep.GenParticle( (-3.047,-19.0,    -54.629,  57.920),   -2,  3 )

    v1 = hep.GenVertex();
    v1.add_particle_in (p1)
    v1.add_particle_out(p2)
    evt.add_vertex(v1)
    v1.status = 4 # make sure vertex is not optimized away by WriterAscii

    v2 = hep.GenVertex()
    v2.add_particle_in (p3)
    v2.add_particle_out(p4)
    evt.add_vertex(v2)
    v2.status = 4 # make sure vertex is not optimized away by WriterAscii

    v3 = hep.GenVertex()
    v3.add_particle_in(p2)
    v3.add_particle_in(p4)
    evt.add_vertex(v3)

    p5 = hep.GenParticle( ( 1.517,-20.68, -20.605,85.925), -24, 3 )
    p6 = hep.GenParticle( (-3.813,  0.113, -1.833, 4.233),  22, 1 )

    v3.add_particle_out(p5)
    v3.add_particle_out(p6)

    v4 = hep.GenVertex()
    v4.add_particle_in (p5)
    evt.add_vertex(v4)
    v4.status = 4 # make sure vertex is not optimized away by WriterAscii

    p7 = hep.GenParticle( (-2.445, 28.816,  6.082,29.552),  1, 1 )
    p8 = hep.GenParticle( ( 3.962,-49.498,-26.687,56.373), -2, 1 )

    v4.add_particle_out(p7)
    v4.add_particle_out(p8)
    return evt


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
E 0 4 8
U GEV MM
P 1 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 7.0000000000000000e+03 7.0000000000000000e+03 0.0000000000000000e+00 3
V -1 4 [1]
P 2 -1 1 7.5000000000000000e-01 -1.5690000000000000e+00 3.2191000000000003e+01 3.2238000000000000e+01 6.2465990744549081e-02 3
P 3 0 2212 0.0000000000000000e+00 0.0000000000000000e+00 -7.0000000000000000e+03 7.0000000000000000e+03 0.0000000000000000e+00 3
V -2 4 [3]
P 4 -2 -2 -3.0470000000000002e+00 -1.9000000000000000e+01 -5.4628999999999998e+01 5.7920000000000002e+01 3.3845236001575724e-01 3
V -3 0 [2,4]
P 5 -3 -24 1.5169999999999999e+00 -2.0680000000000000e+01 -2.0605000000000000e+01 8.5924999999999997e+01 8.0799603408680156e+01 3
P 6 -3 22 -3.8130000000000002e+00 1.1300000000000000e-01 -1.8330000000000000e+00 4.2329999999999997e+00 8.1621075709617186e-02 1
V -4 4 [5]
P 7 -4 1 -2.4449999999999998e+00 2.8815999999999999e+01 6.0819999999999999e+00 2.9552000000000000e+01 -9.9503768772913739e-02 1
P 8 -4 -2 3.9620000000000002e+00 -4.9497999999999998e+01 -2.6687000000000001e+01 5.6372999999999998e+01 -1.7403447934355551e-01 1
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
