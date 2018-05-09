// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef ROOT_TOOL_H
#define ROOT_TOOL_H

#ifndef HEPMC2
#include "HepMC/ReaderRoot.h"
#include "HepMC/WriterRoot.h"
#include "ValidationTool.h"
#include "Timer.h"

class RootTool : public ValidationTool {
public:
    RootTool(const std::string &filename, std::ios::openmode mode);

    ~RootTool();

public:
    const std::string name() {
        if(m_file_in) return "ROOT READER input file";
        else          return "ROOT WRTITER output file";
    }

    const std::string long_name() { return name() + ": " + m_filename; }

    bool tool_modifies_event()    { return (m_file_in) ? true : false; }

    Timer* timer()                { return &m_timer; }

    void initialize();
    int  process(GenEvent &hepmc);
    void finalize();

    bool failed();

private:
    ReaderRoot *m_file_in;
    WriterRoot *m_file_out;
    std::string  m_filename;
    Timer        m_timer;
};

#endif // ifndef HEPMC2
#endif
