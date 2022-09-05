#ifndef PYHEPMC_REPR_HPP
#define PYHEPMC_REPR_HPP

#include "UnparsedAttribute.hpp"
#include <HepMC3/Attribute.h>
#include <HepMC3/FourVector.h>
#include <HepMC3/GenCrossSection.h>
#include <HepMC3/GenEvent.h>
#include <HepMC3/GenHeavyIon.h>
#include <HepMC3/GenParticle.h>
#include <HepMC3/GenPdfInfo.h>
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/GenVertex.h>
#include <HepMC3/LHEFAttributes.h>
#include <map>
#include <memory>
#include <ostream>
#include <string>

std::ostream& repr_ostream(std::ostream& os, const std::string& s);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::Attribute& a);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenRunInfo& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenPdfInfo& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenRunInfo::ToolInfo& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::FourVector& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenParticle& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenVertex& x);
std::ostream& repr_ostream(std::ostream& os, const HepMC3::GenEvent& x);

std::ostream& repr_ostream(std::ostream& os, const HepMC3::UnparsedAttribute& a);

template <class Iterator, class Streamer>
std::ostream& ostream_range(std::ostream& os, Iterator begin, Iterator end,
                            Streamer streamer, const char bracket_left = '[',
                            const char bracket_right = ']') {
  os << bracket_left;
  bool first = true;
  for (; begin != end; ++begin) {
    if (first) {
      first = false;
    } else {
      os << ", ";
    }
    streamer(os, begin);
  }
  os << bracket_right;
  return os;
}

template <class T>
std::ostream& repr_ostream(std::ostream& os, const std::shared_ptr<T>& x) {
  if (x)
    repr_ostream(os, *x.get());
  else
    os << "None";
  return os;
}

template <class T, class A>
std::ostream& repr_ostream(std::ostream& os, const std::vector<T, A>& v) {
  return ostream_range(
      os, v.begin(), v.end(),
      [](std::ostream& os, typename std::vector<T, A>::const_iterator it) {
        repr_ostream(os, *it);
      });
}

template <class K, class V, class... Ts>
std::ostream& repr_ostream(std::ostream& os, const std::map<K, V, Ts...>& m) {
  return ostream_range(
      os, m.begin(), m.end(),
      [](std::ostream& os, typename std::map<K, V, Ts...>::const_iterator it) {
        os << it->first << ": ";
        repr_ostream(os, it->second);
      },
      '{', '}');
}

template <class T>
py::str repr(const T& t) {
  std::ostringstream os;
  repr_ostream(os, t);
  return py::cast(os.str());
}

#endif
