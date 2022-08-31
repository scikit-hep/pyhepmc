#ifndef PYHEPMC_ATTRIBUTEMAPVIEW_HPP
#define PYHEPMC_ATTRIBUTEMAPVIEW_HPP

#include "pybind.hpp"
#include <map>
#include <memory>
#include <string>

namespace HepMC3 {

class GenEvent;
class Attribute;

struct AttributeMapView {
  using AttributePtr = std::shared_ptr<Attribute>;
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
  py::object to_python(AttributePtr a);
  AttributePtr from_python(py::object obj);
};

} // namespace HepMC3

#endif
