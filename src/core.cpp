#include "attributes_view.hpp"
#include "pointer.hpp"
#include "pybind.hpp"
#include <HepMC3/Attribute.h>
#include <HepMC3/FourVector.h>
#include <HepMC3/GenCrossSection.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenHeavyIon.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenPdfInfo.h>
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/GenVertex.h>
#include <HepMC3/LHEFAttributes.h>
#include <HepMC3/Print.h>
#include <HepMC3/Units.h>
#include <algorithm>
#include <cmath>
#include <functional>
#include <map>
#include <memory>
#include <pybind11/detail/common.h>
#include <pybind11/pytypes.h>
#include <sstream>
#include <stdexcept>
#include <string>
#include <type_traits>
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

template <class T>
bool operator!=(const T& a, const T& b) {
  return !operator==(a, b);
}

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
                    [](const std::pair<std::string, AttributePtr>& a,
                       const std::pair<std::string, AttributePtr>& b) {
                      if (a.first != b.first) return false;
                      if (bool(a.second) != bool(b.second)) return false;
                      if (!a.second) return true;
                      std::string sa, sb;
                      a.second->to_string(sa);
                      b.second->to_string(sb);
                      return sa == sb;
                    });
}

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

bool operator==(const GenHeavyIon& a, const GenHeavyIon& b) {
  return a.Ncoll_hard == b.Ncoll_hard && a.Npart_proj == b.Npart_proj &&
         a.Npart_targ == b.Npart_targ && a.Ncoll == b.Ncoll &&
         a.N_Nwounded_collisions == b.N_Nwounded_collisions &&
         a.Nwounded_N_collisions == b.Nwounded_N_collisions &&
         a.Nwounded_Nwounded_collisions == b.Nwounded_Nwounded_collisions &&
         a.impact_parameter == b.impact_parameter &&
         a.event_plane_angle == b.event_plane_angle &&
         a.sigma_inel_NN == b.sigma_inel_NN && a.centrality == b.centrality &&
         a.user_cent_estimate == b.user_cent_estimate;
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

int crosssection_safe_index(GenCrossSection& cs, py::object obj);
std::string crosssection_safe_name(GenCrossSection& cs, py::object obj);

void from_hepevt(GenEvent& event, int event_number, py::array_t<double> px,
                 py::array_t<double> py, py::array_t<double> pz, py::array_t<double> en,
                 py::array_t<double> m, py::array_t<int> pid, py::array_t<int> status,
                 py::object parents, py::object children, py::object vx, py::object vy,
                 py::object vz, py::object vt);

} // namespace HepMC3

PYBIND11_MODULE(_core, m) {
  using namespace HepMC3;

  py::module_ m_doc = py::module_::import("pyhepmc._doc");
  auto doc = py::cast<std::map<std::string, std::string>>(m_doc.attr("doc"));

  py::class_<Units> clsUnits(m, "Units", DOC(Units));

  py::enum_<Units::MomentumUnit>(clsUnits, "MomentumUnit")
      .value("MEV", Units::MomentumUnit::MEV)
      .value("GEV", Units::MomentumUnit::GEV)
      .export_values();

  py::enum_<Units::LengthUnit>(clsUnits, "LengthUnit")
      .value("CM", Units::LengthUnit::CM)
      .value("MM", Units::LengthUnit::MM)
      .export_values();

  py::class_<FourVector>(m, "FourVector", DOC(FourVector))
      .def(py::init<>())
      .def(py::init<double, double, double, double>(), "x"_a, "y"_a, "z"_a, "t"_a)
      .def(py::init([](py::sequence seq) {
        if (py::len(seq) != 4) throw py::value_error("length != 4");
        const double x = py::cast<double>(seq[0]);
        const double y = py::cast<double>(seq[1]);
        const double z = py::cast<double>(seq[2]);
        const double t = py::cast<double>(seq[3]);
        return new FourVector(x, y, z, t);
      }))
      .def_property("x", &FourVector::x, &FourVector::setX, DOC(FourVector.x))
      .def_property("y", &FourVector::y, &FourVector::setY, DOC(FourVector.y))
      .def_property("z", &FourVector::z, &FourVector::setZ, DOC(FourVector.z))
      .def_property("t", &FourVector::t, &FourVector::setT, DOC(FourVector.t))
      .def_property("px", &FourVector::px, &FourVector::setPx, DOC(FourVector.px))
      .def_property("py", &FourVector::py, &FourVector::setPy, DOC(FourVector.py))
      .def_property("pz", &FourVector::pz, &FourVector::setPz, DOC(FourVector.pz))
      .def_property("e", &FourVector::e, &FourVector::setE, DOC(FourVector.e))
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
               default: throw py::index_error("out of bounds");
             }
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
               default: throw py::index_error("out of bounds");
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
      METH(pt2, FourVector)
      METH(m, FourVector)
      METH(m2, FourVector)
      METH(phi, FourVector)
      METH(theta, FourVector)
      METH(eta, FourVector)
      METH(rap, FourVector)
      METH(abs_eta, FourVector)
      METH(abs_rap, FourVector)
      METH(is_zero, FourVector)
      METH(rho, FourVector)
      METH(p3mod, FourVector)
      METH(p3mod2, FourVector)
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

  py::class_<Attribute, AttributePtr>(m, "Attribute", DOC(Attribute))
      .def_property_readonly(
          "particle", overload_cast<GenParticlePtr, Attribute>(&Attribute::particle),
          DOC(Attribute.particle))
      .def_property_readonly("vertex",
                             overload_cast<GenVertexPtr, Attribute>(&Attribute::vertex),
                             DOC(Attribute.vertex))
      .def("to_string",
           [](const Attribute& self) {
             std::string s;
             self.to_string(s);
             return s;
           })
      // clang-format off
      METH(from_string, Attribute)
      PROP_RO(is_parsed, Attribute)
      PROP_RO(unparsed_string, Attribute)
      PROP_RO(event, Attribute)
      // clang-format on
      ;

  py::class_<HEPRUPAttribute, HEPRUPAttributePtr, Attribute>(m, "HEPRUPAttribute",
                                                             DOC(HEPRUPAttribute))
      .def(py::init<>())
      // clang-format off
      ATTR(heprup, HEPRUPAttribute)
      // clang-format on
      ;

  py::class_<HEPEUPAttribute, HEPEUPAttributePtr, Attribute>(m, "HEPEUPAttribute",
                                                             DOC(HEPEUPAttribute))
      .def(py::init<>())
      // clang-format off
      METH(momentum, HEPEUPAttribute)
      ATTR(hepeup, HEPEUPAttribute)
      // clang-format on
      ;

  py::class_<GenHeavyIon, GenHeavyIonPtr, Attribute>(m, "GenHeavyIon", DOC(GenHeavyIon))
      .def(py::init<>())
      .def("__eq__", py::overload_cast<const GenHeavyIon&, const GenHeavyIon&>(
                         HepMC3::operator==))
      // clang-format off
      ATTR(Ncoll_hard, GenHeavyIon)
      ATTR(Npart_proj, GenHeavyIon)
      ATTR(Npart_targ, GenHeavyIon)
      ATTR(Ncoll, GenHeavyIon)
      ATTR(N_Nwounded_collisions, GenHeavyIon)
      ATTR(Nwounded_N_collisions, GenHeavyIon)
      ATTR(Nwounded_Nwounded_collisions, GenHeavyIon)
      ATTR(impact_parameter, GenHeavyIon)
      ATTR(event_plane_angle, GenHeavyIon)
      ATTR(sigma_inel_NN, GenHeavyIon)
      ATTR(centrality, GenHeavyIon)
      ATTR(user_cent_estimate, GenHeavyIon)
      ATTR(Nspec_proj_n, GenHeavyIon)
      ATTR(Nspec_targ_n, GenHeavyIon)
      ATTR(Nspec_proj_p, GenHeavyIon)
      ATTR(Nspec_targ_p, GenHeavyIon)
      ATTR(participant_plane_angles, GenHeavyIon)
      ATTR(eccentricities, GenHeavyIon)
      // clang-format on
      ;

  py::class_<GenPdfInfo, GenPdfInfoPtr, Attribute>(m, "GenPdfInfo", DOC(GenPdfInfo))
      .def(py::init<>())
      .def_property(
          "parton_id1", [](const GenPdfInfo& self) { return self.parton_id[0]; },
          [](GenPdfInfo& self, int value) { self.parton_id[0] = value; },
          DOC(GenPdfInfo.parton_id))
      .def_property(
          "parton_id2", [](const GenPdfInfo& self) { return self.parton_id[1]; },
          [](GenPdfInfo& self, int value) { self.parton_id[1] = value; },
          DOC(GenPdfInfo.parton_id))
      .def_property(
          "pdf_id1", [](const GenPdfInfo& self) { return self.pdf_id[0]; },
          [](GenPdfInfo& self, int value) { self.pdf_id[0] = value; },
          DOC(GenPdfInfo.pdf_id))
      .def_property(
          "pdf_id2", [](const GenPdfInfo& self) { return self.pdf_id[1]; },
          [](GenPdfInfo& self, int value) { self.pdf_id[1] = value; },
          DOC(GenPdfInfo.pdf_id))
      .def_property(
          "x1", [](const GenPdfInfo& self) { return self.x[0]; },
          [](GenPdfInfo& self, double value) { self.x[0] = value; }, DOC(GenPdfInfo.x))
      .def_property(
          "x2", [](const GenPdfInfo& self) { return self.x[1]; },
          [](GenPdfInfo& self, double value) { self.x[1] = value; }, DOC(GenPdfInfo.x))
      .def_property(
          "xf1", [](const GenPdfInfo& self) { return self.xf[0]; },
          [](GenPdfInfo& self, double value) { self.xf[0] = value; },
          DOC(GenPdfInfo.xf))
      .def_property(
          "xf2", [](const GenPdfInfo& self) { return self.xf[1]; },
          [](GenPdfInfo& self, double value) { self.xf[1] = value; },
          DOC(GenPdfInfo.xf))
      // clang-format off
      ATTR(scale, GenPdfInfo)
      // clang-format on
      ;

  py::class_<GenCrossSection, GenCrossSectionPtr, Attribute>(m, "GenCrossSection",
                                                             DOC(GenCrossSection))
      .def(py::init<>())
      .def(
          "xsec",
          [](GenCrossSection& self, py::object obj) {
            // need to do checks for invalid indices because they are missing in C++
            if (py::isinstance<py::int_>(obj)) {
              auto idx = crosssection_safe_index(self, obj);
              return self.xsec(idx);
            } else if (py::isinstance<py::str>(obj)) {
              auto name = crosssection_safe_name(self, obj);
              return self.xsec(name);
            } else
              throw py::type_error("int or str required");
            return 0.0;
          },
          "index_or_name"_a = 0, DOC(GenCrossSection.xsec))
      .def(
          "xsec_err",
          [](GenCrossSection& self, py::object obj) {
            if (py::isinstance<py::int_>(obj)) {
              auto idx = crosssection_safe_index(self, obj);
              return self.xsec_err(idx);
            } else if (py::isinstance<py::str>(obj)) {
              auto name = crosssection_safe_name(self, obj);
              return self.xsec_err(name);
            } else
              throw py::type_error("int or str required");
            return 0.0;
          },
          "index_or_name"_a = 0, DOC(GenCrossSection.xsec_err))
      .def(
          "set_xsec",
          [](GenCrossSection& self, py::object obj, double value) {
            if (py::isinstance<py::int_>(obj)) {
              auto idx = crosssection_safe_index(self, obj);
              self.set_xsec(idx, value);
            } else if (py::isinstance<py::str>(obj)) {
              auto name = crosssection_safe_name(self, obj);
              self.set_xsec(name, value);
            } else
              throw py::type_error("int or str required");
          },
          "index_or_name"_a, "value"_a, DOC(GenCrossSection.set_xsec))
      .def(
          "set_xsec_err",
          [](GenCrossSection& self, py::object obj, double value) {
            if (py::isinstance<py::int_>(obj)) {
              auto idx = crosssection_safe_index(self, obj);
              self.set_xsec_err(idx, value);
            } else if (py::isinstance<py::str>(obj)) {
              auto name = crosssection_safe_name(self, obj);
              self.set_xsec_err(name, value);
            } else
              throw py::type_error("int or str required");
          },
          "index_or_name"_a, "value"_a, DOC(GenCrossSection.set_xsec_err))
      .def("set_cross_section", &GenCrossSection::set_cross_section, "cross_section"_a,
           "cross_section_error"_a, "accepted_events"_a = -1, "attempted_events"_a = -1,
           DOC(GenCrossSection.set_cross_section))
      // clang-format off
      PROP2(accepted_events, GenCrossSection)
      PROP2(attempted_events, GenCrossSection)
      PROP_RO(is_valid, GenCrossSection)
      // clang-format on
      ;

  py::class_<AttributesView> clsAttributesView(m, "AttributesView",
                                               DOC(AttributesView));
  clsAttributesView

      .def("__getitem__", &AttributesView::getitem)
      .def("__setitem__", &AttributesView::setitem)
      .def("__delitem__", &AttributesView::delitem)
      .def("__contains__", &AttributesView::contains)
      .def("__iter__", &AttributesView::iter)
      .def("__len__", &AttributesView::len);

  py::class_<AttributesView::Iter>(clsAttributesView, "Iter")
      .def("next", &AttributesView::Iter::next)
      .def("__next__", &AttributesView::Iter::next)
      .def("__iter__", [](AttributesView::Iter& self) { return self; });

  py::class_<RunInfoAttributesView> clsRunInfoAttributesView(
      m, "RunInfoAttributesView", DOC(RunInfoAttributesView));
  clsRunInfoAttributesView

      .def("__getitem__", &RunInfoAttributesView::getitem)
      .def("__setitem__", &RunInfoAttributesView::setitem)
      .def("__delitem__", &RunInfoAttributesView::delitem)
      .def("__contains__", &RunInfoAttributesView::contains)
      .def("__iter__", &RunInfoAttributesView::iter)
      .def("__len__", &RunInfoAttributesView::len);

  py::class_<RunInfoAttributesView::Iter>(clsRunInfoAttributesView, "Iter")
      .def("next", &RunInfoAttributesView::Iter::next)
      .def("__next__", &RunInfoAttributesView::Iter::next)
      .def("__iter__", [](RunInfoAttributesView::Iter& self) { return self; });

  py::class_<GenRunInfo, GenRunInfoPtr> clsGenRunInfo(m, "GenRunInfo", DOC(GenRunInfo));

  clsGenRunInfo.def(py::init<>())
      .def_property("tools",
                    overload_cast<std::vector<GenRunInfo::ToolInfo>&, GenRunInfo>(
                        &GenRunInfo::tools),
                    [](GenRunInfo& self, py::sequence seq) {
                      self.tools() = py::cast<std::vector<GenRunInfo::ToolInfo>>(seq);
                    })
      .def_property(
          "attributes", [](GenRunInfoPtr self) { return RunInfoAttributesView{self}; },
          [](GenRunInfoPtr self, py::dict obj) {
            auto amv = RunInfoAttributesView{self};
            py::cast(amv).attr("clear")();
            for (const auto& kv : obj) {
              amv.setitem(py::cast<py::str>(kv.first),
                          py::reinterpret_borrow<py::object>(kv.second));
            }
          },
          DOC(attributes))
      .def("__repr__",
           [](const GenRunInfo& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def(py::self == py::self)
      // clang-format off
      PROP(weight_names, GenRunInfo)
      // clang-format on
      ;

  py::class_<GenRunInfo::ToolInfo>(clsGenRunInfo, "ToolInfo", DOC(GenRunInfo.ToolInfo))
      .def(py::init<std::string, std::string, std::string>(), "name"_a, "version"_a,
           "description"_a)
      .def(py::init([](py::sequence seq) {
        if (py::len(seq) != 3) throw py::value_error("length != 3");
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

  py::class_<GenEvent, GenEventPtr>(m, "GenEvent", DOC(GenEvent))
      .def(py::init<GenRunInfoPtr, Units::MomentumUnit, Units::LengthUnit>(), "run"_a,
           "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
      .def(py::init<Units::MomentumUnit, Units::LengthUnit>(),
           "momentum_unit"_a = Units::GEV, "length_unit"_a = Units::MM)
      .def_property(
          "weights", overload_cast<std::vector<double>&, GenEvent>(&GenEvent::weights),
          [](GenEvent& self, py::sequence seq) {
            std::vector<double> w;
            w.reserve(py::len(seq));
            for (auto obj : seq) w.push_back(obj.cast<double>());
            self.weights() = w;
          },
          DOC(GenEvent.weights))
      .def(
          "weight",
          [](GenEvent& self, py::object obj) {
            if (py::isinstance<py::int_>(obj)) try {
                return self.weight(py::cast<int>(obj));
              } catch (const std::runtime_error&) { throw py::index_error(); }
            else if (py::isinstance<py::str>(obj))
              return self.weight(py::cast<std::string>(obj));
            else
              throw py::type_error("int or str required");
            return 0.0;
          },
          "index_or_name"_a = 0, DOC(GenEvent.weight))
      .def(
          "set_weight",
          [](GenEvent& self, const std::string& name, double v) {
            self.weight(name) = v;
          },
          "name"_a, "value"_a, DOC(GenEvent.set_weight))
      .def_property("heavy_ion",
                    overload_cast<GenHeavyIonPtr, GenEvent>(&GenEvent::heavy_ion),
                    &GenEvent::set_heavy_ion, DOC(GenEvent.heavy_ion))
      .def_property("pdf_info",
                    overload_cast<GenPdfInfoPtr, GenEvent>(&GenEvent::pdf_info),
                    &GenEvent::set_pdf_info, DOC(GenEvent.pdf_info))
      .def_property(
          "cross_section",
          overload_cast<GenCrossSectionPtr, GenEvent>(&GenEvent::cross_section),
          &GenEvent::set_cross_section, DOC(GenEvent.cross_section))
      .def_property(
          "attributes",
          [](GenEvent& self) {
            return AttributesView{&self, 0};
          },
          [](GenEvent& self, py::dict obj) {
            auto amv = AttributesView{&self, 0};
            py::cast(amv).attr("clear")();
            for (const auto& kv : obj) {
              amv.setitem(py::cast<py::str>(kv.first),
                          py::reinterpret_borrow<py::object>(kv.second));
            }
          },
          DOC(attributes))
      .def("reserve", &GenEvent::reserve, "particles"_a, "vertices"_a = 0,
           DOC(GenEvent.reserve))
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
           "vz"_a = py::none(), "vt"_a = py::none(), DOC(GenEvent.from_hepevt))
      // clang-format off
      METH(clear, GenEvent)
      PROP(run_info, GenEvent)
      PROP(event_number, GenEvent)
      PROP_RO(momentum_unit, GenEvent)
      PROP_RO(length_unit, GenEvent)
      PROP_RO(weight_names, GenEvent)
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

  py::class_<GenParticle, GenParticlePtr>(m, "GenParticle", DOC(GenParticle))
      .def(py::init<const FourVector&, int, int>(),
           "momentum"_a = py::make_tuple(0, 0, 0, 0), "pid"_a = 0, "status"_a = 0)
      .def(py::self == py::self)
      .def("__repr__",
           [](const GenParticlePtr& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def_property(
          "attributes",
          [](GenParticle& self) {
            return AttributesView{self.parent_event(), self.id()};
          },
          [](GenParticle& self, py::dict obj) {
            auto amv = AttributesView{self.parent_event(), self.id()};
            py::cast(amv).attr("clear")();
            for (const auto& kv : obj) {
              amv.setitem(py::cast<py::str>(kv.first),
                          py::reinterpret_borrow<py::object>(kv.second));
            }
          },
          DOC(attributes))
      // clang-format off
      PROP_RO_OL(parent_event, GenParticle, const GenEvent*)
      PROP_RO(in_event, GenParticle)
      PROP_RO(id, GenParticle)
      // PROP_RO(data, GenParticle) // TODO
      PROP_RO_OL(production_vertex, GenParticle, ConstGenVertexPtr)
      PROP_RO_OL(end_vertex, GenParticle, ConstGenVertexPtr)
      PROP_RO_OL(parents, GenParticle, std::vector<ConstGenParticlePtr>)
      PROP_RO_OL(children, GenParticle, std::vector<ConstGenParticlePtr>)
      PROP(pid, GenParticle)
      PROP_RO(abs_pid, GenParticle)
      PROP(status, GenParticle)
      PROP(momentum, GenParticle)
      PROP(generated_mass, GenParticle)
      METH(unset_generated_mass, GenParticle)
      METH(is_generated_mass_set, GenParticle)
      // clang-format on
      ;

  py::class_<GenVertex, GenVertexPtr>(m, "GenVertex", DOC(GenVertex))
      .def(py::init<const FourVector&>(), "position"_a = FourVector())
      .def(py::self == py::self)
      .def("__repr__",
           [](const GenVertexPtr& self) {
             std::ostringstream os;
             repr(os, self);
             return os.str();
           })
      .def_property(
          "attributes",
          [](GenVertex& self) {
            return AttributesView{self.parent_event(), self.id()};
          },
          [](GenVertex& self, py::dict obj) {
            auto amv = AttributesView{self.parent_event(), self.id()};
            py::cast(amv).attr("clear")();
            for (const auto& kv : obj) {
              amv.setitem(py::cast<py::str>(kv.first),
                          py::reinterpret_borrow<py::object>(kv.second));
            }
          },
          DOC(GenVertex.attributes))
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
      METH(has_set_position, GenVertex)
      // clang-format on
      ;

  // py::class_<GenParticleData>(m, "GenParticleData");
  // py::class_<GenVertexData>(m, "GenVertexData");

  m.def(
      "content",
      [](const GenEvent& event) {
        std::ostringstream os;
        HepMC3::Print::content(os, event);
        return os.str();
      },
      DOC(Print.content));

  m.def(
      "listing",
      [](const GenEvent& event, unsigned short precision = 2) {
        std::ostringstream os;
        HepMC3::Print::listing(os, event, precision);
        return os.str();
      },
      DOC(Print.listing));

  FUNC(equal_particle_sets);
  FUNC(equal_vertex_sets);

  register_io(m);
}
