#include <HepMC3/GenEvent.h>
#include <HepMC3/GenParticle.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace HepMC3;

void register_bench(py::module& m) {
  m.def("_sum_energy_of_protons", [](GenEvent& event) {
    double esum = 0;
    for (auto&& p : event.particles()) {
      if (std::abs(p->pdg_id()) != 2212) continue;
      if (p->status() != 1) continue;
      esum += p->momentum().e();
    }
    return esum;
  });
}
