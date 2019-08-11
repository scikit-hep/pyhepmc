#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include "HepMC3/FourVector.h"
#include "HepMC3/GenHeavyIon.h"
#include "HepMC3/GenPdfInfo.h"
#include "HepMC3/GenCrossSection.h"
#include "HepMC3/GenRunInfo.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/GenVertex.h"
#include "HepMC3/Units.h"
#include "HepMC3/Print.h"
#include "HepMC3/WriterAscii.h"
#include "HepMC3/ReaderAscii.h"
#include "HepMC3/ReaderAsciiHepMC2.h"
#include "HepMC3/HEPEVT_Wrapper.h"
#include <memory>
#include <vector>
#include <algorithm>
#include <cmath>
#include <map>
#include <sstream>
#include <stdexcept>
#include <functional>

#include "hepevt_wrapper.h"
// #include "GzReaderAscii.h"

template <class Iterator, class Streamer>
std::ostream& ostream_range(std::ostream& os,
  Iterator begin, Iterator end, Streamer streamer,
  const char bracket_left = '[',
  const char bracket_right=']') {
  os << bracket_left;
  bool first = true;
  for (; begin != end; ++begin) {
    if (first) { first = false; }
    else { os << ", "; }
    streamer(os, begin);
  }
  os << bracket_right;
  return os;
}

namespace HepMC3 {

using GenRunInfoPtr = std::shared_ptr<GenRunInfo>;

// equality comparions used by unit tests
bool is_close(const FourVector& a, const FourVector& b,
              double rel_eps = 1e-7) {
    auto is_close = [rel_eps](double a, double b) {
            return std::abs(a-b) < rel_eps;
        };
    return is_close(a.x(), b.x()) &&
        is_close(a.y(), b.y()) &&
        is_close(a.z(), b.z()) &&
        is_close(a.t(), b.t());
}

bool operator==(const GenParticle& a, const GenParticle& b) {
    return a.id() == b.id() && a.pid() == b.pid() &&
        a.status() == b.status() && is_close(a.momentum(), b.momentum());
}

bool operator!=(const GenParticle& a, const GenParticle& b) {
  return !operator==(a, b);
}

bool operator==(const GenVertex& a, const GenVertex& b) {
    auto equal_id = [](ConstGenParticlePtr a,
                       ConstGenParticlePtr b) { return a->id() == b->id(); };
    return a.id() == b.id() && a.status() == b.status() &&
        is_close(a.position(), b.position()) &&
        a.particles_in().size() == b.particles_in().size() &&
        a.particles_out().size() == b.particles_out().size() &&
        std::equal(a.particles_in().begin(), a.particles_in().end(),
                   b.particles_in().begin(), equal_id) &&
        std::equal(a.particles_out().begin(), a.particles_out().end(),
                   b.particles_out().begin(),
                   equal_id);
}

bool operator!=(const GenVertex& a, const GenVertex& b) {
  return !operator==(a, b);
}

bool operator==(const GenRunInfo::ToolInfo& a,
                const GenRunInfo::ToolInfo& b) {
    return a.name == b.name &&
        a.version == b.version &&
        a.description == b.description;
}

bool operator!=(const GenRunInfo::ToolInfo& a, const GenRunInfo::ToolInfo& b) {
  return !operator==(a, b);
}

bool operator==(const GenRunInfo& a, const GenRunInfo& b) {
  const auto a_attr = a.attributes();
  const auto b_attr = b.attributes();
  return a.tools().size() == b.tools().size() &&
    a.weight_names().size() == b.weight_names().size() &&
    a_attr.size() == b_attr.size() &&
    std::equal(a.tools().begin(), a.tools().end(), b.tools().begin()) &&
    std::equal(a.weight_names().begin(), a.weight_names().end(), b.weight_names().begin()) &&
    std::equal(a_attr.begin(), a_attr.end(), b_attr.begin(), [](const std::pair<std::string, std::shared_ptr<Attribute>>& a, const std::pair<std::string, std::shared_ptr<Attribute>>& b) {
      if (a.first != b.first)
        return false;
      if (bool(a.second) != bool(b.second))
        return false;
      if (!a.second)
        return true;
      std::string sa, sb;
      a.second->to_string(sa);
      b.second->to_string(sb);        
      return sa == sb;
    });
}

bool operator!=(const GenRunInfo& a, const GenRunInfo& b) {
  return !operator==(a, b);
}

bool operator==(const GenEvent& a, const GenEvent& b) {
    // incomplete:
    // missing comparison of GenHeavyIon, GenPdfInfo, GenCrossSection

    if (a.event_number() != b.event_number() ||
        a.momentum_unit() != b.momentum_unit() ||
        a.length_unit() != b.length_unit())
        return false;

    // run_info may be missing
    if (a.run_info() && b.run_info()) {
      if (!(*a.run_info() == *b.run_info()))
        return false;
    } else if (!a.run_info() && b.run_info()) {
      if (*b.run_info() != GenRunInfo())
        return false;
    } else if (a.run_info() && !b.run_info()) {
      if (*a.run_info() != GenRunInfo())
        return false;
    }

    const auto& ap = a.particles();
    const auto& bp = b.particles();
    const auto& av = a.vertices();
    const auto& bv = b.vertices();

    return ap.size() == bp.size() && av.size() == bv.size() &&
    std::equal(ap.begin(), ap.end(), bp.begin(),
      [](decltype(*ap.begin()) a, decltype(*bp.begin()) b) {
        return *a == *b;
      }) &&
    std::equal(av.begin(), av.end(), bv.begin(),
      [](decltype(*av.begin()) a, decltype(*bv.begin()) b) {
        return *a == *b;
      });
}

bool operator!=(const GenEvent& a, const GenEvent& b) {
  return !operator==(a, b);
}

template <class T>
std::ostream& repr(std::ostream& os, const std::shared_ptr<T>& x) {
  if (x)
    repr(os, *x.get());
  else
    os << "None";
  return os;
}

inline std::ostream& repr(std::ostream& os, const std::string& s) {
  os << "'" << s << "'";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::Attribute& a) {
  std::string s;
  a.to_string(s);
  os << s;
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenRunInfo::ToolInfo& x) {
  os << "ToolInfo(name=";
  repr(os, x.name) << ", version=";
  repr(os, x.version) << ", description=";
  repr(os, x.description) << ")";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::FourVector& x) {
  os << "FourVector("
     << x.x() << ", "
     << x.y() << ", "
     << x.z() << ", "
     << x.t() << ")";
  return os;
}

template <class T, class A>
std::ostream& repr(std::ostream& os, const std::vector<T, A>& v) {
  return ostream_range(os, v.begin(), v.end(),
    [](std::ostream& os, typename std::vector<T, A>::const_iterator it) {
      repr(os, *it);
    });
}

template <class K, class V, class... Ts>
std::ostream& repr(std::ostream& os, const std::map<K, V, Ts...>& m) {
  return ostream_range(os, m.begin(), m.end(), [](std::ostream& os, typename std::map<K, V, Ts...>::const_iterator it) {
    os << it->first << ": ";
    repr(os, it->second);
  }, '{', '}');
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenRunInfo& x) {
  os << "GenRunInfo(tools=";
  repr(os, x.tools()) << ", weight_names=";
  repr(os, x.weight_names()) << ", attributes=";
  repr(os, x.attributes()) << ")";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenParticle& x) {
  os << "GenParticle(";
  repr(os, x.momentum());
  if (x.is_generated_mass_set())
    os << ", mass=" << x.data().mass;
  os << ", status="
     << x.status() << ", id="
     << x.id() << ", production_vertex="
     << (x.production_vertex() ? x.production_vertex()->id() : -1)
     << ", end_vertex="
     << (x.end_vertex() ? x.end_vertex()->id() : -1)
     << ")";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenVertex& x) {
  os << "GenVertex(";
  repr(os, x.position());
  os << ", status="
     << x.status() << ", id="
     << x.id();
  ostream_range(os << ", particles_in=",
    x.particles_in().begin(), x.particles_in().end(),
    [](std::ostream& os, decltype(x.particles_in().begin()) it) {
      os << it->get()->id();
    }
  );
  ostream_range(os << ", particles_out=",
    x.particles_out().begin(), x.particles_out().end(),
    [](std::ostream& os, decltype(x.particles_in().begin()) it) {
      os << it->get()->id();
    }
  );
  os << ")";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenEvent& x) {
  // incomplete:
  // missing comparison of GenHeavyIon, GenPdfInfo, GenCrossSection

  os << "GenEvent("
     << "momentum_unit=" << x.momentum_unit() << ", "
     << "length_unit=" << x.length_unit() << ", "
     << "event_number=" << x.event_number() << ", "
     << "particles=";
  repr(os, x.particles()) << ", vertices=";
  repr(os, x.vertices()) << ", run_info=";
  repr(os, x.run_info()) << ")";
  return os;
}
} // namespace HepMC3

namespace py = pybind11;
using namespace py::literals;

#define FUNC(name) m.def(#name, name)
#define PROP_RO(name, cls) .def_property_readonly(#name, &cls::name)
#define PROP_RO_OL(name, cls, rval) .def_property_readonly(#name, (rval (cls::*)() const) &cls::name)
#define PROP(name, cls) .def_property(#name, &cls::name, &cls::set_##name)
#define PROP_OL(name, cls, rval) .def_property(#name, (rval (cls::*)() const) &cls::name, &cls::set_##name)
#define METH(name, cls) .def(#name, &cls::name)
#define METH_OL(name, cls, rval, args) .def(#name, (rval (cls::*)(args)) &cls::name)

PYBIND11_MODULE(cpp, m) {
    using namespace HepMC3;

    // m.doc() = R"pbdoc(
    //     _pyhepmc_ng plugin
    //     --------------
    //     .. currentmodule:: pyhepmc_ng
    //     .. autosummary::
    //        :toctree: _generate
    //        Units
    //        FourVector
    //        GenEvent
    //        GenParticle
    //        GenVertex
    //        fill_genevent_from_hepevt
    //        print_hepevt
    //        print_content
    //        print_listing
    // )pbdoc";

    // m.def("dummy", []() { return 0; }, R"pbdoc(
    //     Return zero
    //     Some other explanation about the dummy function.
    // )pbdoc");

    py::class_<Units> clsUnits(m, "Units");

    py::enum_<Units::MomentumUnit>(clsUnits, "MomentumUnit")
        .value("MEV", Units::MomentumUnit::MEV)
        .value("GEV", Units::MomentumUnit::GEV)
        .export_values();

    py::enum_<Units::LengthUnit>(clsUnits, "LengthUnit")
        .value("CM", Units::LengthUnit::CM)
        .value("MM", Units::LengthUnit::MM)
        .export_values();

    py::class_<FourVector>(m, "FourVector")
        .def(py::init<>())
        .def(py::init<double, double, double, double>(),
             "x"_a, "y"_a, "z"_a, "t"_a)
        .def(py::init([](py::sequence seq) {
                const double x = py::cast<double>(seq[0]);
                const double y = py::cast<double>(seq[1]);
                const double z = py::cast<double>(seq[2]);
                const double t = py::cast<double>(seq[3]);
                return new FourVector(x, y, z, t);
            }))
        .def_property("x", &FourVector::x, &FourVector::setX)
        .def_property("y", &FourVector::y, &FourVector::setY)
        .def_property("z", &FourVector::z, &FourVector::setZ)
        .def_property("t", &FourVector::t, &FourVector::setT)
        .def_property("px", &FourVector::px, &FourVector::setPx)
        .def_property("py", &FourVector::py, &FourVector::setPy)
        .def_property("pz", &FourVector::pz, &FourVector::setPz)
        .def_property("e", &FourVector::e, &FourVector::setE)
        // support sequence protocol
        .def("__len__", [](FourVector& self) { return 4; })
        .def("__getitem__", [](const FourVector& self, int i) {
                if (i < 0) i += 4;
                switch(i) {
                    case 0: return self.x();
                    case 1: return self.y();
                    case 2: return self.z();
                    case 3: return self.t();
                    default:;// noop
                }
                PyErr_SetString(PyExc_IndexError, "out of bounds");
                throw py::error_already_set();
                return 0.0;
            })
        .def("__setitem__", [](FourVector& self, int i, double v) {
                if (i < 0) i += 4;
                switch(i) {
                    case 0: self.setX(v); break;
                    case 1: self.setY(v); break;
                    case 2: self.setZ(v); break;
                    case 3: self.setT(v); break;
                    default:
                        PyErr_SetString(PyExc_IndexError, "out of bounds");
                        throw py::error_already_set();
                }
            })
        METH(length2, FourVector)
        METH(length, FourVector)
        METH(perp2, FourVector)
        METH(perp, FourVector)
        METH(interval, FourVector)
        METH(pt, FourVector)
        METH(m2, FourVector)
        METH(m, FourVector)
        METH(phi, FourVector)
        METH(theta, FourVector)
        METH(eta, FourVector)
        METH(rap, FourVector)
        METH(abs_eta, FourVector)
        METH(abs_rap, FourVector)
        METH(is_zero, FourVector)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def(py::self * double())
        .def(py::self / double())
        .def(py::self += py::self)
        .def(py::self -= py::self)
        .def(py::self *= double())
        .def(py::self /= double())
        .def("__repr__", [](const FourVector& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        ;

    py::implicitly_convertible<py::sequence, FourVector>();

    FUNC(delta_phi);
    FUNC(delta_eta);
    FUNC(delta_rap);
    FUNC(delta_r2_eta);
    FUNC(delta_r_eta);
    FUNC(delta_r2_rap);
    FUNC(delta_r_rap);

    py::class_<GenRunInfo, GenRunInfoPtr> clsGenRunInfo(m, "GenRunInfo");
    clsGenRunInfo
        .def(py::init<>())
        .def_property("tools",
                (std::vector<GenRunInfo::ToolInfo>&(GenRunInfo::*)()) &GenRunInfo::tools,
                [](GenRunInfo& self, py::sequence seq) {
                    self.tools() = py::cast<std::vector<GenRunInfo::ToolInfo>>(seq);
                }
            )
        PROP(weight_names, GenRunInfo)
        PROP_RO(attributes, GenRunInfo)
        .def("__repr__", [](const GenRunInfo& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        .def(py::self == py::self)
        ;

    py::class_<GenRunInfo::ToolInfo>(clsGenRunInfo, "ToolInfo")
        .def(py::init<std::string, std::string, std::string>(),
             "name"_a, "version"_a, "description"_a)
        .def(py::init([](py::sequence seq) {
                return new GenRunInfo::ToolInfo({
                    py::cast<std::string>(seq[0]),
                    py::cast<std::string>(seq[1]),
                    py::cast<std::string>(seq[2])
                });
            }))
        .def("__repr__", [](const GenRunInfo::ToolInfo& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        .def(py::self == py::self)
        ;

    py::implicitly_convertible<py::sequence, GenRunInfo::ToolInfo>();

    py::class_<GenHeavyIon, GenHeavyIonPtr>(m, "GenHeavyIon")
        .def(py::init([](int nh, int np, int nt, int nc, int ns, int nsp,
                         int nnw=0, int nwn=0, int nwnw=0,
                         float im=0., float pl=0., float ec=0., float s=0., float cent=0.) {
                auto x = GenHeavyIonPtr(new GenHeavyIon());
                x->set(nh, np, nt, nc, ns, nsp, nnw, nwn, nwnw, im, pl, ec, s, cent);
                return x;
            }),
            "n_coll_hard"_a,
            "n_part_proj"_a,
            "n_part_targ"_a,
            "n_coll"_a,
            "n_spec_neut"_a,
            "n_spec_prot"_a,
            "nnw"_a = 0, "nwn"_a = 0, "nwnw"_a = 0,
            "impact_parameter"_a = 0.f, "event_plane_angle"_a = 0.f,
            "eccentricity"_a = 0.f, "sigma_inel_NN"_a = 0.f,
            "centrality"_a = 0.f)
        ;

    py::class_<GenEvent>(m, "GenEvent")
        .def(py::init<std::shared_ptr<GenRunInfo>, Units::MomentumUnit, Units::LengthUnit>(),
             "run"_a, "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
        .def(py::init<Units::MomentumUnit, Units::LengthUnit>(),
             "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
        PROP_RO_OL(particles, GenEvent, const std::vector<ConstGenParticlePtr>&)
        PROP_RO_OL(vertices, GenEvent, const std::vector<ConstGenVertexPtr>&)
        .def_property("weights",
          (std::vector<double>& (GenEvent::*)())&GenEvent::weights,
          [](GenEvent& x, py::sequence seq) {
            std::vector<double> w;
            w.reserve(py::len(seq));
            for (auto obj : seq)
              w.push_back(obj.cast<double>());
            x.weights() = w;
          }
        )
        PROP(run_info, GenEvent)
        PROP(event_number, GenEvent)
        PROP_RO(momentum_unit, GenEvent)
        PROP_RO(length_unit, GenEvent)
        METH(set_units, GenEvent)
        .def_property("heavy_ion",
          (GenHeavyIonPtr (GenEvent::*)()) &GenEvent::heavy_ion,
          &GenEvent::set_heavy_ion)
        .def_property("pdf_info",
          (HepMC3::GenPdfInfoPtr (GenEvent::*)()) &GenEvent::pdf_info,
          &GenEvent::set_pdf_info)
        .def_property("cross_section",
          (HepMC3::GenCrossSectionPtr (GenEvent::*)()) &GenEvent::cross_section,
          &GenEvent::set_cross_section)
        METH(event_pos, GenEvent)
        PROP_RO_OL(beams, GenEvent, std::vector<ConstGenParticlePtr>)
        METH_OL(add_vertex, GenEvent, void, GenVertexPtr)
        METH_OL(add_particle, GenEvent, void, GenParticlePtr)
        METH(set_beam_particles, GenEvent)
        METH_OL(remove_vertex, GenEvent, void, GenVertexPtr)
        METH_OL(remove_particle, GenEvent, void, GenParticlePtr)
        .def("reserve", &GenEvent::reserve, "particles"_a, "vertices"_a = 0)
        METH(clear, GenEvent)
        .def(py::self == py::self)
        .def("__repr__", [](GenEvent& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        .def("__str__", [](GenEvent& self) {
          std::ostringstream os;
          HepMC3::Print::listing(os, self, 2);
          return os.str();
        })
        ;

    py::class_<GenParticle, GenParticlePtr>(m, "GenParticle")
        .def(py::init<const FourVector&, int, int>(),
             "momentum"_a = py::make_tuple(0, 0, 0, 0),
             "pid"_a = 0, "status"_a = 0)
        PROP_RO_OL(parent_event, GenParticle, const GenEvent*)
        PROP_RO(in_event, GenParticle)
        PROP_RO(id, GenParticle)
        // PROP_RO(data, GenParticle)
        PROP_RO_OL(production_vertex, GenParticle, ConstGenVertexPtr)
        PROP_RO_OL(end_vertex, GenParticle, ConstGenVertexPtr)
        PROP_RO_OL(parents, GenParticle, std::vector<ConstGenParticlePtr>)
        PROP_RO_OL(children, GenParticle, std::vector<ConstGenParticlePtr>)
        // PROP_RO(ancestors, GenParticle)
        // PROP_RO(descendants, GenParticle)
        PROP(pid, GenParticle)
        PROP(status, GenParticle)
        PROP(momentum, GenParticle)
        PROP(generated_mass, GenParticle)
        METH(is_generated_mass_set, GenParticle)
        METH(unset_generated_mass, GenParticle)
        .def(py::self == py::self)
        .def("__repr__", [](const GenParticlePtr& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        ;

    py::class_<GenVertex, GenVertexPtr>(m, "GenVertex")
        .def(py::init<const FourVector&>(),
             "position"_a = py::make_tuple(0, 0, 0, 0))
        PROP_RO_OL(parent_event, GenVertex, const GenEvent*)
        PROP_RO(in_event, GenVertex)
        PROP_RO(id, GenVertex)
        PROP(status, GenVertex)
        // PROP_RO(data, GenVertex)
        METH_OL(add_particle_in, GenVertex, void, GenParticlePtr)
        METH_OL(add_particle_out, GenVertex, void, GenParticlePtr)
        METH_OL(remove_particle_in, GenVertex, void, GenParticlePtr)
        METH_OL(remove_particle_out, GenVertex, void, GenParticlePtr)
        // METH(particles, GenVertex)
        PROP_RO_OL(particles_in, GenVertex, const std::vector<ConstGenParticlePtr>&)
        PROP_RO_OL(particles_out, GenVertex, const std::vector<ConstGenParticlePtr>&)
        PROP(position, GenVertex)
        METH(has_set_position, GenVertex)
        .def(py::self == py::self)
        .def("__repr__", [](const GenVertexPtr& self) {
          std::ostringstream os;
          repr(os, self);
          return os.str();
        })
        ;

    // py::class_<GenParticleData>(m, "GenParticleData");
    // py::class_<GenVertexData>(m, "GenVertexData");

    // this class is here to allow unit testing of HEPEVT converters
    py::class_<HEPEVT>(m, "HEPEVT")
        .def(py::init<>())
        .def_readwrite("event_number", &HEPEVT::nevhep)
        .def_readwrite("nentries", &HEPEVT::nhep)
        .def("status", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<int>(evt.nhep, evt.isthep, self);
            })
        .def("pid", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<int>(evt.nhep, evt.idhep, self);
            })
        .def("parents", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<int>({evt.nhep, 2}, &evt.jmohep[0][0], self);
            })
        .def("children", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<int>({evt.nhep, 2}, &evt.jdahep[0][0], self);
            })
        .def("pm", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<momentum_t>({evt.nhep, 5}, &evt.phep[0][0], self);
            })
        .def("v", [](py::object self) {
                auto& evt = py::cast<HEPEVT&>(self);
                return py::array_t<momentum_t>({evt.nhep, 4}, &evt.vhep[0][0], self);
            })
        .def("clear", [](HEPEVT& self) {
                HEPEVT_Wrapper::set_hepevt_address((char*)&self);
                HEPEVT_Wrapper::zero_everything();
            })
        // GenEvent_to_HEPEVT is broken: sometimes produces wrong connections
        // .def("fill_from_genevent", [](HEPEVT& self, const GenEvent& evt) {
        //         HepMC::HEPEVT_Wrapper::set_hepevt_address((char*)&self);
        //         HepMC::HEPEVT_Wrapper::GenEvent_to_HEPEVT(&evt);
        //     })
        .def("__str__", [](const HEPEVT& self) {
                HEPEVT_Wrapper::set_hepevt_address((char*)&self);
                std::ostringstream os;
                HEPEVT_Wrapper::print_hepevt(os);
                return os.str();
            })
        .def_property_readonly("ptr", [](const HEPEVT& self) { return (std::intptr_t)&self; })
        .def_property_readonly_static("max_size", [](py::object){ return NMXHEP; } )
        ;

    // this class is here to simplify unit testing of Reader- and WriterAscii
    py::class_<std::stringstream>(m, "stringstream")
        .def(py::init<>())
        .def(py::init<std::string>())
        .def("__str__", (std::string (std::stringstream::*)() const) &std::stringstream::str)
        METH(flush, std::stringstream)
        METH(write, std::stringstream)
        METH(read, std::stringstream)
        ;

    py::class_<ReaderAscii>(m, "ReaderAscii")
        .def(py::init<const std::string>(), "filename"_a)
        .def(py::init<std::stringstream&>())
        METH(read_event, ReaderAscii)
        METH(failed, ReaderAscii)
        METH(close, ReaderAscii)
        .def("read", [](ReaderAscii& self) {
                py::object obj = py::cast(GenEvent());
                bool ok = self.read_event(py::cast<GenEvent&>(obj));
                if (!ok) {
                    PyErr_SetString(PyExc_IOError, "error reading event");
                    throw py::error_already_set();
                }
                return obj;
            })
        // support contextmanager protocoll
        .def("__enter__", [](py::object self) { return self; })
        .def("__exit__", [](ReaderAscii& self, py::object type, py::object value, py::object tb) {
                self.close();
                return false;
            })
        ;

    py::class_<ReaderAsciiHepMC2>(m, "ReaderAsciiHepMC2")
        .def(py::init<const std::string>(), "filename"_a)
        METH(read_event, ReaderAsciiHepMC2)
        METH(failed, ReaderAsciiHepMC2)
        METH(close, ReaderAsciiHepMC2)
        .def("read", [](ReaderAsciiHepMC2& self) {
                py::object obj = py::cast(GenEvent());
                bool ok = self.read_event(py::cast<GenEvent&>(obj));
                if (!ok) {
                    PyErr_SetString(PyExc_IOError, "error reading event");
                    throw py::error_already_set();
                }
                return obj;
            })
        // support contextmanager protocoll
        .def("__enter__", [](py::object self) { return self; })
        .def("__exit__", [](ReaderAsciiHepMC2& self, py::object type, py::object value, py::object tb) {
                self.close();
                return false;
            })
        ;

    py::class_<WriterAscii>(m, "WriterAscii")
        .def(py::init<const std::string&, GenRunInfoPtr>(),
             "filename"_a, "run"_a = nullptr)
        .def(py::init<std::stringstream&, GenRunInfoPtr>(),
             "ostringstream"_a, "run"_a = nullptr,
             py::keep_alive<1, 2>())
        METH(write_event, WriterAscii)
        METH(write_run_info, WriterAscii)
        .def("write", [](WriterAscii& self, const GenEvent& evt) {
                self.write_event(evt);
            })
        METH(failed, WriterAscii)
        METH(close, WriterAscii)
        PROP(precision, WriterAscii)
        // support contextmanager protocoll
        .def("__enter__", [](py::object self) { return self; })
        .def("__exit__", [](WriterAscii& self, py::object type, py::object value, py::object tb) {
                self.close();
                return false;
            })
        ;

    m.def("fill_genevent_from_hepevt", fill_genevent_from_hepevt<double>,
          "evt"_a, "event_number"_a, "p"_a, "m"_a, "v"_a, "pid"_a, "parents"_a,
          "children"_a, "particle_status"_a, "vertex_status"_a,
          "momentum_scaling"_a = 1.0, "length_scaling"_a = 1.0);

    m.def("content", [](const GenEvent& event) {
      std::ostringstream os;
      HepMC3::Print::content(os, event);
      return os.str();
    });

    m.def("listing", [](const GenEvent& event, unsigned short precision = 2) {
      std::ostringstream os;
      HepMC3::Print::listing(os, event, precision);
      return os.str();
    });

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}