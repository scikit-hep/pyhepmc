#include "pybind.hpp"
#include <HepMC3/Data/GenEventData.h>
#include <HepMC3/Data/GenParticleData.h>
#include <HepMC3/Data/GenVertexData.h>
#include <vector>

struct FourPos {
  double x, y, z, t;
};

struct VertexData {
  int status;
  FourPos position;
};

struct FourMom {
  double px, py, pz, e;
};

struct ParticleData {
  int pid;
  int status;
  bool is_mass_set;
  double mass;
  FourMom momentum;
};

namespace HepMC3 {

py::object particledata_asarray(std::vector<GenParticleData>& self) {
  PYBIND11_NUMPY_DTYPE(FourMom, px, py, pz, e);
  PYBIND11_NUMPY_DTYPE(ParticleData, pid, status, is_mass_set, mass, momentum);
  auto dt = py::dtype::of<ParticleData>();
  ssize_t shape[1] = {static_cast<ssize_t>(self.size())};
  return py::array(dt, shape, self.data());
}

py::object vertexdata_asarray(std::vector<GenVertexData>& self) {
  PYBIND11_NUMPY_DTYPE(FourPos, x, y, z, t);
  PYBIND11_NUMPY_DTYPE(VertexData, status, position);
  auto dt = py::dtype::of<VertexData>();
  ssize_t shape[1] = {static_cast<ssize_t>(self.size())};
  return py::array(dt, shape, self.data());
}

} // namespace HepMC3
