// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef FILE_VALIDTAION_TOOL_H
#define FILE_VALIDTAION_TOOL_H

#ifdef HEPMC2
#include "HepMC/IO_GenEvent.h"
#else
#include "HepMC/WriterAscii.h"
#include "HepMC/ReaderAsciiHepMC2.h"
#endif // ifdef HEPMC2

#include "ValidationTool.h"
#include "Timer.h"

class FileValidationTool : public ValidationTool {
public:
    FileValidationTool(const std::string &filename, std::ios::openmode mode);

    ~FileValidationTool();

public:
    const std::string name() {
        if(m_file_in) return "input file";
        else          return "output file";
    }

    const std::string long_name() { return name() + ": " + m_filename; }

    bool   tool_modifies_event() { return (m_file_in) ? true : false; }
    Timer* timer()               { return &m_timer; }

    void initialize();
    int  process(GenEvent &hepmc);
    void finalize();

    bool failed();

private:
    HEPMC2CODE(
        IO_GenEvent *m_file_in;
        IO_GenEvent *m_file_out;
    )
    HEPMC3CODE(
        ReaderAsciiHepMC2 *m_file_in;
        WriterAscii       *m_file_out;
    )

    std::string  m_filename;
    Timer        m_timer;
};

#endif
