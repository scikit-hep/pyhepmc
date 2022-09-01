#include "attributes_view.hpp"
#include "pointer.hpp"
#include "pybind.hpp"
#include <HepMC3/GenRunInfo.h>
#include <accessor/accessor.hpp>
#include <algorithm>
#include <map>
#include <pybind11/detail/common.h>
#include <pybind11/pytypes.h>
#include <pyerrors.h>
#include <set>
#include <sstream>
#include <string>

// To avoid the superfluous copy, we use the legal crowbar
// to access the private attribute map of GenRunInfo
MEMBER_ACCESSOR(MA2, HepMC3::GenRunInfo, m_attributes,
                HepMC3::RunInfoAttributesView::AttributeMap)

namespace HepMC3 {
py::object RunInfoAttributesView::Iter::next() {
  if (it_ != end_) return py::cast(it_++->first);
  throw py::stop_iteration();
}

RunInfoAttributesView::Iter RunInfoAttributesView::iter() {
  auto& m = attributes();
  return {m.begin(), m.end()};
}

py::object RunInfoAttributesView::getitem(py::str name) {
  auto it = find(name);
  if (it == attributes().end()) throw py::key_error(name);
  return attribute_to_python(it->second);
}

void RunInfoAttributesView::setitem(py::str name, py::object value) {
  auto& amap = attributes();
  amap[py::cast<std::string>(name)] = attribute_from_python(value);
}

void RunInfoAttributesView::delitem(py::str name) {
  auto it = find(name);
  if (it == attributes().end()) throw py::key_error(name);
  attributes().erase(it);
}

bool RunInfoAttributesView::contains(py::str name) {
  return find(name) != attributes().end();
}

RunInfoAttributesView::AttributeMap& RunInfoAttributesView::attributes() {
  auto ref = accessor::accessMember<MA2>(*run_info_);
  return ref.get();
}

py::ssize_t RunInfoAttributesView::len() {
  return static_cast<py::ssize_t>(attributes().size());
}

RunInfoAttributesView::iterator RunInfoAttributesView::find(py::str name) {
  return attributes().find(py::cast<std::string>(name));
}

} // namespace HepMC3
