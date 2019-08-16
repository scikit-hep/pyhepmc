#ifndef PYHEPMC_PYBIND_HEADER
#define PYHEPMC_PYBIND_HEADER

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace py::literals;

#define FUNC(name) m.def(#name, name)
#define PROP_RO(name, cls) .def_property_readonly(#name, &cls::name)
#define PROP_RO_OL(name, cls, rval) .def_property_readonly(#name, (rval (cls::*)() const) &cls::name)
#define PROP(name, cls) .def_property(#name, &cls::name, &cls::set_##name)
#define PROP_OL(name, cls, rval) .def_property(#name, (rval (cls::*)() const) &cls::name, &cls::set_##name)
#define METH(name, cls) .def(#name, &cls::name)
#define METH_OL(name, cls, rval, args) .def(#name, (rval (cls::*)(args)) &cls::name)

#endif
