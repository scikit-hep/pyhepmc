#include "repr.hpp"
#include <HepMC3/Attribute.h>
#include <HepMC3/FourVector.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/GenVertex.h>
#include <ostream>

std::ostream& repr_ostream(std::ostream& os, const std::string& s) {
  os << "'" << s << "'";
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::Attribute& a) {
  std::string s;
  a.to_string(s);
  os << s;
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenRunInfo::ToolInfo& x) {
  os << "ToolInfo(name=";
  repr_ostream(os, x.name) << ", version=";
  repr_ostream(os, x.version) << ", description=";
  repr_ostream(os, x.description) << ")";
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::FourVector& x) {
  const int saved = os.precision();
  os.precision(3);
  os << "FourVector(" << x.x() << ", " << x.y() << ", " << x.z() << ", " << x.t()
     << ")";
  os.precision(saved);
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenRunInfo& x) {
  os << "GenRunInfo(tools=";
  repr_ostream(os, x.tools()) << ", weight_names=";
  repr_ostream(os, x.weight_names()) << ", attributes=";
  repr_ostream(os, x.attributes()) << ")";
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenParticle& x) {
  os << "GenParticle(";
  repr_ostream(os, x.momentum());
  if (x.is_generated_mass_set()) os << ", mass=" << x.data().mass;
  os << ", pid=" << x.pid() << ", status=" << x.status() << ")";
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenVertex& x) {
  os << "GenVertex(";
  repr_ostream(os, x.position());
  os << ")";
  return os;
}

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenEvent& x) {
  // incomplete:
  // missing comparison of GenHeavyIon, GenPdfInfo, GenCrossSection

  os << "GenEvent("
     << "momentum_unit=" << x.momentum_unit() << ", "
     << "length_unit=" << x.length_unit() << ", "
     << "event_number=" << x.event_number() << ", "
     << "particles=";
  repr_ostream(os, x.particles()) << ", vertices=";
  repr_ostream(os, x.vertices()) << ", run_info=";
  repr_ostream(os, x.run_info()) << ")";
  return os;
}
