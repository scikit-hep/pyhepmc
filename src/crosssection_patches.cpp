#include "pybind.hpp"
#include <HepMC3/GenCrossSection.h>
#include <HepMC3/GenEvent.h>
#include <accessor/accessor.hpp>
#include <cassert>
#include <vector>

// To resize cross-section vectors, we use the legal crowbar
// to access the private attribute map of GenCrossSection
MEMBER_ACCESSOR(CS1, HepMC3::GenCrossSection, cross_sections, std::vector<double>)
MEMBER_ACCESSOR(CS2, HepMC3::GenCrossSection, cross_section_errors, std::vector<double>)

namespace HepMC3 {

void crosssection_maybe_increase_vector(GenCrossSection& cs, unsigned size) {
  auto cs1 = accessor::accessMember<CS1>(cs);
  auto cs2 = accessor::accessMember<CS2>(cs);
  assert(cs1.get().size() == cs2.get().size());
  if (size > cs1.get().size()) {
    cs1.get().resize(size, 0);
    cs2.get().resize(size, 0);
  }
}

int crosssection_safe_index(GenCrossSection& cs, py::object obj) {
  auto idx = py::cast<int>(obj);
  const auto size =
      cs.event() ? (std::max)(cs.event()->weights().size(), static_cast<std::size_t>(1))
                 : 1u;
  if (idx < 0) idx += size;
  if (idx < 0 || static_cast<unsigned>(idx) >= size) throw py::index_error();
  crosssection_maybe_increase_vector(cs, size);
  return idx;
}

std::string crosssection_safe_name(GenCrossSection& cs, py::object obj) {
  auto name = py::cast<std::string>(obj);
  if (cs.event() && cs.event()->run_info()) {
    const auto size =
        (std::max)(cs.event()->weights().size(), static_cast<std::size_t>(1));
    crosssection_maybe_increase_vector(cs, size);
    const auto& wnames = cs.event()->run_info()->weight_names();
    if (std::find(wnames.begin(), wnames.end(), name) != wnames.end()) return name;
  }
  throw py::key_error(name);
  return {};
}

} // namespace HepMC3
