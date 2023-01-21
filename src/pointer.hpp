#ifndef PYHEPMC_POINTER_HPP
#define PYHEPMC_POINTER_HPP

#include "HepMC3/AssociatedParticle.h"
#include "HepMC3/GenRunInfo.h"
#include <memory>

namespace HepMC3 {
class Attribute;
class HEPEUPAttribute;
class HEPRUPAttribute;
class GenRunInfo;
class GenEvent;
class AssociatedParticle;
class GenParticle;
class GenVertex;

using GenEventPtr = std::shared_ptr<GenEvent>;
using AttributePtr = std::shared_ptr<Attribute>;
using HEPEUPAttributePtr = std::shared_ptr<HEPEUPAttribute>;
using HEPRUPAttributePtr = std::shared_ptr<HEPRUPAttribute>;
using GenRunInfoPtr = std::shared_ptr<GenRunInfo>;
using AssociatedParticlePtr = std::shared_ptr<AssociatedParticle>;
using ConstGenParticlePtr = std::shared_ptr<const GenParticle>;
using ConstGenVertexPtr = std::shared_ptr<const GenVertex>;
} // namespace HepMC3

#endif
