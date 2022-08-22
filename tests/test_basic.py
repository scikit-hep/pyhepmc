import pytest
import pyhepmc as hep


@pytest.fixture()
def evt():
    r"""
    In this example we will generate the following event by hand

        name status pdg_id  parent Px       Py     Pz       Energy      Mass
     1  !p+!    1   2212    0,0    0.000    0.000  7000.000 7000.000    0.938
     2  !p+!    2   2212    0,0    0.000    0.000 -7000.000 7000.000    0.938
    =========================================================================
     3  !d!     3      1    1,1    0.750   -1.569    32.191   32.238    0.000
     4  !u~!    4     -2    2,2   -3.047  -19.000   -54.629   57.920    0.000
     5  !W-!    5    -24    3,4    1.517   -20.68   -20.605   85.925   80.799
     6  !gamma! 6     22    3,4   -3.813    0.113    -1.833    4.233    0.000
     7  !d!     7      1    5,5   -2.445   28.816     6.082   29.552    0.010
     8  !u~!    8     -2    5,5    3.962  -49.498   -26.687   56.373    0.006

    The corresponding graph looks like this

                           p7
     p1                   /
       \v1__p3      p5---v4
             \_v3_/       \
             /    \        p8
        v2__p4     \
       /            p6
     p2

    Finally, the event gets a weight.
    """
    evt = hep.GenEvent(hep.Units.GEV, hep.Units.MM)
    evt.event_number = 1

    #                     px   py   pz      e        pdgid status
    p1 = hep.GenParticle((0.0, 0.0, 7000.0, 7000.0), 2212, 1)
    p1.generated_mass = 0.938
    p2 = hep.GenParticle((0.0, 0.0, -7000.0, 7000.0), 2212, 2)
    p2.generated_mass = 0.938
    p3 = hep.GenParticle((0.750, -1.569, 32.191, 32.238), 1, 3)
    p3.generated_mass = 0
    p4 = hep.GenParticle((-3.047, -19.0, -54.629, 57.920), -2, 4)
    p4.generated_mass = 0
    p5 = hep.GenParticle((1.517, -20.68, -20.605, 85.925), -24, 5)
    p5.generated_mass = 80.799
    p6 = hep.GenParticle((-3.813, 0.113, -1.833, 4.233), 22, 6)
    p6.generated_mass = 0
    p7 = hep.GenParticle((-2.445, 28.816, 6.082, 29.552), 1, 7)
    p7.generated_mass = 0.01
    p8 = hep.GenParticle((3.962, -49.498, -26.687, 56.373), -2, 8)
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
    v1 = hep.GenVertex((1.0, 1.0, 1.0, 1.0))
    v1.add_particle_in(p1)
    v1.add_particle_out(p3)
    evt.add_vertex(v1)

    # make sure vertex is not optimized away by WriterAscii
    v2 = hep.GenVertex((2.0, 2.0, 2.0, 2.0))
    v2.add_particle_in(p2)
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
    v4.add_particle_in(p5)
    v4.add_particle_out(p7)
    v4.add_particle_out(p8)
    evt.add_vertex(v4)

    evt.weights = [1.0]

    ti = hep.GenRunInfo.ToolInfo("dummy", "1.0", "dummy generator")
    ri = hep.GenRunInfo()
    ri.tools = [ti]
    ri.weight_names = ["0"]
    evt.run_info = ri

    return evt


def test_GenEvent(evt):
    for i, p in enumerate(evt.particles):
        assert p.status == i + 1

    p1, p2, p3, p4, *rest = evt.particles
    assert p1.pid == 2212
    assert p1.momentum == (0, 0, 7000, 7000)
    assert p2.pid == 2212
    assert p2.momentum == (0, 0, -7000, 7000)
    assert p3.parents == [p1]
    assert p3.momentum == (0.750, -1.569, 32.191, 32.238)
    assert p4.parents == [p2]
    assert p4.momentum == (-3.047, -19.0, -54.629, 57.920)


@pytest.mark.parametrize("use_parent", (True, False))
def test_GenEvent_from_hepevt(use_parent, evt):
    status = [p.status for p in evt.particles]
    pid = [p.pid for p in evt.particles]
    px = [p.momentum[0] for p in evt.particles]
    py = [p.momentum[1] for p in evt.particles]
    pz = [p.momentum[2] for p in evt.particles]
    en = [p.momentum[3] for p in evt.particles]
    m = [p.generated_mass for p in evt.particles]
    vx = vy = vz = vt = [0, 0, 1, 2, 3, 3, 4, 4]

    assert len(m) == 8

    #                           p7
    #     p1                   /
    #       \v1__p3      p5---v4
    #             \_v3_/       \
    #             /    \        p8
    #        v2__p4     \
    #       /            p6
    #     p2

    parents = [(0, 0), (0, 0), (1, 1), (2, 2), (3, 4), (3, 4), (5, 5), (5, 5)]
    children = [(3, 0), (4, 0), (5, 6), (5, 6), (7, 8), (0, 0), (0, 0), (0, 0)]

    ev = hep.GenEvent()
    if use_parent:
        ev.from_hepevt(
            evt.event_number,
            px,
            py,
            pz,
            en,
            m,
            pid,
            status,
            parents,
            None,
            vx,
            vy,
            vz,
            vt,
        )
    else:
        ev.from_hepevt(
            evt.event_number,
            px,
            py,
            pz,
            en,
            m,
            pid,
            status,
            None,
            children,
            vx,
            vy,
            vz,
            vt,
        )

    # cannot be taken from HepEvt record, but is set for evt
    ev.weights = [1.0]
    ev.run_info = evt.run_info

    assert len(ev.particles) == len(evt.particles)
    assert ev.particles == evt.particles
    assert len(ev.vertices) == len(evt.vertices)
    assert hep.equal_vertex_sets(ev.vertices, evt.vertices)
    assert ev == evt


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
    assert repr(evt) == (
        "GenEvent(momentum_unit=1, length_unit=0, event_number=0, "
        "particles=[GenParticle(FourVector(1, 2, 3, 4), pid=5, status=0)], "
        "vertices=[GenVertex(FourVector(1, 2, 3, 4))], run_info=None)"
    )


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


def test_GenParticle_repr():
    p = hep.GenParticle([1, 2, 3, 4], pid=211, status=2)
    assert repr(p) == "GenParticle(FourVector(1, 2, 3, 4), pid=211, status=2)"


def test_GenVertex_repr():
    p = hep.GenVertex([1, 2, 3, 4])
    assert repr(p) == "GenVertex(FourVector(1, 2, 3, 4))"
