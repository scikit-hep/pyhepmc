#ifndef PYHEPMC_GENEVENTDATA_HPP
#define PYHEPMC_GENEVENTDATA_HPP

#include "pybind.hpp"

py::object GenEventData_particles(py::object);
py::object GenEventData_vertices(py::object);
py::object GenEventData_weights(py::object);
py::object GenEventData_links1(py::object);
py::object GenEventData_links2(py::object);
py::object GenEventData_attribute_id(py::object);
py::object GenEventData_attribute_name(py::object);
py::object GenEventData_attribute_string(py::object);

void register_geneventdata_dtypes();

#endif
