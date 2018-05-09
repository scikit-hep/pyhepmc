// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_READERROOT_H
#define  HEPMC_READERROOT_H
/**
 *  @file  ReaderRoot.h
 *  @brief Definition of \b class ReaderRoot
 *
 *  @class HepMC::ReaderRoot
 *  @brief GenEvent I/O parsing and serialization for root files
 *
 *  If HepMC was compiled with path to ROOT available, this class can be used
 *  for root file I/O in the same manner as with HepMC::ReaderAscii class.
 *
 *  @ingroup IO
 *
 */
#include "HepMC/Reader.h"
#include "HepMC/GenEvent.h"
#include "HepMC/Data/GenEventData.h"
#include "HepMC/Data/GenRunInfoData.h"

// ROOT header files
#include "TFile.h"
#include "TKey.h"

namespace HepMC {

  class ReaderRoot : public Reader {
//
// Constructors
//
public:
    /** @brief Default constructor */
    ReaderRoot(const std::string &filename);

//
// Functions
//
public:

    /** @brief Read event from file
     *
     *  @param[out] evt Contains parsed event
     */
    bool read_event(GenEvent &evt);

    /** @brief Close file stream */
    void close();

    /** @brief Get stream error state */
    bool failed();
//
// Fields
//
private:
    TFile m_file; //!< File handler
    TIter m_next; //!< Iterator for event reading
};

} // namespace HepMC

#endif
