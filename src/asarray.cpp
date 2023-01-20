#include "pybind.hpp"
#include <HepMC3/Data/GenEventData.h>
#include <HepMC3/Data/GenParticleData.h>
#include <HepMC3/Data/GenVertexData.h>
#include <vector>

namespace HepMC3 {

py::object particledata_asarray(std::vector<GenParticleData>& self) {
  auto dt = py::dtype::of<ParticleData>();
  ssize_t shape[1] = {static_cast<ssize_t>(self.size())};
  return py::array(dt, shape, static_cast<void*>(self.data()));
}

py::object vertexdata_asarray(std::vector<GenVertexData>& self) {
  auto dt = py::dtype::of<VertexData>();
  ssize_t shape[1] = {static_cast<ssize_t>(self.size())};
  return py::array(dt, shape, static_cast<void*>(self.data()));
}

} // namespace HepMC3
