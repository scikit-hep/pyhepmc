#include "attributes_view.hpp"
#include "pointer.hpp"
#include "pybind.hpp"
#include <HepMC3/GenEvent.h>
#include <accessor/accessor.hpp>
#include <algorithm>
#include <cassert>
#include <map>
#include <pybind11/detail/common.h>
#include <pybind11/pytypes.h>
#include <pyerrors.h>
#include <set>
#include <sstream>
#include <string>

// To avoid the superfluous copy, we use the legal crowbar
// to access the private attribute map of GenEvent
MEMBER_ACCESSOR(MA1, HepMC3::GenEvent, m_attributes,
                HepMC3::AttributesView::AttributeMap)

namespace HepMC3 {

py::object AttributesView::Iter::next() {
  while (it_ != end_) {
    auto& amap2 = it_->second;
    if (amap2.find(id_) != amap2.end()) return py::cast(it_++->first);
    ++it_;
  }
  throw py::stop_iteration();
}

AttributesView::Iter AttributesView::iter() {
  auto& amap = attributes();
  return {amap.begin(), amap.end(), id_};
}

py::object AttributesView::getitem(py::str name) {
  auto& amap = attributes();
  auto it = amap.find(py::cast<std::string>(name));
  if (it != amap.end()) {
    auto& amap2 = it->second;
    auto jt = amap2.find(id_);
    if (jt != amap2.end()) return attribute_to_python(jt->second);
  }
  throw py::key_error(name);
  return {};
}

void AttributesView::setitem(py::str name, py::object value) {
  auto a = attribute_from_python(value);
  // add_attribute has desired side-effects:
  // it connects Attribute to event, particle, vertex
  assert(event_);
  event_->add_attribute(py::cast<std::string>(name), a, id_);
}

void AttributesView::delitem(py::str name) {
  // cannot use GenEvent::remove_attribute because it does
  // not signal when attribute does not exist
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

bool AttributesView::contains(py::str name) {
  auto& amap = attributes();
  auto it = amap.find(py::cast<std::string>(name));
  if (it == amap.end()) return false;
  auto& amap2 = it->second;
  return amap2.find(id_) != amap2.end();
}

AttributesView::AttributeMap& AttributesView::attributes() {
  auto ref = accessor::accessMember<MA1>(*event_);
  return ref.get();
}

py::ssize_t AttributesView::len() {
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
