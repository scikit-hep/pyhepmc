// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_READERROOTTREE_H
#define  HEPMC_READERROOTTREE_H
/**
 *  @file  ReaderRootTree.h
 *  @brief Definition of \b class ReaderRootTree
 *
 *  @class HepMC::ReaderRootTreeTree
 *  @brief GenEvent I/O parsing and serialization for root files  based on root TTree
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
#include "TTree.h"
#include "TBranch.h"

namespace HepMC
{

class ReaderRootTree : public Reader
{
//
// Constructors
//
public:
    /** @brief Default constructor */
    ReaderRootTree(const std::string &filename);
    /** @brief Constructor with tree name*/
    ReaderRootTree(const std::string &filename,const std::string &treename,const std::string &branchname);

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

private:
    /** @brief init routine */
    bool init();
//
// Fields
//
private:
    TFile m_file;         //!< File handler
public:
    TTree* m_tree;//!< Tree handler. Public to allow simple access, e.g. custom branches.
private:
    int   m_events_count; //!< Events count. Needed to read the tree
    GenEventData* m_event_data;
    std::string m_tree_name;
    std::string m_branch_name;
};

} // namespace HepMC

#endif
