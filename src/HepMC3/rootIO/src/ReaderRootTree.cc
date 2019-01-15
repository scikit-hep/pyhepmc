// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
/**
 *  @file ReaderRootTree.cc
 *  @brief Implementation of \b class ReaderRootTree
 *
 */
#include "HepMC/ReaderRootTree.h"
#include "HepMC/Units.h"

namespace HepMC
{

ReaderRootTree::ReaderRootTree(const std::string &filename):
    m_tree(0),m_events_count(0),m_tree_name("hepmc3_tree"),m_branch_name("hepmc3_event")
{
    m_file = TFile::Open(filename.c_str());
    if (!init()) return;
}


ReaderRootTree::ReaderRootTree(const std::string &filename,const std::string &treename,const std::string &branchname):
    m_tree(0),m_events_count(0),m_tree_name(treename.c_str()),m_branch_name(branchname.c_str())
{
    m_file = TFile::Open(filename.c_str());
    if (!init()) return;
}

bool ReaderRootTree::init()
{
    if ( !m_file->IsOpen() )
        {
            ERROR( "ReaderRootTree: problem opening file: " << m_file->GetName() )
            return false;
        }
   
        
    m_tree=reinterpret_cast<TTree*>(m_file->Get(m_tree_name.c_str()));
    if (!m_tree)
        {
            ERROR( "ReaderRootTree: problem opening tree:  " << m_tree_name)
            return false;
        }
    m_event_data=new GenEventData();
    int result=m_tree->SetBranchAddress(m_branch_name.c_str(),&m_event_data);
    if (result<0)
        {
            ERROR( "ReaderRootTree: problem reading branch tree:  " << m_tree_name)
            return false;
        }
 m_run_info_data= new GenRunInfoData();
    result=m_tree->SetBranchAddress("GenRunInfo",&m_run_info_data);
    if (result<0)
        {
            ERROR( "ReaderRootTree2: problem reading branch tree:  " << "GenRunInfo")
            return false;
        }
 set_run_info(make_shared<GenRunInfo>());
    return true;
}




bool ReaderRootTree::read_event(GenEvent& evt)
{
    if (m_events_count>m_tree->GetEntries()) return false;
    m_event_data->particles.clear();
    m_event_data->vertices.clear();
    m_event_data->links1.clear();
    m_event_data->links2.clear();
    m_event_data->attribute_id.clear();
    m_event_data->attribute_name.clear();
    m_event_data->attribute_string.clear();

    
    m_run_info_data->weight_names.clear();
    m_run_info_data->tool_name.clear();
    m_run_info_data->tool_version.clear();
    m_run_info_data->tool_description.clear();
    m_run_info_data->attribute_name.clear();
    m_run_info_data->attribute_string.clear();


    m_tree->GetEntry(m_events_count);
    evt.read_data(*m_event_data);
    run_info()->read_data(*m_run_info_data);
    evt.set_run_info(run_info());
    m_events_count++;
    return true;
}

void ReaderRootTree::close()
{
    m_file->Close();
}

bool ReaderRootTree::failed()
{
    if ( !m_file->IsOpen() ) return true;
    if (m_events_count>m_tree->GetEntries()) return true;
    return false;
}

} // namespace HepMC
