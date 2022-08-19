#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/GenVertex.h"
#include "pybind.h"

#include <array>
#include <unordered_map>
#include <utility>

template <>
struct std::hash<std::pair<int, int>> {
  std::size_t operator()(const std::pair<int, int>& p) const noexcept {
    auto h1 = std::hash<int>{}(p.first);
    auto h2 = std::hash<int>{}(p.second);
    return h1 ^ (h2 << 1); // or use boost::hash_combine
  }
};

bool normalize(int& m1, int& m2) {
  // normalize mother range, see
  // https://pythia.org/latest-manual/ParticleProperties.html
  // m1 == m2 == 0 : no mothers
  // m1 == m2 > 0 : elastic scattering
  // m1 > 0, m2 == 0 : one mother
  // m1 < m2, both > 0: interaction
  // m2 < m1, both > 0: same, needs swapping

  if (m1 > 0 && m2 > 0 && m2 < m1) std::swap(m1, m2);

  if (m1 > 0 && m2 == 0) m2 = m1;

  return m2 == 0;
}

namespace HepMC3 {

void from_hepevt(GenEvent& event, int event_number, py::array_t<double> momentum,
                 py::array_t<double> mass, py::array_t<double> position,
                 py::array_t<int> pid, py::array_t<int> status, py::object parents,
                 py::object children) {

  namespace py = pybind11;

  const bool has_parents = !parents.is_none();
  const bool has_children = !children.is_none();

  if (mass.request().ndim != 1) throw std::runtime_error("m must be 1D");
  if (pid.request().ndim != 1) throw std::runtime_error("pid must be 1D");
  if (status.request().ndim != 1) throw std::runtime_error("status must be 1D");

  if (momentum.request().ndim != 2) throw std::runtime_error("p must be 2D");
  if (position.request().ndim != 2) throw std::runtime_error("v must be 2D");
  if (has_parents && py::cast<py::array_t<int>>(parents).request().ndim != 2)
    throw std::runtime_error("parent must be 2D");
  if (has_children && py::cast<py::array_t<int>>(children).request().ndim != 2)
    throw std::runtime_error("children must be 2D");

  auto rm = mass.unchecked<1>();
  auto rpid = pid.unchecked<1>();
  auto rsta = status.unchecked<1>();

  auto rp = momentum.unchecked<2>();
  auto rv = position.unchecked<2>();

  std::array<py::ssize_t, 2> shape = {rm.shape(0), 2};
  if (!has_parents) parents = py::array_t<int>(shape);
  if (!has_children) children = py::array_t<int>(shape);

  auto rpar = py::cast<py::array_t<int>>(parents).unchecked<2>();
  auto rchi = py::cast<py::array_t<int>>(children).unchecked<2>();

  const int n = rm.shape(0);
  if (rp.shape(0) != n || rv.shape(0) != n || rpid.shape(0) != n ||
      rsta.shape(0) != n || rpar.shape(0) != n || rchi.shape(0) != n)
    throw std::runtime_error(
        "p, m, v, pid, parents, children, status must have same length");

  if (rp.shape(1) != 4) throw std::runtime_error("p must have shape (N, 4)");

  if (rv.shape(1) != 4) throw std::runtime_error("v must have shape (N, 4)");

  event.clear();
  event.reserve(n);
  event.set_event_number(event_number);

  // first pass, only add unique vertices
  // particles with same ancestor(s) have the same starting vertex
  std::unordered_map<std::pair<int, int>, int> vmap;
  for (int i = 0; i < n; ++i) {
    auto p = new GenParticle(FourVector(rp(i, 0), rp(i, 1), rp(i, 2), rp(i, 3)),
                             rpid(i), rsta(i));
    p->set_generated_mass(rm(i));
    event.add_particle(p);

    // if particle has no mother, it is beam
    bool is_beam = rpar(i, 0) == rpar(i, 1) == 0;

    if (!is_beam) vmap.emplace(std::make_pair(rpar(i, 0), rpar(i, 1)), i);
  }

  auto& particles = event.particles();

  for (const auto& vx : vmap) {

    int m1 = vx.first.first;
    int m2 = vx.first.second;
    if (normalize(m1, m2)) continue;

    const int i = vx.second;
    auto v = new GenVertex(FourVector(rv(i, 0), rv(i, 1), rv(i, 2), rv(i, 3)));
    event.add_vertex(v);

    for (int k = m1; k <= m2; ++k) v->add_particle_in(particles.at(k));

    // add any daugthers from mother
    // normalize daugther range, same rules as for mothers
    int d1 = rchi(m1, 0);
    int d2 = rchi(m1, 1);
    if (normalize(d1, d2)) continue;

    for (int k = d1; k <= d2; ++k) v->add_particle_out(particles.at(k));
  }
}

} // namespace HepMC3
