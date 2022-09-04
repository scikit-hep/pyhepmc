#ifndef PYHEPMC_UNPARSEDATTRIBUTE_HPP
#define PYHEPMC_UNPARSEDATTRIBUTE_HPP

#include "pointer.hpp"
#include "pybind.hpp"
#include <cstdint>

namespace HepMC3 {

py::object unparsed_attribute_to_python(AttributePtr& unparsed, py::object pytype);

struct UnparsedAttribute {
  AttributePtr& parent_;

  py::object astype(py::object pytype) {
    return unparsed_attribute_to_python(parent_, pytype);
  }
};

} // namespace HepMC3

#endif
