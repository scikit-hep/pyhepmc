// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
/**
 *  @file ReaderRoot.cc
 *  @brief Implementation of \b class ReaderRoot
 *
 */
#include "HepMC/ReaderRoot.h"

namespace HepMC {

ReaderRoot::ReaderRoot(const std::string &filename):
m_file(filename.c_str()),
m_next(m_file.GetListOfKeys()) {

    if ( !m_file.IsOpen() ) {
        ERROR( "ReaderRoot: problem opening file: " << filename )
        return;
    }

    shared_ptr<GenRunInfo> ri = make_shared<GenRunInfo>();

    GenRunInfoData *run = (GenRunInfoData*)m_file.Get("GenRunInfoData");
    
    if(run) {
        ri->read_data(*run);
        delete run;
    }

    set_run_info(ri);
}

bool ReaderRoot::read_event(GenEvent& evt) {

    // Skip object of different type than GenEventData
    GenEventData *data = NULL;

    while(true) {
        TKey *key = (TKey*)m_next();

        if( !key ) {
            m_file.Close();
            return false;
        }

        const char *cl = key->GetClassName();

        if( !cl ) continue;
        
        if( strncmp(cl,"HepMC::GenEventData",19) == 0 ) {
            data = (GenEventData*)key->ReadObj();
            break;
        }
    }

    if( !data ) {
        ERROR("ReaderRoot: could not read event from root file")
        m_file.Close();
        return false;
    }

    evt.read_data(*data);
    evt.set_run_info( run_info() );

    delete data;
    return true;
}

void ReaderRoot::close() {
    m_file.Close();
}

bool ReaderRoot::failed() {
    if ( !m_file.IsOpen() ) return true;

    return false;
}

} // namespace HepMC
