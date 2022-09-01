#ifndef PYHEPMC_POINTER_HPP
#define PYHEPMC_POINTER_HPP

#include "HepMC3/GenRunInfo.h"
#include <memory>

namespace HepMC3 {
class Attribute;
class HEPEUPAttribute;
class HEPRUPAttribute;
class GenRunInfo;
class GenEvent;

using GenEventPtr = std::shared_ptr<GenEvent>;
using AttributePtr = std::shared_ptr<Attribute>;
using HEPEUPAttributePtr = std::shared_ptr<HEPEUPAttribute>;
using HEPRUPAttributePtr = std::shared_ptr<HEPRUPAttribute>;
using GenRunInfoPtr = std::shared_ptr<GenRunInfo>;
using AttributePtr = std::shared_ptr<Attribute>;
} // namespace HepMC3

#endif
