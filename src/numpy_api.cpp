#include "numpy_api.hpp"

#define NP_ARRAY(cls, kind, type, method)                           \
  .def_property_readonly(#method, [](cls& self) {                   \
    using namespace HepMC3;                                         \
    const GenEvent& event = py::cast<const GenEvent&>(self.event_); \
    const auto& x = event.kind();                                   \
    py::array_t<type> a(x.size());                                  \
    auto a2 = a.mutable_unchecked<1>();                             \
    for (size_t i = 0; i < x.size(); ++i) a2[i] = x[i]->method();   \
    return a;                                                       \
  })

#define NP_ARRAY2(cls, kind, type, method1, method2)                         \
  .def_property_readonly(#method2, [](cls& self) {                           \
    using namespace HepMC3;                                                  \
    const GenEvent& event = py::cast<const GenEvent&>(self.event_);          \
    const auto& x = event.kind();                                            \
    py::array_t<type> a(x.size());                                           \
    auto a2 = a.mutable_unchecked<1>();                                      \
    for (size_t i = 0; i < x.size(); ++i) a2[i] = x[i]->method1().method2(); \
    return a;                                                                \
  })

void register_numpy_api(py::module& m) {
  py::class_<ParticlesAPI>(m, "ParticlesAPI")
      .def(py::init<py::object>())
      // clang-format off
      NP_ARRAY(ParticlesAPI, particles, int, id)
      NP_ARRAY(ParticlesAPI, particles, int, pid)
      NP_ARRAY(ParticlesAPI, particles, int, status)
      NP_ARRAY(ParticlesAPI, particles, bool, is_generated_mass_set)
      NP_ARRAY(ParticlesAPI, particles, double, generated_mass)
      NP_ARRAY2(ParticlesAPI, particles, double, momentum, px)
      NP_ARRAY2(ParticlesAPI, particles, double, momentum, py)
      NP_ARRAY2(ParticlesAPI, particles, double, momentum, pz)
      NP_ARRAY2(ParticlesAPI, particles, double, momentum, e)
      // clang-format on
      ;

  py::class_<VerticesAPI>(m, "VerticesAPI")
      .def(py::init<py::object>())
      // clang-format off
      NP_ARRAY(VerticesAPI, vertices, int, id)
      NP_ARRAY(VerticesAPI, vertices, int, status)
      NP_ARRAY(VerticesAPI, vertices, bool, has_set_position)
      NP_ARRAY2(VerticesAPI, vertices, double, position, x)
      NP_ARRAY2(VerticesAPI, vertices, double, position, y)
      NP_ARRAY2(VerticesAPI, vertices, double, position, z)
      NP_ARRAY2(VerticesAPI, vertices, double, position, t)
      // clang-format on
      ;

  py::class_<NumpyAPI>(m, "NumpyAPI")
      .def_property_readonly("particles",
                             [](NumpyAPI& self) { return ParticlesAPI(self.event_); })
      .def_property_readonly("vertices",
                             [](NumpyAPI& self) { return VerticesAPI(self.event_); });
}
