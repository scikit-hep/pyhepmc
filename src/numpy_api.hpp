#ifndef PYHEPMC_NUMPY_API_HPP
#define PYHEPMC_NUMPY_API_HPP

#include <HepMC3/GenEvent.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenVertex.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

struct NumpyAPI {
  py::object event_;
  NumpyAPI(py::object event) : event_{event} {}
};

struct ParticlesAPI : NumpyAPI {
  using NumpyAPI::NumpyAPI;
};
struct VerticesAPI : NumpyAPI {
  using NumpyAPI::NumpyAPI;
};

void register_numpy_api(py::module& m);

#endif
