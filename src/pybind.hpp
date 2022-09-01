#ifndef PYHEPMC_PYBIND_HPP
#define PYHEPMC_PYBIND_HPP

#include <pybind11/numpy.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace py::literals;

template <
    class R, class C, class... Args,
    class _T = typename std::conditional<
        std::is_const<C>::value, R (C::*)(Args...) const, R (C::*)(Args...)>::type>
_T overload_cast(_T x) {
  return x;
}

#define FUNC(name) m.def(#name, name, doc[#name].c_str())
#define PROP_RO(name, cls) \
  .def_property_readonly(#name, &cls::name, doc[#cls "." #name].c_str())
#define PROP_ROS(name, cls) \
  .def_property_readonly_static(#name, &cls::name, doc[#cls "." #name].c_str())
#define PROP_RO_OL(name, cls, rval)                                         \
  .def_property_readonly(#name, overload_cast<rval, const cls>(&cls::name), \
                         doc[#cls "." #name].c_str())
#define PROP(name, cls) \
  .def_property(#name, &cls::name, &cls::set_##name, doc[#cls "." #name].c_str())
#define PROP2(name, cls) \
  .def_property(#name, &cls::get_##name, &cls::set_##name, doc[#cls "." #name].c_str())
#define PROP_OL(name, cls, rval)                                                     \
  .def_property(#name, overload_cast<rval, const cls>(&cls::name), &cls::set_##name, \
                doc[#cls "." #name].c_str())
#define METH(name, cls) .def(#name, &cls::name, doc[#cls "." #name].c_str())
#define METH_OL(name, cls, rval, args) \
  .def(#name, (rval(cls::*)(args)) & cls::name, doc[#cls "." #name].c_str())
#define ATTR(name, cls) .def_readwrite(#name, &cls::name, doc[#cls "." #name].c_str())

#define DOC(name) doc[#name].c_str()

#endif
