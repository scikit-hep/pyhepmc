// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#include "RootTool2.h"

#ifndef HEPMC2

RootTool2::RootTool2(const std::string &filename, std::ios::openmode mode):m_file(NULL),m_timer("ROOT STREAMER event writing time") {

    m_filename = filename;
    m_mode     = mode;

    if( mode == std::ios::in ) {
        m_file = new TFile(filename.c_str());
        m_timer = Timer("ROOT STREAMER event parsing time");
    }
    else m_file = new TFile(filename.c_str(),"RECREATE");

    m_next     = new TIter(m_file->GetListOfKeys());
    m_key      = NULL;
    m_counter  = 0;

}

RootTool2::~RootTool2() {
    if(m_next)  delete m_next;
    if(m_file)  delete m_file;
}

void RootTool2::initialize() {}

int RootTool2::process(GenEvent &hepmc) {
    if( m_mode == std::ios::in ) {
        m_key = (TKey*)(*m_next)();
        if( !m_key ) return -1;

        TString classname = "RootTool2_serialized_class";

        m_file->GetObject(m_key->GetName(), m_class);
        if(!m_class) return -1;
        if(!m_class->GetEvent()) return -1;

        GenEventData data;
        m_class->GetEvent()->write_data(data);
        hepmc.read_data(data);

        delete m_class->GetEvent();
        delete m_class;
        m_class = NULL;

        if( failed() ) return -1;
    }
    else {
        m_class = new RootTool2_serialized_class();

        m_class->SetEvent(&hepmc);

        TString name = "Event_";
        name += (++m_counter);

        m_file->WriteObject(m_class, name.Data());

        delete m_class;

        if( failed() ) return -1;
    }

    return 0;
}

void RootTool2::finalize() {
    if(m_file) m_file->Close();
}

bool RootTool2::failed() {
    if(m_file) return !(m_file->IsOpen());

    return true;
}

#endif // ifndef HEPMC2
