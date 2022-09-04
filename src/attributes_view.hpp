#ifndef PYHEPMC_ATTRIBUTEMAPVIEW_HPP
#define PYHEPMC_ATTRIBUTEMAPVIEW_HPP

#include "HepMC3/Attribute.h"
#include "pointer.hpp"
#include "pybind.hpp"
#include <map>
#include <memory>
#include <string>

namespace HepMC3 {

class GenRunInfo;
class GenEvent;
class Attribute;

struct AttributesView {
  using AttributeIdMap = std::map<int, AttributePtr>;
  using AttributeMap = std::map<std::string, AttributeIdMap>;

  GenEvent* event_;
  int id_;

  struct Iter {
    using iterator = AttributeMap::iterator;
    iterator it_, end_;
    int id_;
    py::object next();
  };

  Iter iter();
  py::object getitem(py::str name);
  void setitem(py::str name, py::object value);
  void delitem(py::str name);
  bool contains(py::str name);
  py::ssize_t len();
  AttributeMap& attributes();
};

struct RunInfoAttributesView {
  using AttributeMap = std::map<std::string, AttributePtr>;
  using iterator = typename AttributeMap::iterator;

  GenRunInfoPtr run_info_;

  struct Iter {
    using iterator = AttributeMap::iterator;
    iterator it_, end_;
    py::object next();
  };

  Iter iter();
  py::object getitem(py::str name);
  void setitem(py::str name, py::object value);
  void delitem(py::str name);
  bool contains(py::str name);
  py::ssize_t len();
  AttributeMap& attributes();
  iterator find(py::str name);
  iterator end();
};

py::object attribute_to_python(AttributePtr& a);
AttributePtr attribute_from_python(py::object obj);

} // namespace HepMC3

#endif
