#include "repr.hpp"
#include "HepMC3/GenPdfInfo.h"
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

std::ostream& repr_ostream(std::ostream& os, const HepMC3::UnparsedAttribute& a) {
  os << "<UnparsedAttribute '" << a.parent_->unparsed_string() << "'>";
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

std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenPdfInfo& x) {
  os << "GenPdfInfo(";
  os << "parton_id1=" << x.parton_id[0] << ", parton_id2=" << x.parton_id[1]
     << ", x1=" << x.x[0] << ", x2=" << x.x[1] << ", scale=" << x.scale
     << ", xf1=" << x.xf[0] << ", xf2=" << x.xf[1] << ", pdf_id1=" << x.pdf_id[0]
     << ", pdf_id2=" << x.pdf_id[1] << ")";
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

  os << "<GenEvent "
     << "momentum_unit=" << x.momentum_unit() << ", "
     << "length_unit=" << x.length_unit() << ", "
     << "event_number=" << x.event_number() << ", "
     << "particles=" << x.particles().size() << ", "
     << "vertices=" << x.vertices().size() << ", "
     << "run_info=";
  repr_ostream(os, x.run_info()) << ">";
  return os;
}
