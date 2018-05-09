// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//

/**
 * @class HepMC3Event
 * @brief HEPEvent Interface to HepMC classes
 *
 * This class provides a set of methods that allow access to event data
 * stored in HepMC format. The HepMC data structures are used by
 * HEP programs as storage for event records in C++
 *
 * This class extends the HepMC::GenEvent class and implements the methods of
 * HEPEvent used by MC-TESTER. Not all functions are needed by the MC-TESTER,
 * so dummy defintion are introduced for these
 *
 */

#ifndef _HepMC3Event_H
#define _HepMC3Event_H

#include "HepMC/GenEvent.h"
#include "HepMC3Particle.h"
#include "HEPEvent.H"

#ifdef _USE_ROOT_
#include <TObject.h>
#endif

class HepMC3Event: public HEPEvent
{
private:
  /** List of particles in the event */
  HepMC3Particle **particles;

  /** Flag for how particles decaying into there own type are treated */
  bool count_self_decays;

public:
  /** Constructor for HepMC3Event. Creates a new event using the
      event info from HepMC::GenEvent e. Also copies each particle
      into a HepMC3Particle and stores them as a list. */
  HepMC3Event(HepMC::GenEvent &e, bool include_self_decay=true);
  /** Destructor for HepMC3Event */
  ~HepMC3Event();

  /** return the number of particles in the event */
  int GetNumOfParticles();

  /** returns the event number */
  int GetEventNumber();

  /** Dummy function definition. Do not use */
  void SetNumOfParticles(int n);

  /** Dummy function definition. Do not use */
  void SetEventNumber(int ev);

  /** Returns the HEPParticle with id "idx". This is the id number as used
   by MC-TESTER and not the id number from the original HepMC::GenParticle.
   Note: Indecies begin at 1.*/
  HEPParticle* GetParticle( int idx);

  /** Returns the HepMC3Particle by its id. This is the ID
    number from the original HepMC::GenParticle and not the ID used by
    MC-TESTER. */
  HepMC3Particle* GetParticleWithId( int id );

  /** Dummy function definition. Do not use */
  void  SetParticle( int idx, HEPParticle *particle) ;

  /** Dummy function definition. Do not use */
  void  AddParticle( HEPParticle *particle);

  /** Dummy function definition. Do not use */
  void  Clear (int fromIdx);

  /** Dummy function definition. Do not use */
  void  InsertParticle(int at_idx,HEPParticle *p);

  /** Dummy function definition. Do not use */
  void  AddParticle( int id, int pdgid, int status,
                             int mother, int mother2,
                             int firstdaughter, int lastdaughter,
                             double E,double px, double py, double pz, double m,
                             double vx, double vy, double vz, double tau);

  std::vector<double> * Sum4Momentum();

  bool CountSelfDecays(){ return count_self_decays; };

  /** Implementation of FindParticle needed for excluding "self decays" */
  HEPParticleList* FindParticle(int pdg, HEPParticleList *list);

private:
  HepMC::GenEvent *evt;
  int m_particle_count;
#ifdef _USE_ROOT_
  ClassDef(HepMC3Event,1)  //Interface to HepMC event record
#endif
};

#endif
