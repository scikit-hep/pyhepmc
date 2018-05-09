// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_WRITERROOTTREE_H
#define  HEPMC_WRITERROOTTREE_H
/**
 *  @file  WriterRootTree.h
 *  @brief Definition of \b class WriterRootTree
 *
 *  @class HepMC::WriterRootTree
 *  @brief GenEvent I/O serialization for root files based on root TTree
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
#include "TTree.h"

namespace HepMC
{
class WriterRootTree : public Writer
{
//
// Constructors
//
public:
    /** @brief Default constructor
     *  @warning If file exists, it will be overwritten
     */
    WriterRootTree(const std::string &filename,
               shared_ptr<GenRunInfo> run = shared_ptr<GenRunInfo>());
    /** @brief Constructor with tree name*/
    WriterRootTree(const std::string &filename,const std::string &treename,const std::string &branchname,
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

private:
    /** @brief init routine */
    bool init(shared_ptr<GenRunInfo> run);
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
