#include "geneventdata.hpp"
#include <HepMC3/Data/GenEventData.h>
#include <HepMC3/Data/GenParticleData.h>
#include <HepMC3/Data/GenVertexData.h>

using namespace HepMC3;

struct ParticleData {
  int pid;
  int status;
  bool is_mass_set;
  double mass;
  double px, py, pz, e;
};

struct VertexData {
  int status;
  double x, y, z, t;
};

void register_geneventdata_dtypes() {
  PYBIND11_NUMPY_DTYPE(ParticleData, pid, status, is_mass_set, mass, px, py, pz, e);
  PYBIND11_NUMPY_DTYPE(VertexData, status, x, y, z, t);
}

#define MAKE(name, type)                                              \
  py::object GenEventData_##name(py::object self) {                   \
    auto& s = py::cast<GenEventData&>(self);                          \
    py::ssize_t shape[1] = {static_cast<py::ssize_t>(s.name.size())}; \
    auto dt = py::dtype::of<type>();                                  \
    return py::array(dt, shape, s.name.data(), self);                 \
  }

MAKE(weights, double)
MAKE(vertices, VertexData)
MAKE(particles, ParticleData)
MAKE(links1, int)
MAKE(links2, int)

#define MAKES(name)                                 \
  py::object GenEventData_##name(py::object self) { \
    auto& s = py::cast<GenEventData&>(self);        \
    py::list l;                                     \
    for (const auto& str : s.name) l.append(str);   \
    return l;                                       \
  }

MAKES(attribute_id)
MAKES(attribute_name)
MAKES(attribute_string)
