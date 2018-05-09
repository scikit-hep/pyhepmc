// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#include "FileValidationTool.h"

FileValidationTool::FileValidationTool(const std::string &filename, std::ios::openmode mode):m_file_in(NULL),m_file_out(NULL),m_timer("HepMC event writing time") {

    m_filename = filename;

    if(mode == std::ios::in) {
        HEPMC2CODE( m_file_in = new IO_GenEvent(m_filename, mode); )
        HEPMC3CODE( m_file_in = new ReaderAsciiHepMC2(m_filename); )

        m_timer = Timer("HepMC event parsing time");
    }
    else {
        HEPMC2CODE(
            m_filename += "2";
            m_file_out = new IO_GenEvent(m_filename, mode);
        )
        HEPMC3CODE(
            m_filename += "3";
            m_file_out = new WriterAscii(m_filename);
        )
    }
}

FileValidationTool::~FileValidationTool() {
    if(m_file_in)  delete m_file_in;
    if(m_file_out) delete m_file_out;
}

void FileValidationTool::initialize() {}

int FileValidationTool::process(GenEvent &hepmc) {
    if(m_file_in) {
        HEPMC2CODE(
            m_file_in->fill_next_event(&hepmc);
            if( m_file_in->rdstate() ) return -1;
        )
        HEPMC3CODE(
            m_file_in->read_event(hepmc);
            if( m_file_in->failed() ) return -1;
        )
        
    }
    else if(m_file_out) {
        HEPMC2CODE(
            m_file_out->write_event(&hepmc);
            if( m_file_out->rdstate() ) return -1;
        )
        HEPMC3CODE(
            m_file_out->write_event( hepmc);
            if( m_file_out->failed() ) return -1;
        )
    }

    return 0;
}

void FileValidationTool::finalize() {
    HEPMC3CODE(
        if(m_file_in)  m_file_in->close();
        if(m_file_out) m_file_out->close();
    )
}

bool FileValidationTool::failed() {
    HEPMC2CODE(
        if(m_file_in)  return m_file_in->rdstate();
        if(m_file_out) return m_file_out->rdstate();
    )
    HEPMC3CODE(
        if(m_file_in)  return m_file_in->failed();
        if(m_file_out) return m_file_out->failed();
    )
    return true;
}
