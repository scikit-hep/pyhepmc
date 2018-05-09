// -*- C++ -*-
//
/**
 *  @file WriterRootTree.cc
 *  @brief Implementation of \b class WriterRootTree
 *
 */
#include "HepMC/WriterRootTree.h"
#include <cstdio>  // sprintf

namespace HepMC
{

WriterRootTree::WriterRootTree(const std::string &filename, shared_ptr<GenRunInfo> run):
    m_file(filename.c_str(),"RECREATE"),
    m_tree(0),    
    m_events_count(0),
    m_tree_name("hepmc3_tree"),
    m_branch_name("hepmc3_event")
{
    if (!init(run)) return;
}

WriterRootTree::WriterRootTree(const std::string &filename,const std::string &treename,const std::string &branchname, shared_ptr<GenRunInfo> run):
    m_file(filename.c_str(),"RECREATE"),
    m_tree(0),    
    m_events_count(0),
    m_tree_name(treename.c_str()),
    m_branch_name(branchname.c_str())
{
    if (!init(run)) return;
}

bool WriterRootTree::init(shared_ptr<GenRunInfo> run )
{
    if ( !m_file.IsOpen() )
        {
            ERROR( "WriterRootTree: problem opening file: " <<m_file.GetName() )
            return false;
        }
    set_run_info(run);
    m_event_data= new GenEventData();
    m_tree= new TTree(m_tree_name.c_str(),"hepmc3_tree");
    m_tree->Branch(m_branch_name.c_str(), m_event_data);
    if ( run_info() ) write_run_info();
    return true;
}

void WriterRootTree::write_event(const GenEvent &evt)
{
    if ( !m_file.IsOpen() ) return;
    
        if ( !run_info() ) {
        set_run_info(evt.run_info());
        write_run_info();
    } else {
        if ( evt.run_info() && run_info() != evt.run_info() )
        WARNING( "WriterAscii::write_event: GenEvents contain "
                 "different GenRunInfo objects from - only the "
                 "first such object will be serialized." )
    }

    
    
    m_event_data->particles.clear();
    m_event_data->vertices.clear();
    m_event_data->links1.clear();
    m_event_data->links2.clear();
    m_event_data->attribute_id.clear();
    m_event_data->attribute_name.clear();
    m_event_data->attribute_string.clear();

    evt.write_data(*m_event_data);
    m_tree->Fill();
    ++m_events_count;
}


void WriterRootTree::write_run_info() {
    if ( !m_file.IsOpen() || !run_info() ) return;

    GenRunInfoData data;
    run_info()->write_data(data);

    int nbytes = m_file.WriteObject(&data,"GenRunInfoData");

    if( nbytes == 0 ) {
        ERROR( "WriterRootTree: error writing GenRunInfo")
        m_file.Close();
    }
}


void WriterRootTree::close()
{

    m_tree->Write();
    m_file.Close();
}

bool WriterRootTree::failed()
{
    if ( !m_file.IsOpen() ) return true;

    return false;
}

} // namespace HepMC
