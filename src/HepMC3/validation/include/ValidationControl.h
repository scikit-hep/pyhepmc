// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef VALIDATION_CONTROL_H
#define VALIDATION_CONTROL_H

#ifdef HEPMC2
#include "HepMC/GenEvent.h"
#else
#include "HepMC/GenEvent.h"
#include "HepMC/Print.h"
#include "HepMC/Search/FindParticles.h"
#endif // ifdef HEPMC2

#include "ValidationTool.h"
#include "Timer.h"

#include <vector>

class ValidationControl {
//
// Constructors
//
public:
    ValidationControl();
    ~ValidationControl();

//
// Functions
//
public:
    void read_file(const std::string &filename);
    bool new_event();
    void initialize();
    void process(GenEvent &hepmc);
    void finalize();

//
// Accessors
//
public:
    const std::vector<ValidationTool*>& toolchain() { return m_toolchain; }
    int   event_limit()                             { return m_events;    }
    void  set_event_limit(int events)               { m_events = events;  }

    void  print_events(int events)              { m_print_events          = events; }
    void  check_momentum_for_events(int events) { m_momentum_check_events = events; }

//
// Fields
//
private:
    std::vector<ValidationTool*> m_toolchain;

    int    m_events;
    int    m_events_print_step;
    int    m_momentum_check_events;
    double m_momentum_check_threshold;
    int    m_print_events;
    int    m_event_counter;
    int    m_status;
    Timer  m_timer;

    bool m_has_input_source;

    enum PARSING_STATUS {
        PARSING_OK,
        UNRECOGNIZED_COMMAND,
        UNRECOGNIZED_OPTION,
        UNRECOGNIZED_INPUT,
        UNRECOGNIZED_TOOL,
        UNAVAILABLE_TOOL,
        ADDITIONAL_INPUT,
        CANNOT_OPEN_FILE
    };
};

#endif
