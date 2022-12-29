#include "UnparsedAttribute.hpp"
#include "pointer.hpp"
#include "pybind.hpp"
#include <HepMC3/AssociatedParticle.h>
#include <HepMC3/Attribute.h>
#include <HepMC3/GenCrossSection.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenHeavyIon.h>
#include <HepMC3/GenParticle_fwd.h>
#include <HepMC3/GenPdfInfo.h>
#include <HepMC3/LHEFAttributes.h>
#include <accessor/accessor.hpp>
#include <boost/mp11/algorithm.hpp>
#include <boost/mp11/list.hpp>
#include <boost/mp11/utility.hpp>
#include <cassert>
#include <memory>
#include <pybind11/detail/common.h>
#include <pybind11/pytypes.h>
#include <sstream>
#include <stdexcept>

MEMBER_ACCESSOR(A1, HepMC3::Attribute, m_event, const HepMC3::GenEvent*)
MEMBER_ACCESSOR(A2, HepMC3::Attribute, m_particle, HepMC3::GenParticlePtr)
MEMBER_ACCESSOR(A3, HepMC3::Attribute, m_vertex, HepMC3::GenVertexPtr)

namespace HepMC3 {

template <class TPtr>
py::object value_to_python(TPtr a) {
  return py::cast(a->value());
}
py::object value_to_python(AssociatedParticlePtr a) {
  return py::cast(a->associated());
}
py::object value_to_python(GenCrossSectionPtr a) { return py::cast(a); }
py::object value_to_python(GenHeavyIonPtr a) { return py::cast(a); }
py::object value_to_python(GenPdfInfoPtr a) { return py::cast(a); }
py::object value_to_python(HEPRUPAttributePtr a) { return py::cast(a); }
py::object value_to_python(HEPEUPAttributePtr a) { return py::cast(a); }

py::object attribute_to_python(AttributePtr& a) {
  using namespace boost::mp11;

  if (!a->is_parsed()) return py::cast(UnparsedAttribute{a});

  // Must cover all C++ attribute types derived from Attribute.
  // AssociatedParticle derives from IntAttribute; must come first.

  using RawTypes =
      mp_list<GenCrossSection, GenHeavyIon, GenPdfInfo, HEPRUPAttribute,
              HEPEUPAttribute, AssociatedParticle, BoolAttribute, IntAttribute,
              LongAttribute, DoubleAttribute, FloatAttribute, StringAttribute,
              CharAttribute, LongLongAttribute, LongDoubleAttribute, UIntAttribute,
              ULongLongAttribute, VectorCharAttribute, VectorFloatAttribute,
              VectorLongDoubleAttribute, VectorLongLongAttribute, VectorUIntAttribute,
              VectorULongAttribute, VectorULongLongAttribute, VectorIntAttribute,
              VectorLongIntAttribute, VectorDoubleAttribute, VectorStringAttribute>;
  // use mp_identity to make sure that default ctor is a noop
  using Types = mp_transform<mp_identity, RawTypes>;
  py::object result;
  mp_for_each<Types>([&](auto t) {
    using AttributeType = typename decltype(t)::type;
    if (result) return;
    if (auto x = std::dynamic_pointer_cast<AttributeType>(a))
      result = value_to_python(x);
  });
  if (!result) throw std::runtime_error("Attribute not convertible to Python type");
  return result;
}

template <class T>
bool convert(AttributePtr& unparsed, py::object pytype, py::object other,
             py::object& result) {
  if (pytype.is(other)) {
    auto a = std::make_shared<T>();
    // must be done before calling from_string() and init()
    accessor::accessMember<A1>(*a).get() = unparsed->event();
    accessor::accessMember<A2>(*a).get() = unparsed->particle();
    accessor::accessMember<A3>(*a).get() = unparsed->vertex();
    if (a->from_string(unparsed->unparsed_string()) && a->init()) {
      result = value_to_python(a);
      unparsed = std::move(a);
      return true;
    }
  }
  return false;
}

py::object unparsed_attribute_to_python(AttributePtr& unparsed, py::object pytype) {
  py::module_ builtins = py::module_::import("builtins");
  auto bool_type = builtins.attr("bool");
  auto int_type = builtins.attr("int");
  auto float_type = builtins.attr("float");
  auto str_type = builtins.attr("str");
  auto list_type = builtins.attr("list");
  py::module_ pyhepmc = py::module_::import("pyhepmc");
  auto particle_type = pyhepmc.attr("GenParticle");
  auto pdfinfo_type = pyhepmc.attr("GenPdfInfo");
  auto heavyion_type = pyhepmc.attr("GenHeavyIon");
  auto crosssection_type = pyhepmc.attr("GenCrossSection");
  auto heprup_type = pyhepmc.attr("HEPRUPAttribute");
  auto hepeup_type = pyhepmc.attr("HEPEUPAttribute");
  py::module_ typing = py::module_::import("typing");
  auto get_origin = typing.attr("get_origin");
  auto get_args = typing.attr("get_args");
  auto list2_type = typing.attr("List");

  // Convert the internal attribute as well as the Python return value;
  // see template<class T> std::shared_ptr<T>
  // GenEvent::attribute(const std::string &name,  const int& id) const

  py::object result;

  // handle lists first
  if ((pytype.is(list_type) || pytype.is(list2_type)))
    throw py::type_error("cannot convert UnparsedAttribute to untyped list");

  if (get_origin(pytype).is(list_type)) {
    py::object subtype = get_args(pytype)[py::int_(0)];
    if (!(convert<VectorIntAttribute>(unparsed, subtype, int_type, result) ||
          convert<VectorDoubleAttribute>(unparsed, subtype, float_type, result) ||
          convert<VectorStringAttribute>(unparsed, subtype, str_type, result))) {
      std::ostringstream msg;
      msg << "cannot convert UnparsedAttribute to type List["
          << py::cast<std::string>(subtype.attr("__name__")) << "]";
      throw py::type_error(msg.str());
    }
  } else {
    if (!(convert<BoolAttribute>(unparsed, pytype, bool_type, result) ||
          convert<IntAttribute>(unparsed, pytype, int_type, result) ||
          convert<DoubleAttribute>(unparsed, pytype, float_type, result) ||
          convert<StringAttribute>(unparsed, pytype, str_type, result) ||
          convert<AssociatedParticle>(unparsed, pytype, particle_type, result) ||
          convert<GenPdfInfo>(unparsed, pytype, pdfinfo_type, result) ||
          convert<GenCrossSection>(unparsed, pytype, crosssection_type, result) ||
          convert<GenHeavyIon>(unparsed, pytype, heavyion_type, result) ||
          convert<HEPRUPAttribute>(unparsed, pytype, heprup_type, result) ||
          convert<HEPEUPAttribute>(unparsed, pytype, hepeup_type, result))) {
      std::ostringstream msg;
      msg << "cannot convert UnparsedAttribute to type "
          << py::cast<std::string>(pytype.attr("__name__"));
      throw py::type_error(msg.str());
    }
  }
  return result;
}

AttributePtr attribute_from_python(py::object obj) {
  using namespace boost::mp11;

  AttributePtr result;

  if (py::isinstance<GenPdfInfo>(obj)) {
    result = py::cast<GenPdfInfoPtr>(obj);
  } else if (py::isinstance<GenHeavyIon>(obj)) {
    result = py::cast<GenHeavyIonPtr>(obj);
  } else if (py::isinstance<GenCrossSection>(obj)) {
    result = py::cast<GenCrossSectionPtr>(obj);
  } else if (py::isinstance<HEPRUPAttribute>(obj)) {
    result = py::cast<HEPRUPAttributePtr>(obj);
  } else if (py::isinstance<HEPEUPAttribute>(obj)) {
    result = py::cast<HEPEUPAttributePtr>(obj);
  } else if (py::isinstance<GenParticle>(obj)) {
    auto p = py::cast<GenParticlePtr>(obj);
    result = std::make_shared<AssociatedParticle>(p);
  }

  if (!result) {
    using Types = mp_list<mp_list<BoolAttribute, py::bool_, bool>,
                          mp_list<IntAttribute, py::int_, int>,
                          mp_list<DoubleAttribute, py::float_, double>,
                          mp_list<StringAttribute, py::str, std::string>>;

    mp_for_each<Types>([&](auto t) {
      using T = decltype(t);
      using AT = mp_at_c<T, 0>;
      using PT = mp_at_c<T, 1>;
      using CT = mp_at_c<T, 2>;
      if (!result && py::isinstance<PT>(obj)) {
        auto a = std::make_shared<AT>();
        a->set_value(py::cast<CT>(obj));
        result = a;
      }
    });
  }

  if (!result && py::isinstance<py::iterable>(obj) && py::len(obj) > 0) {
    using Types = mp_list<mp_list<VectorIntAttribute, py::int_, int>,
                          mp_list<VectorDoubleAttribute, py::float_, double>,
                          mp_list<VectorStringAttribute, py::str, std::string>>;

    py::int_ zero(0);
    mp_for_each<Types>([&](auto t) {
      using T = decltype(t);
      using AT = mp_at_c<T, 0>;
      using PT = mp_at_c<T, 1>;
      using CT = std::vector<mp_at_c<T, 2>>;
      auto item = py::reinterpret_borrow<py::object>(obj[zero]);
      if (!result && py::isinstance<PT>(item)) {
        auto a = std::make_shared<AT>();
        a->set_value(py::cast<CT>(obj));
        result = a;
      }
    });
  }

  if (!result) {
    std::ostringstream msg;
    msg << py::cast<std::string>(obj.attr("__class__").attr("__name__"))
        << " not convertible to Attribute";
    throw std::runtime_error(msg.str());
  }
  return result;
}

} // namespace HepMC3
