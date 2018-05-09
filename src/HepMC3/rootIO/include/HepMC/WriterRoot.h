// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_WRITERROOT_H
#define  HEPMC_WRITERROOT_H
/**
 *  @file  WriterRoot.h
 *  @brief Definition of \b class WriterRoot
 *
 *  @class HepMC::WriterRoot
 *  @brief GenEvent I/O serialization for root files
 *
 *  If HepMC was compiled with path to ROOT available, this class can be used
 *  for root writing in the same manner as with HepMC::WriterAscii class.
 *
 *  @ingroup IO
 *
 */
#include "HepMC/Writer.h"
#include "HepMC/GenEvent.h"
#include "HepMC/Data/GenEventData.h"
#include "HepMC/Data/GenRunInfoData.h"

// ROOT header files
#include "TFile.h"

namespace HepMC {

  class WriterRoot : public Writer {
//
// Constructors
//
public:
    /** @brief Default constructor
     *  @warning If file exists, it will be overwritten
     */
    WriterRoot(const std::string& filename,
               shared_ptr<GenRunInfo> run = shared_ptr<GenRunInfo>());

//
// Functions
//
public:

    /** @brief Write event to file
     *
     *  @param[in] evt Event to be serialized
     */
    void write_event(const GenEvent &evt);

    /** @brief Write the GenRunInfo object to file. */
    void write_run_info();

    /** @brief Close file stream */
    void close();

    /** @brief Get stream error state flag */
    bool failed();
//
// Fields
//
private:
    TFile m_file;         //!< File handler
    int   m_events_count; //!< Events count. Needed to generate unique object name
};

} // namespace HepMC

#endif
