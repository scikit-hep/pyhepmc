// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef ROOT_TOOL2_H
#define ROOT_TOOL2_H

#ifndef HEPMC2
#include "HepMC/GenEvent.h"
#include "HepMC/Data/GenEventData.h"
#include "RootTool2_serialized_class.h"
#include "ValidationTool.h"
#include "Timer.h"

#include "TFile.h"
#include "TSystem.h"
#include "TKey.h"
#include "TString.h"

class RootTool2 : public ValidationTool {
public:
    RootTool2(const std::string &filename, std::ios::openmode mode);

    ~RootTool2();

public:
    const std::string name() {
        if(m_mode == std::ios::in) return "ROOT STREAMER input file";
        else                       return "ROOT STREAMER output file";
    }

    const std::string long_name() { return name() + ": " + m_filename; }

    bool tool_modifies_event() {
        return (m_mode == std::ios::in) ? true : false;
    }

    Timer* timer() { return &m_timer; }

    void initialize();
    int  process(GenEvent &hepmc);
    void finalize();

    bool failed();

private:
    RootTool2_serialized_class *m_class;
    TFile             *m_file;
    TIter             *m_next;
    TKey              *m_key;
    std::ios::openmode m_mode;
    std::string        m_filename;
    int                m_counter;
    Timer              m_timer;
};

#endif // ifndef HEPMC2
#endif
