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
    m_file(filename.c_str()),m_tree(0),m_events_count(0),m_tree_name("hepmc3_tree"),m_branch_name("hepmc3_event")
{
    if (!init()) return;
}


ReaderRootTree::ReaderRootTree(const std::string &filename,const std::string &treename,const std::string &branchname):
    m_file(filename.c_str()),m_tree(0),m_events_count(0),m_tree_name(treename.c_str()),m_branch_name(branchname.c_str())
{
    if (!init()) return;
}

bool ReaderRootTree::init()
{
    if ( !m_file.IsOpen() )
        {
            ERROR( "ReaderRootTree: problem opening file: " << m_file.GetName() )
            return false;
        }
    shared_ptr<GenRunInfo> ri = make_shared<GenRunInfo>();

    GenRunInfoData *run = (GenRunInfoData*)m_file.Get("GenRunInfoData");
    
    if(run) {
        ri->read_data(*run);
        delete run;
    }

    set_run_info(ri);        
        
        
        
    m_tree=(TTree*)m_file.Get(m_tree_name.c_str());
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

    m_tree->GetEntry(m_events_count);
    evt.read_data(*m_event_data);

    m_events_count++;
    return true;
}

void ReaderRootTree::close()
{
    m_file.Close();
}

bool ReaderRootTree::failed()
{
    if ( !m_file.IsOpen() ) return true;
    if (m_events_count>m_tree->GetEntries()) return true;
    return false;
}

} // namespace HepMC
