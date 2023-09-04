import pytest
import pyhepmc as hep
from numpy.testing import assert_equal
import numpy as np


def make_evt():
    r"""
    In this example we will generate the following event by hand

        name status pdg_id      parent Px       Py     Pz       Energy      Mass
     1  !p+!    1   2212        0,0    0.000    0.000  7000.000 7000.000    0.938
     2  !He4!   2   1000020040  0,0    0.000    0.000 -7000.000 7000.000    3.756
    =============================================================================
     3  !d!     3      1        1,1    0.750   -1.569    32.191   32.238    0.000
     4  !u~!    4     -2        2,2   -3.047  -19.000   -54.629   57.920    0.000
     5  !W-!    5    -24        3,4    1.517   -20.68   -20.605   85.925   80.799
     6  !gamma! 6     22        3,4   -3.813    0.113    -1.833    4.233    0.000
     7  !d!     7      1        5,5   -2.445   28.816     6.082   29.552    0.010
     8  !u~!    8     -2        5,5    3.962  -49.498   -26.687   56.373    0.006

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
    p2 = hep.GenParticle((0.0, 0.0, -7000.0, 7000.0), 1000020040, 2)
    p2.generated_mass = 3.756
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


@pytest.fixture()
def evt():
    return make_evt()


def test_GenHeavyIon():
    hi = hep.GenHeavyIon()
    assert hi == hep.GenHeavyIon()
    hi.Ncoll_hard = 3
    assert hi != hep.GenHeavyIon()


def test_GenParticle_as_attribute(evt):
    p = evt.particles[3]
    evt.attributes["foo"] = p
    assert evt.attributes == {"foo": p}


def test_GenCrossSection():
    cs = hep.GenCrossSection()
    cs.set_cross_section(1.2, 0.2, 3, 10)
    assert cs.event is None
    cs.set_xsec(0, 1.2)
    with pytest.raises(KeyError):
        cs.set_xsec_err("foo", 0.2)
    with pytest.raises(KeyError):
        cs.xsec("foo")
    assert cs.xsec(0) == 1.2
    assert cs.xsec_err(0) == 0.2
    assert cs.xsec() == 1.2
    with pytest.raises(IndexError):
        assert cs.xsec(1)

    ri = hep.GenRunInfo()
    ri.weight_names = ("foo", "bar")  # optional
    evt = hep.GenEvent()
    evt.run_info = ri
    evt.weights = [1.0, 2.0]
    evt.cross_section = cs
    assert evt.cross_section.event is evt
    cs = evt.cross_section
    cs.set_xsec("foo", 1.3)
    cs.set_xsec("bar", 2.3)
    assert cs.xsec("foo") == 1.3
    assert cs.xsec("bar") == 2.3
    assert cs.xsec(0) == 1.3
    assert cs.xsec(1) == 2.3
    with pytest.raises(IndexError):
        cs.xsec(2)
    with pytest.raises(KeyError):
        cs.xsec("baz")
    with pytest.raises(KeyError):
        cs.xsec_err("baz")


def test_attributes_1():
    ri = hep.GenRunInfo()
    att = ri.attributes
    assert att == {}
    assert len(att) == 0
    assert repr(att) == r"<RunInfoAttributesView>{}"
    att["foo"] = 1
    att["bar"] = "xy"
    att["baz"] = True
    assert att["foo"] == 1
    assert att["bar"] == "xy"
    assert att["baz"] is True
    assert att != {}
    assert att != {"foo": 2, "bar": "xy", "baz": True}
    assert att != {"foo": 1, "bra": "xy", "baz": True}
    with pytest.raises(KeyError):
        att["xyz"]
    assert len(att) == 3
    assert att == {"baz": True, "foo": 1, "bar": "xy"}
    # AttributeMapView has sorted keys
    assert repr(att) == r"<RunInfoAttributesView>{'bar': 'xy', 'baz': True, 'foo': 1}"

    del att["bar"]
    assert len(att) == 2
    assert att == {"baz": True, "foo": 1}

    keys = [k for k in att]
    assert keys == ["baz", "foo"]

    assert len(ri.attributes) == 2
    assert ri.attributes == att
    att.clear()
    assert len(att) == 0
    assert att == {}

    del ri
    # att should keep GenRunInfo alive through shared_ptr
    assert len(att) == 0


def test_attributes_2(evt):
    att = evt.attributes
    assert att == {}
    assert len(att) == 0
    assert repr(att) == r"<AttributesView>{}"
    att["foo"] = 1
    att["bar"] = "xy"
    att["baz"] = True
    assert att["foo"] == 1
    assert att["bar"] == "xy"
    assert att["baz"] is True
    with pytest.raises(KeyError):
        att["xyz"]
    assert len(att) == 3
    assert att == {"baz": True, "foo": 1, "bar": "xy"}
    # AttributeMapView has sorted keys
    assert repr(att) == r"<AttributesView>{'bar': 'xy', 'baz': True, 'foo': 1}"

    del att["bar"]
    assert len(att) == 2
    assert att == {"baz": True, "foo": 1}

    keys = [k for k in att]
    assert keys == ["baz", "foo"]

    assert len(evt.attributes) == 2
    assert evt.attributes == att
    att.clear()
    assert len(att) == 0
    assert att == {}


@pytest.mark.parametrize(
    "value",
    [
        True,
        2,
        1.5,
        "baz",
        [1, 2],
        ["foo", "bar"],
        [True, False],
        hep.GenCrossSection(),
        hep.GenHeavyIon(),
        hep.GenPdfInfo(),
        hep.HEPRUPAttribute(),
        hep.HEPEUPAttribute(),
    ],
)
def test_attributes_3(evt, value):
    if isinstance(value, hep.GenCrossSection):
        value.set_cross_section(1.2, 0.2, 3, 10)
    p1 = evt.particles[0]
    assert p1.id == 1
    assert p1.attributes == {}
    p1.attributes = {"foo": value}
    assert p1.attributes == {"foo": value}
    p1.attributes = {"bar": value}
    assert p1.attributes == {"bar": value}
    p1.attributes = {}
    assert p1.attributes == {}

    v1 = evt.vertices[0]
    assert v1.id != p1.id
    assert v1.attributes == {}
    v1.attributes = {"foo": value}
    assert v1.attributes == {"foo": value}
    v1.attributes = {"bar": value}
    assert v1.attributes == {"bar": value}
    v1.attributes = {}
    assert v1.attributes == {}


def test_FourVector():
    a = hep.FourVector(1, 2, 3, 4)
    b = hep.FourVector([1, 2, 3, 4])
    assert a == b

    with pytest.raises(ValueError):
        hep.FourVector([1, 2, 3])

    with pytest.raises(ValueError):
        hep.FourVector([1, 2, 3, 4, 5])


def test_GenPdfInfo(evt):
    pi = hep.GenPdfInfo()
    pi.parton_id1 = 211
    pi.parton_id2 = 2212
    pi.x1 = 0.5
    pi.x2 = 0.3
    assert pi.parton_id1 == 211
    assert pi.parton_id2 == 2212
    assert pi.x1 == 0.5
    assert pi.x2 == 0.3
    assert pi.scale == 0.0
    pi.scale = 1.2
    assert pi.scale == 1.2
    assert evt.pdf_info is None
    evt.pdf_info = pi
    assert evt.pdf_info == pi


def test_GenEvent(evt):
    for i, p in enumerate(evt.particles):
        assert p.status == i + 1

    p1, p2, p3, p4, *rest = evt.particles
    assert p1.pid == 2212
    assert p1.momentum == (0, 0, 7000, 7000)
    assert p1.generated_mass == 0.938
    assert p2.pid == 1000020040
    assert p2.generated_mass == 3.756
    assert p2.momentum == (0, 0, -7000, 7000)
    assert p3.parents == [p1]
    assert p3.momentum == (0.750, -1.569, 32.191, 32.238)
    assert p4.parents == [p2]
    assert p4.momentum == (-3.047, -19.0, -54.629, 57.920)


def test_GenEvent_generated_mass():
    p = hep.GenParticle((0.0, 0.0, 3.0, 5.0), 2212, 1)
    assert p.is_generated_mass_set() is False
    assert p.generated_mass == 4.0
    p.generated_mass = 2.3
    assert p.is_generated_mass_set() is True
    assert p.generated_mass == 2.3
    p.unset_generated_mass()
    assert p.generated_mass == 4.0


@pytest.mark.parametrize("use_parent", (True, False))
@pytest.mark.parametrize("fortran", (True, False))
def test_GenEvent_from_hepevt(use_parent, fortran, evt):
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

    # fortran style
    parents = [(0, 0), (0, 0), (1, 1), (2, 2), (3, 4), (3, 4), (5, 5), (5, 5)]
    children = [(3, 0), (4, 0), (5, 6), (5, 6), (7, 8), (0, 0), (0, 0), (0, 0)]

    if not fortran:
        parents = np.subtract(parents, 1)
        children = np.subtract(children, 1)

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
            fortran=fortran,
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
            fortran=fortran,
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
        "<GenEvent momentum_unit=1, length_unit=0, event_number=0, "
        "particles=1, vertices=1, run_info=None>"
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
    with pytest.raises(RuntimeError, match="no weight with given name"):
        evt.weight("foo")
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


def test_GenEventData(evt):
    ed = hep.GenEventData()
    evt.write_data(ed)

    assert len(ed.vertices) == 4
    a = ed.vertices
    assert_equal(a["status"], [v.status for v in evt.vertices])
    assert_equal(a["x"], [v.position.x for v in evt.vertices])
    assert_equal(a["z"], [v.position.z for v in evt.vertices])

    assert len(ed.particles) == 8
    b = ed.particles
    assert_equal(b["status"], [p.status for p in evt.particles])
    assert_equal(b["pid"], [p.pid for p in evt.particles])
    assert_equal(b["px"], [p.momentum.px for p in evt.particles])
    assert_equal(b["e"], [p.momentum.e for p in evt.particles])

    a["status"] = 2
    assert ed.vertices[0]["status"] == 2
    ed.particles["mass"] = 123
    assert ed.particles[0]["mass"] == 123

    evt2 = hep.GenEvent()
    evt2.read_data(ed)
    assert_equal([v.status for v in evt2.vertices], [2] * 4)
    assert_equal([p.generated_mass for p in evt2.particles], [123] * 8)


def test_numpy_api(evt):
    pids = evt.numpy.particles.pid
    assert_equal(pids, [p.pid for p in evt.particles])
    x = evt.numpy.vertices.x
    assert_equal(x, [v.position.x for v in evt.vertices])
