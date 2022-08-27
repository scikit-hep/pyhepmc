#include "pybind.h"

#include "HepMC3/FourVector.h"
#include "HepMC3/GenCrossSection.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenHeavyIon.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/GenPdfInfo.h"
#include "HepMC3/GenRunInfo.h"
#include "HepMC3/GenVertex.h"
#include "HepMC3/Print.h"
#include "HepMC3/Units.h"

#include <algorithm>
#include <cmath>
#include <functional>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <vector>

// #include "GzReaderAscii.h"

void register_io(py::module& m);

template <class Iterator, class Streamer>
std::ostream& ostream_range(std::ostream& os, Iterator begin, Iterator end,
                            Streamer streamer, const char bracket_left = '[',
                            const char bracket_right = ']') {
  os << bracket_left;
  bool first = true;
  for (; begin != end; ++begin) {
    if (first) {
      first = false;
    } else {
      os << ", ";
    }
    streamer(os, begin);
  }
  os << bracket_right;
  return os;
}

namespace HepMC3 {

using GenRunInfoPtr = std::shared_ptr<GenRunInfo>;

// equality comparions used by unit tests
bool is_close(const FourVector& a, const FourVector& b, double rel_eps = 1e-7) {
  auto is_close = [rel_eps](double a, double b) { return std::abs(a - b) < rel_eps; };
  return is_close(a.x(), b.x()) && is_close(a.y(), b.y()) && is_close(a.z(), b.z()) &&
         is_close(a.t(), b.t());
}

// compares all real qualities of two particles, but ignores the .id() field
bool operator==(const GenParticle& a, const GenParticle& b) {
  return a.pid() == b.pid() && a.status() == b.status() &&
         is_close(a.momentum(), b.momentum());
}

bool operator!=(const GenParticle& a, const GenParticle& b) {
  return !operator==(a, b);
}

// compares all real qualities of both particle sets,
// but ignores the .id() fields and the particle order
bool equal_particle_sets(const std::vector<ConstGenParticlePtr>& a,
                         const std::vector<ConstGenParticlePtr>& b) {
  if (a.size() != b.size()) return false;
  auto unmatched = b;
  for (auto&& ai : a) {
    auto it = std::find_if(unmatched.begin(), unmatched.end(),
                           [ai](ConstGenParticlePtr x) { return *ai == *x; });
    if (it == unmatched.end()) return false;
    unmatched.erase(it);
  }
  return unmatched.empty();
}

// compares all real qualities of two vertices, but ignores the .id() field
bool operator==(const GenVertex& a, const GenVertex& b) {
  return a.status() == b.status() && is_close(a.position(), b.position()) &&
         equal_particle_sets(a.particles_in(), b.particles_in()) &&
         equal_particle_sets(a.particles_out(), b.particles_out());
}

bool operator!=(const GenVertex& a, const GenVertex& b) { return !operator==(a, b); }

// compares all real qualities of both vertex sets,
// but ignores the .id() fields and the vertex order
bool equal_vertex_sets(const std::vector<ConstGenVertexPtr>& a,
                       const std::vector<ConstGenVertexPtr>& b) {
  if (a.size() != b.size()) return false;
  auto unmatched = b;
  for (auto&& ai : a) {
    auto it = std::find_if(unmatched.begin(), unmatched.end(),
                           [ai](ConstGenVertexPtr x) { return *ai == *x; });
    if (it == unmatched.end()) return false;
    unmatched.erase(it);
  }
  return unmatched.empty();
}

bool operator==(const GenRunInfo::ToolInfo& a, const GenRunInfo::ToolInfo& b) {
  return a.name == b.name && a.version == b.version && a.description == b.description;
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
         std::equal(a.weight_names().begin(), a.weight_names().end(),
                    b.weight_names().begin()) &&
         std::equal(a_attr.begin(), a_attr.end(), b_attr.begin(),
                    [](const std::pair<std::string, std::shared_ptr<Attribute>>& a,
                       const std::pair<std::string, std::shared_ptr<Attribute>>& b) {
                      if (a.first != b.first) return false;
                      if (bool(a.second) != bool(b.second)) return false;
                      if (!a.second) return true;
                      std::string sa, sb;
                      a.second->to_string(sa);
                      b.second->to_string(sb);
                      return sa == sb;
                    });
}

bool operator!=(const GenRunInfo& a, const GenRunInfo& b) { return !operator==(a, b); }

bool operator==(const GenEvent& a, const GenEvent& b) {
  // incomplete:
  // missing comparison of GenHeavyIon, GenPdfInfo, GenCrossSection

  if (a.event_number() != b.event_number() || a.momentum_unit() != b.momentum_unit() ||
      a.length_unit() != b.length_unit())
    return false;

  // run_info may be missing
  if (a.run_info() && b.run_info()) {
    if (!(*a.run_info() == *b.run_info())) return false;
  } else if (!a.run_info() && b.run_info()) {
    if (*b.run_info() != GenRunInfo()) return false;
  } else if (a.run_info() && !b.run_info()) {
    if (*a.run_info() != GenRunInfo()) return false;
  }

  // if all vertices compare equal, then also all particles are equal
  return equal_vertex_sets(a.vertices(), b.vertices());
}

bool operator!=(const GenEvent& a, const GenEvent& b) { return !operator==(a, b); }

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
  const int saved = os.precision();
  os.precision(3);
  os << "FourVector(" << x.x() << ", " << x.y() << ", " << x.z() << ", " << x.t()
     << ")";
  os.precision(saved);
  return os;
}

template <class T, class A>
std::ostream& repr(std::ostream& os, const std::vector<T, A>& v) {
  return ostream_range(
      os, v.begin(), v.end(),
      [](std::ostream& os, typename std::vector<T, A>::const_iterator it) {
        repr(os, *it);
      });
}

template <class K, class V, class... Ts>
std::ostream& repr(std::ostream& os, const std::map<K, V, Ts...>& m) {
  return ostream_range(
      os, m.begin(), m.end(),
      [](std::ostream& os, typename std::map<K, V, Ts...>::const_iterator it) {
        os << it->first << ": ";
        repr(os, it->second);
      },
      '{', '}');
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
  if (x.is_generated_mass_set()) os << ", mass=" << x.data().mass;
  os << ", pid=" << x.pid() << ", status=" << x.status() << ")";
  return os;
}

inline std::ostream& repr(std::ostream& os, const HepMC3::GenVertex& x) {
  os << "GenVertex(";
  repr(os, x.position());
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

void from_hepevt(GenEvent& event, int event_number, py::array_t<double> px,
                 py::array_t<double> py, py::array_t<double> pz, py::array_t<double> en,
                 py::array_t<double> m, py::array_t<int> pid, py::array_t<int> status,
                 py::object parents, py::object children, py::object vx, py::object vy,
                 py::object vz, py::object vt);

} // namespace HepMC3

PYBIND11_MODULE(_core, m) {
  using namespace HepMC3;

  // m.doc() = R"pbdoc(
  //     _pyhepmc plugin
  //     --------------
  //     .. currentmodule:: pyhepmc
  //     .. autosummary::
  //        :toctree: _generate
  //        Units
  //        FourVector
  //        GenEvent
  //        GenParticle
  //        GenVertex
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
      .def(py::init<double, double, double, double>(), "x"_a, "y"_a, "z"_a, "t"_a)
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
      .def("__getitem__",
           [](const FourVector& self, int i) {
             if (i < 0) i += 4;
             switch (i) {
               case 0: return self.x();
               case 1: return self.y();
               case 2: return self.z();
               case 3: return self.t();
               default:; // noop
             }
             PyErr_SetString(PyExc_IndexError, "out of bounds");
             throw py::error_already_set();
             return 0.0;
           })
      .def("__setitem__",
           [](FourVector& self, int i, double v) {
             if (i < 0) i += 4;
             switch (i) {
               case 0: self.setX(v); break;
               case 1: self.setY(v); break;
               case 2: self.setZ(v); break;
               case 3: self.setT(v); break;
               default:
                 PyErr_SetString(PyExc_IndexError, "out of bounds");
                 throw py::error_already_set();
             }
           })
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
      .def("__repr__",
           [](const FourVector& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      // clang-format off
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
      // clang-format on
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
  clsGenRunInfo.def(py::init<>())
      .def_property("tools",
                    overload_cast<std::vector<GenRunInfo::ToolInfo>&, GenRunInfo>(
                        &GenRunInfo::tools),
                    [](GenRunInfo& self, py::sequence seq) {
                      self.tools() = py::cast<std::vector<GenRunInfo::ToolInfo>>(seq);
                    })
      .def("__repr__",
           [](const GenRunInfo& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def(py::self == py::self)
      // clang-format off
      PROP(weight_names, GenRunInfo)
      PROP_RO(attributes, GenRunInfo)
      // clang-format on
      ;

  py::class_<GenRunInfo::ToolInfo>(clsGenRunInfo, "ToolInfo")
      .def(py::init<std::string, std::string, std::string>(), "name"_a, "version"_a,
           "description"_a)
      .def(py::init([](py::sequence seq) {
        return new GenRunInfo::ToolInfo({py::cast<std::string>(seq[0]),
                                         py::cast<std::string>(seq[1]),
                                         py::cast<std::string>(seq[2])});
      }))
      .def("__repr__",
           [](const GenRunInfo::ToolInfo& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def(py::self == py::self)
      // clang-format off
      ATTR(name, GenRunInfo::ToolInfo)
      ATTR(version, GenRunInfo::ToolInfo)
      ATTR(description, GenRunInfo::ToolInfo)
      // clang-format on
      ;

  py::implicitly_convertible<py::sequence, GenRunInfo::ToolInfo>();

  py::class_<GenHeavyIon, GenHeavyIonPtr>(m, "GenHeavyIon")
      .def(py::init([](int nh, int np, int nt, int nc, int ns, int nsp, int nnw = 0,
                       int nwn = 0, int nwnw = 0, float im = 0., float pl = 0.,
                       float ec = 0., float s = 0., float cent = 0.) {
             auto x = GenHeavyIonPtr(new GenHeavyIon());
             x->set(nh, np, nt, nc, ns, nsp, nnw, nwn, nwnw, im, pl, ec, s, cent);
             return x;
           }),
           "n_coll_hard"_a, "n_part_proj"_a, "n_part_targ"_a, "n_coll"_a,
           "n_spec_neut"_a, "n_spec_prot"_a, "nnw"_a = 0, "nwn"_a = 0, "nwnw"_a = 0,
           "impact_parameter"_a = 0.f, "event_plane_angle"_a = 0.f,
           "eccentricity"_a = 0.f, "sigma_inel_NN"_a = 0.f, "centrality"_a = 0.f);

  py::class_<GenEvent>(m, "GenEvent")
      .def(py::init<std::shared_ptr<GenRunInfo>, Units::MomentumUnit,
                    Units::LengthUnit>(),
           "run"_a, "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
      .def(py::init<Units::MomentumUnit, Units::LengthUnit>(),
           "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
      .def_property("weights",
                    overload_cast<std::vector<double>&, GenEvent>(&GenEvent::weights),
                    [](GenEvent& self, py::sequence seq) {
                      std::vector<double> w;
                      w.reserve(py::len(seq));
                      for (auto obj : seq) w.push_back(obj.cast<double>());
                      self.weights() = w;
                    })
      .def(
          "weight",
          [](GenEvent& self, const unsigned long i) -> double {
            try {
              return self.weight(i);
            } catch (const std::runtime_error&) { throw py::index_error(); }
          },
          "index"_a = 0)
      .def("weight",
           overload_cast<double, const GenEvent, const std::string&>(&GenEvent::weight),
           "name"_a)
      .def(
          "set_weight",
          [](GenEvent& self, const std::string& name, double v) {
            self.weight(name) = v;
          },
          "name"_a, "value"_a)
      .def_property_readonly("weight_names",
                             [](const GenEvent& self) { return self.weight_names(); })
      .def_property("heavy_ion",
                    overload_cast<GenHeavyIonPtr, GenEvent>(&GenEvent::heavy_ion),
                    &GenEvent::set_heavy_ion)
      .def_property("pdf_info",
                    overload_cast<GenPdfInfoPtr, GenEvent>(&GenEvent::pdf_info),
                    &GenEvent::set_pdf_info)
      .def_property(
          "cross_section",
          overload_cast<GenCrossSectionPtr, GenEvent>(&GenEvent::cross_section),
          &GenEvent::set_cross_section)
      .def("reserve", &GenEvent::reserve, "particles"_a, "vertices"_a = 0)
      .def(py::self == py::self)
      .def("__repr__",
           [](GenEvent& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def("__str__",
           [](GenEvent& self) {
             std::ostringstream os;
             HepMC3::Print::listing(os, self, 2);
             return os.str();
           })

      .def("from_hepevt", from_hepevt, "event_number"_a, "px"_a, "py"_a, "pz"_a, "en"_a,
           "m"_a, "pid"_a, "status"_a, "parents"_a = py::none(),
           "children"_a = py::none(), "vx"_a = py::none(), "vy"_a = py::none(),
           "vz"_a = py::none(), "vt"_a = py::none())
      // clang-format off
      METH(clear, GenEvent)
      PROP(run_info, GenEvent)
      PROP(event_number, GenEvent)
      PROP_RO(momentum_unit, GenEvent)
      PROP_RO(length_unit, GenEvent)
      METH(set_units, GenEvent)
      METH(event_pos, GenEvent)
      PROP_RO_OL(beams, GenEvent, std::vector<ConstGenParticlePtr>)
      METH_OL(add_vertex, GenEvent, void, GenVertexPtr)
      METH_OL(add_particle, GenEvent, void, GenParticlePtr)
      METH(set_beam_particles, GenEvent)
      METH_OL(remove_vertex, GenEvent, void, GenVertexPtr)
      METH_OL(remove_particle, GenEvent, void, GenParticlePtr)
      PROP_RO_OL(particles, GenEvent, const std::vector<ConstGenParticlePtr>&)
      PROP_RO_OL(vertices, GenEvent, const std::vector<ConstGenVertexPtr>&)
      // clang-format on
      ;

  py::class_<GenParticle, GenParticlePtr>(m, "GenParticle")
      .def(py::init<const FourVector&, int, int>(),
           "momentum"_a = py::make_tuple(0, 0, 0, 0), "pid"_a = 0, "status"_a = 0)
      .def(py::self == py::self)
      .def("__repr__",
           [](const GenParticlePtr& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      // clang-format off
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
      // clang-format on
      ;

  py::class_<GenVertex, GenVertexPtr>(m, "GenVertex")
      .def(py::init<const FourVector&>(), "position"_a = py::make_tuple(0, 0, 0, 0))
      .def(py::self == py::self)
      .def("__repr__",
           [](const GenVertexPtr& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      // clang-format off
      PROP_RO_OL(parent_event, GenVertex, const GenEvent*)
      PROP_RO(in_event, GenVertex)
      PROP_RO(id, GenVertex)
      PROP(status, GenVertex)
      PROP_RO_OL(particles_in, GenVertex, const std::vector<ConstGenParticlePtr>&)
      PROP_RO_OL(particles_out, GenVertex, const std::vector<ConstGenParticlePtr>&)
      // PROP_RO(data, GenVertex)
      PROP(position, GenVertex)
      METH_OL(add_particle_in, GenVertex, void, GenParticlePtr)
      METH_OL(add_particle_out, GenVertex, void, GenParticlePtr)
      METH_OL(remove_particle_in, GenVertex, void, GenParticlePtr)
      METH_OL(remove_particle_out, GenVertex, void, GenParticlePtr)
      // METH(particles, GenVertex)
      METH(has_set_position, GenVertex)
      // clang-format on
      ;

  // py::class_<GenParticleData>(m, "GenParticleData");
  // py::class_<GenVertexData>(m, "GenVertexData");

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

  FUNC(equal_particle_sets);
  FUNC(equal_vertex_sets);

  register_io(m);
}
