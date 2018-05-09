// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef PYTHIA_VALIDATION_TOOL_H
#define PYTHIA_VALIDATION_TOOL_H

#ifdef PYTHIA8_HEPMC2
#include "HepMC/GenEvent.h"
#include "Pythia8/Pythia8ToHepMC.h"
#else
#include "HepMC/GenEvent.h"
#include "Pythia8/Pythia8ToHepMC3.h"
#endif // ifdef PYTHIA8_HEPMC2

#include "ValidationTool.h"
#include "Timer.h"

#include "Pythia8/Pythia.h"

class PythiaValidationTool : public ValidationTool {
public:
    PythiaValidationTool( const string &filename );

    const std::string name()      { return "pythia8"; }
    const std::string long_name() { return name() + " config file: " + m_filename; }

    bool   tool_modifies_event() { return true;      }
    Timer* timer()               { return &m_timer;  }

    void initialize();
    int  process(GenEvent &hepmc);
    void finalize();

private:
    Pythia8::Pythia m_pythia;
    std::string     m_filename;
    Timer           m_timer;
    HEPMC2CODE( HepMC::Pythia8ToHepMC   m_tohepmc; )
    HEPMC3CODE( HepMC::Pythia8ToHepMC3 m_tohepmc; )
};

#endif
