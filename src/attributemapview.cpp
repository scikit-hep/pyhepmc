#include "attributemapview.hpp"
#include "pointer.hpp"
#include "pybind.hpp"
#include <HepMC3/Attribute.h>
#include <HepMC3/GenCrossSection.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenHeavyIon.h>
#include <HepMC3/GenPdfInfo.h>
#include <HepMC3/LHEFAttributes.h>
#include <accessor/accessor.hpp>
#include <algorithm>
#include <boost/mp11/algorithm.hpp>
#include <boost/mp11/list.hpp>
#include <boost/mp11/utility.hpp>
#include <map>
#include <pybind11/detail/common.h>
#include <pybind11/pytypes.h>
#include <pyerrors.h>
#include <set>
#include <sstream>
#include <string>

namespace HepMC3 {
using AttributeIdMap = std::map<int, AttributePtr>;
using AttributeMap = std::map<std::string, AttributeIdMap>;
} // namespace HepMC3

// To avoid a superfluous copy, use legal evil to get private access
// to attribute map of GenEvent
MEMBER_ACCESSOR(MA1, HepMC3::GenEvent, m_attributes, HepMC3::AttributeMap)

namespace HepMC3 {
py::object AttributeMapView::Iter::next() {
  while (it_ != end_) {
    auto& amap2 = it_->second;
    if (amap2.find(id_) != amap2.end()) return py::cast(it_++->first);
    ++it_;
  }
  throw py::stop_iteration();
}

AttributeMapView::Iter AttributeMapView::iter() {
  auto& amap = attributes();
  return {amap.begin(), amap.end(), id_};
}

py::object AttributeMapView::getitem(py::str name) {
  auto& amap = attributes();
  auto it = amap.find(py::cast<std::string>(name));
  if (it != amap.end()) {
    auto& amap2 = it->second;
    auto jt = amap2.find(id_);
    if (jt != amap2.end()) return to_python(jt->second);
  }
  throw py::key_error(name);
  return {};
}

void AttributeMapView::setitem(py::str name, py::object value) {
  auto& amap = attributes();
  auto& amap2 = amap[py::cast<std::string>(name)];
  amap2.emplace(id_, from_python(value));
}

void AttributeMapView::delitem(py::str name) {
  auto& amap = attributes();
  auto it = amap.find(py::cast<std::string>(name));
  if (it != amap.end()) {
    auto& amap2 = it->second;
    auto jt = amap2.find(id_);
    if (jt != amap2.end()) {
      amap2.erase(jt);
      return;
    }
  }
  throw py::key_error(name);
}

bool AttributeMapView::contains(py::str name) {
  auto& amap = attributes();
  auto it = amap.find(py::cast<std::string>(name));
  if (it == amap.end()) return false;
  auto& amap2 = it->second;
  return amap2.find(id_) != amap2.end();
}

AttributeMap& AttributeMapView::attributes() {
  auto ref = accessor::accessMember<MA1>(*event_);
  return ref.get();
}

py::object AttributeMapView::to_python(AttributePtr a) {
  using namespace boost::mp11;

  // this implementation must cover all C++ attribute types derived from Attribute

  py::object result;

  using RawTypes = mp_list<GenCrossSection, GenHeavyIon, GenPdfInfo, HEPRUPAttribute,
                           HEPEUPAttribute>;
  // use mp_identity to make sure that default ctor is a noop
  using Types = mp_transform<mp_identity, RawTypes>;
  // this loop has exactly one match if any
  mp_for_each<Types>([&](auto t) {
    using AttributeType = typename decltype(t)::type;
    if (auto x = std::dynamic_pointer_cast<AttributeType>(a)) result = py::cast(x);
  });

  if (!result) {

    using RawTypes =
        mp_list<IntAttribute, LongAttribute, DoubleAttribute, FloatAttribute,
                StringAttribute, CharAttribute, LongLongAttribute, LongDoubleAttribute,
                UIntAttribute, ULongLongAttribute, BoolAttribute, VectorCharAttribute,
                VectorFloatAttribute, VectorLongDoubleAttribute,
                VectorLongLongAttribute, VectorUIntAttribute, VectorULongAttribute,
                VectorULongLongAttribute, VectorIntAttribute, VectorLongIntAttribute,
                VectorDoubleAttribute, VectorStringAttribute>;

    using Types = mp_transform<mp_identity, RawTypes>;
    // this loop has exactly one match if any
    mp_for_each<Types>([&](auto t) {
      using AttributeType = typename decltype(t)::type;
      if (auto x = std::dynamic_pointer_cast<AttributeType>(a))
        result = py::cast(x->value());
    });
  }

  if (!result) throw std::runtime_error("Attribute not convertible to Python type");
  return result;
}

AttributePtr AttributeMapView::from_python(py::object obj) {
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
  }

  if (!result) {
    using Types = mp_list<mp_list<BoolAttribute, py::bool_, bool>,
                          mp_list<IntAttribute, py::int_, int>,
                          mp_list<FloatAttribute, py::float_, double>,
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

  if (!result) throw std::runtime_error("Python type not convertible to Attribute");
  return result;
}

py::ssize_t AttributeMapView::len() {
  py::size_t n = 0;
  auto& amap = attributes();
  for (auto& kv : amap) {
    auto& amap2 = kv.second;
    auto it = amap2.find(id_);
    if (it != amap2.end()) ++n;
  }
  return n;
}

} // namespace HepMC3
