#include "HepMC3/GenPdfInfo.h"
#include "HepMC3/LHEFAttributes.h"
#include "pointer.hpp"
#include <HepMC3/Data/GenEventData.h>
#include <HepMC3/Data/GenParticleData.h>
#include <HepMC3/Data/GenVertexData.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenHeavyIon.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/GenVertex.h>

namespace HepMC3 {

template <class T>
bool operator!=(const T& a, const T& b) {
  return !operator==(a, b);
}

template <class T>
bool operator==(const std::vector<T>& a, const std::vector<T>& b) {
  return std::equal(a.begin(), a.end(), b.begin(), b.end());
}

// equality comparions used by unit tests
bool is_close(const FourVector& a, const FourVector& b, double rel_eps = 1e-7) {
  auto is_close = [rel_eps](double a, double b) { return std::abs(a - b) < rel_eps; };
  return is_close(a.x(), b.x()) && is_close(a.y(), b.y()) && is_close(a.z(), b.z()) &&
         is_close(a.t(), b.t());
}

// compares all real qualities of two particles, but ignores the .id() field
bool operator==(const GenParticle& a, const GenParticle& b) {
  return a.pid() == b.pid() && a.status() == b.status() &&
         is_close(a.momentum(), b.momentum());
}

// compares all real qualities of both particle sets,
// but ignores the .id() fields and the particle order
bool equal_particle_sets(const std::vector<ConstGenParticlePtr>& a,
                         const std::vector<ConstGenParticlePtr>& b) {
  if (a.size() != b.size()) return false;
  auto unmatched = b;
  for (auto&& ai : a) {
    auto it = std::find_if(unmatched.begin(), unmatched.end(),
                           [ai](ConstGenParticlePtr x) { return *ai == *x; });
    if (it == unmatched.end()) return false;
    unmatched.erase(it);
  }
  return unmatched.empty();
}

// compares all real qualities of two vertices, but ignores the .id() field
bool operator==(const GenVertex& a, const GenVertex& b) {
  return a.status() == b.status() && is_close(a.position(), b.position()) &&
         equal_particle_sets(a.particles_in(), b.particles_in()) &&
         equal_particle_sets(a.particles_out(), b.particles_out());
}

// compares all real qualities of both vertex sets,
// but ignores the .id() fields and the vertex order
bool equal_vertex_sets(const std::vector<ConstGenVertexPtr>& a,
                       const std::vector<ConstGenVertexPtr>& b) {
  if (a.size() != b.size()) return false;
  auto unmatched = b;
  for (auto&& ai : a) {
    auto it = std::find_if(unmatched.begin(), unmatched.end(),
                           [ai](ConstGenVertexPtr x) { return *ai == *x; });
    if (it == unmatched.end()) return false;
    unmatched.erase(it);
  }
  return unmatched.empty();
}

bool operator==(const GenRunInfo::ToolInfo& a, const GenRunInfo::ToolInfo& b) {
  return a.name == b.name && a.version == b.version && a.description == b.description;
}

bool operator==(const GenRunInfo& a, const GenRunInfo& b) {
  const auto a_attr = a.attributes();
  const auto b_attr = b.attributes();
  return a.tools().size() == b.tools().size() &&
         a.weight_names().size() == b.weight_names().size() &&
         a_attr.size() == b_attr.size() && a.tools() == b.tools() &&
         a.weight_names() == b.weight_names() &&
         std::equal(a_attr.begin(), a_attr.end(), b_attr.begin(),
                    [](const std::pair<std::string, AttributePtr>& a,
                       const std::pair<std::string, AttributePtr>& b) {
                      if (a.first != b.first) return false;
                      if (bool(a.second) != bool(b.second)) return false;
                      if (!a.second) return true;
                      std::string sa, sb;
                      a.second->to_string(sa);
                      b.second->to_string(sb);
                      return sa == sb;
                    });
}

bool operator==(const GenHeavyIon& a, const GenHeavyIon& b) {
  std::string as, bs;
  a.to_string(as);
  b.to_string(bs);
  return as == bs;
}

bool operator==(const GenPdfInfo& a, const GenPdfInfo& b) {
  std::string as, bs;
  a.to_string(as);
  b.to_string(bs);
  return as == bs;
}

bool operator==(const GenCrossSection& a, const GenCrossSection& b) {
  std::string as, bs;
  a.to_string(as);
  b.to_string(bs);
  return as == bs;
}

bool operator==(const HEPRUPAttribute& a, const HEPRUPAttribute& b) {
  std::string as, bs;
  a.to_string(as);
  b.to_string(bs);
  return as == bs;
}

bool operator==(const HEPEUPAttribute& a, const HEPEUPAttribute& b) {
  std::string as, bs;
  a.to_string(as);
  b.to_string(bs);
  return as == bs;
}

bool operator==(const GenEvent& a, const GenEvent& b) {
  // incomplete:
  // missing comparison of GenHeavyIon, GenPdfInfo, GenCrossSection

  if (a.event_number() != b.event_number() || a.momentum_unit() != b.momentum_unit() ||
      a.length_unit() != b.length_unit())
    return false;

  // run_info may be missing
  if (a.run_info() && b.run_info()) {
    if (!(*a.run_info() == *b.run_info())) return false;
  } else if (!a.run_info() && b.run_info()) {
    if (*b.run_info() != GenRunInfo()) return false;
  } else if (a.run_info() && !b.run_info()) {
    if (*a.run_info() != GenRunInfo()) return false;
  }

  // if all vertices compare equal, then also all particles are equal
  return equal_vertex_sets(a.vertices(), b.vertices());
}

bool operator==(const GenParticleData& a, const GenParticleData& b) {
  return a.pid == b.pid && a.status == b.status && a.is_mass_set == b.is_mass_set &&
         a.mass == b.mass && a.momentum == b.momentum;
}

bool operator==(const GenVertexData& a, const GenVertexData& b) {
  return a.status == b.status && a.position == b.position;
}

bool operator==(const GenEventData& a, const GenEventData& b) {
  return a.event_number == b.event_number && a.momentum_unit == b.momentum_unit &&
         a.length_unit == b.length_unit && a.particles == b.particles &&
         a.vertices == b.vertices && a.weights == b.weights &&
         a.event_pos == b.event_pos && a.links1 == b.links1 && a.links2 == b.links2 &&
         a.attribute_id == b.attribute_id && a.attribute_name == b.attribute_name &&
         a.attribute_string == b.attribute_string;
}

} // namespace HepMC3
