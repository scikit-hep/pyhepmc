#include "pybind.hpp"
#include <HepMC3/Errors.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenVertex.h>
#include <array>
#include <cassert>
#include <map>
#include <utility>
#include <vector>

template <>
struct std::less<std::pair<int, int>> {
  bool operator()(const std::pair<int, int>& a,
                  const std::pair<int, int>& b) const noexcept {
    if (a.first == b.first) return a.second < b.second;
    return a.first < b.first;
  }
};

void normalize(int& m1, int& m2, bool fortran) {
  // normalize mother range, see
  // https://pythia.org/latest-manual/ParticleProperties.html
  //   m1 == m2 == 0 : no mothers
  //   m1 == m2 > 0 : elastic scattering
  //   m1 > 0, m2 == 0 : one mother
  //   m1 < m2, both > 0: interaction
  //   m2 < m1, both > 0: same, needs swapping
  // If the input is coming from C, all indices one less.
  // After normalization, we want m1, m2 to be a valid
  // c-style integer range, where m2 points one past the
  // last included index or m1 == m2 (empty range).

  const int invalid = fortran ? 0 : -1;

  if (m1 > invalid && m2 == invalid)
    m2 = m1;
  else if (m2 < m1)
    std::swap(m1, m2);

  if (fortran)
    --m1;
  else
    ++m2;

  // postcondition after normalize
  assert((m1 == 0 && m2 == 0) || m1 < m2);
}

namespace HepMC3 {

void modded_add_particle_in(int vid, GenVertexPtr v, GenParticlePtr p) {
  // Particle can only have one end vertex in HepMC3. Default is to reassign so
  // that the later end vertex gets the particle. We change this here so that
  // the first vertex keeps the particle. This is safer, because otherwise the
  // first vertex may end up without incoming particles.
  if (p->end_vertex()) {
    // clang-format off
    HEPMC3_DEBUG(10,"from_hepevt: vertex -" << vid << ": skipping incoming particle " << p->id() << " which already has end_vertex " << p->end_vertex()->id());
    // clang-format on
  } else
    v->add_particle_in(p);
}

void connect_parents_and_children(GenEvent& event, bool parents,
                                  py::array_t<int> parents_or_children, py::object vx,
                                  py::object vy, py::object vz, py::object vt,
                                  bool fortran) {

  if (parents_or_children.request().ndim != 2)
    throw std::runtime_error("parents or children must be 2D");

  auto rco = parents_or_children.unchecked<2>();

  const std::vector<GenParticlePtr>& particles = event.particles();
  const int n = particles.size();
  if (rco.shape(0) != n || rco.shape(1) != 2)
    throw std::runtime_error("parents or children must have shape (N, 2)");

  // find unique vertices:
  // particles with same parents or children share one vertex
  // if parents: map from parents to children
  // if children: map from children to parents
  std::map<std::pair<int, int>, std::vector<int>> vmap;
  const int invalid = fortran ? 0 : -1;
  for (int i = 0; i < n; ++i) {
    if (rco(i, 0) <= invalid && rco(i, 1) <= invalid) continue;
    vmap[std::make_pair(rco(i, 0), rco(i, 1))].push_back(i);
  }

  const int has_vertex = !vx.is_none() + !vy.is_none() + !vz.is_none() + !vt.is_none();

  if (has_vertex && has_vertex != 4)
    throw std::runtime_error("if one of vx, vy, vz, vt is set, all must be set");

  py::array_t<double> avx;
  py::array_t<double> avy;
  py::array_t<double> avz;
  py::array_t<double> avt;

  if (has_vertex) {
    avx = py::cast<py::array_t<double>>(vx);
    avy = py::cast<py::array_t<double>>(vy);
    avz = py::cast<py::array_t<double>>(vz);
    avt = py::cast<py::array_t<double>>(vt);

    if (avx.request().ndim != 1 || avy.request().ndim != 1 || avz.request().ndim != 1 ||
        avt.request().ndim != 1)
      throw std::runtime_error("vx, vy, vz, vt must be 1D");
  }

  auto x = avx.unchecked<1>();
  auto y = avy.unchecked<1>();
  auto z = avz.unchecked<1>();
  auto t = avt.unchecked<1>();

  if (has_vertex &&
      (x.shape(0) != n || y.shape(0) != n || z.shape(0) != n || t.shape(0) != n))
    throw std::runtime_error("vx, vy, vz, vt must have same length");

  for (const auto& vi : vmap) {

    int m1 = vi.first.first;
    int m2 = vi.first.second;

    // there must be at least one parent or child when we arrive here...
    normalize(m1, m2, fortran);

    if (m1 < 0 || m2 > n) {
      std::ostringstream os;
      os << "invalid " << (parents ? "parents" : "children") << " range for vertex "
         << event.vertices().size() << " [" << m1 << ", " << m2
         << ") total number of particles " << n;
      throw std::runtime_error(os.str().c_str());
    }

    // ...with at least one child or parent
    const auto& co = vi.second;

    if (co.empty()) {
      std::ostringstream os;
      os << "invalid empty " << (!parents ? "parents" : "children")
         << " list for vertex " << event.vertices().size();
      throw std::runtime_error(os.str().c_str());
    }
    FourVector pos;
    if (has_vertex) {
      // we assume this is a production vertex
      // if parent, co.front() is location of production vertex of first child
      // if child, we use location of first child m1
      const int i = parents ? co.front() : m1;
      pos.set(x(i), y(i), z(i), t(i));
    }

    GenVertexPtr v{new GenVertex(pos)};
    int vid = event.vertices().size();

    if (parents) {
      for (int k = m1; k < m2; ++k) modded_add_particle_in(vid, v, particles.at(k));
      for (const auto k : co) v->add_particle_out(particles.at(k));
    } else {
      for (int k = m1; k < m2; ++k) v->add_particle_out(particles.at(k));
      for (const auto k : co) modded_add_particle_in(vid, v, particles.at(k));
    }

    event.add_vertex(v);
  }
}

void from_hepevt(GenEvent& event, int event_number, py::array_t<double> px,
                 py::array_t<double> py, py::array_t<double> pz, py::array_t<double> en,
                 py::array_t<double> m, py::array_t<int> pid, py::array_t<int> status,
                 py::object parents, py::object children, py::object vx, py::object vy,
                 py::object vz, py::object vt, bool fortran) {
  if (px.request().ndim != 1) throw std::runtime_error("px must be 1D");
  if (py.request().ndim != 1) throw std::runtime_error("py must be 1D");
  if (pz.request().ndim != 1) throw std::runtime_error("pz must be 1D");
  if (en.request().ndim != 1) throw std::runtime_error("en must be 1D");
  if (m.request().ndim != 1) throw std::runtime_error("m must be 1D");
  if (pid.request().ndim != 1) throw std::runtime_error("pid must be 1D");
  if (status.request().ndim != 1) throw std::runtime_error("status must be 1D");

  auto rpx = px.unchecked<1>();
  auto rpy = py.unchecked<1>();
  auto rpz = pz.unchecked<1>();
  auto ren = en.unchecked<1>();
  auto rm = m.unchecked<1>();
  auto rpid = pid.unchecked<1>();
  auto rsta = status.unchecked<1>();

  const int n = pid.shape(0);
  if (rpx.shape(0) != n || rpy.shape(0) != n || rpz.shape(0) != n ||
      ren.shape(0) != n || rm.shape(0) != n)
    throw std::runtime_error("px, py, pz, en, m, pid, status must have same length");

  event.clear();
  event.reserve(n);
  event.set_event_number(event_number);

  for (int i = 0; i < n; ++i) {
    GenParticlePtr p{
        new GenParticle(FourVector(rpx(i), rpy(i), rpz(i), ren(i)), rpid(i), rsta(i))};
    p->set_generated_mass(rm(i));
    event.add_particle(p);
  }

  const bool have_parents = !parents.is_none();
  const bool have_children = !children.is_none();
  if (have_parents || have_children)
    connect_parents_and_children(
        event, have_parents,
        py::cast<py::array_t<int>>(have_parents ? parents : children), vx, vy, vz, vt,
        fortran);
}

} // namespace HepMC3
