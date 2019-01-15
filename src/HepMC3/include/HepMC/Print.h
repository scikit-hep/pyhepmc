// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2015 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_PRINT_H
#define  HEPMC_PRINT_H
///
/// @file Print.h
/// @brief Definition of static \b class Print
///

#include "HepMC/GenEvent.h"
#include "HepMC/GenVertex.h"
#include "HepMC/GenParticle.h"

namespace HepMC {


class GenPdfInfo;
class GenHeavyIon;
class GenCrossSection;


/// @brief Provides different printing formats
/// @todo This class has no state -- why isn't it just a namespace with free functions?
class Print {
public:
    /// @brief Print content of all GenEvent containers
    static void content(std::ostream& os, const GenEvent &event);
    inline static void content(const GenEvent &event) { content(std::cout, event); }

    /// @brief Print event in listing (HepMC2) format
    static void listing(std::ostream& os, const GenEvent &event, unsigned short precision = 2);
    inline static void listing(const GenEvent &event, unsigned short precision = 2) {
      listing(std::cout, event, precision);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, const GenEvent &event, bool attributes=false);
    inline static void line(const GenEvent &event, bool attributes=false) {
      line(std::cout, event, attributes);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, const GenVertexPtr &v, bool attributes=false);
    inline static void line(const GenVertexPtr &v, bool attributes=false) {
      line(std::cout, v, attributes);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, const GenParticlePtr &p, bool attributes=false);
    inline static void line(const GenParticlePtr &p, bool attributes=false) {
      line(std::cout, p, attributes);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, shared_ptr<GenCrossSection> &cs);
    inline static void line(shared_ptr<GenCrossSection> &cs) {
      line(std::cout, cs);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, shared_ptr<GenHeavyIon> &hi);
    inline static void line(shared_ptr<GenHeavyIon> &hi) {
      line(std::cout, hi);
    }

    /// @brief Print one-line info
    static void line(std::ostream& os, shared_ptr<GenPdfInfo> &pi);
    inline static void line(shared_ptr<GenPdfInfo> &pi) {
      line(std::cout, pi);
    }

private:
    /// @brief Helper function for printing a vertex in listing format
    static void listing(std::ostream& os, const GenVertexPtr &v);

    /// @brief Helper function for printing a particle in listing format
    static void listing(std::ostream& os, const GenParticlePtr &p);

    virtual ~Print() {}
};


} // namespace HepMC

#endif
