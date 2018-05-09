// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
/**
 * @class HepMC3Particle
 * @brief HEPParticle interface to HepMC classes
 *
 * HepMC3Particle extends HepMC::GenParticle class, so that
 * MC-TESTER can accesses the particle information through
 * the common HEPEvent methods
 *
 */

#ifndef _HepMC3Particle_H
#define _HepMC3Particle_H

#include "HEPParticle.H"
#include "HepMC/GenParticle.h"
#include "HepMC/GenVertex.h"

#ifdef _USE_ROOT_
#include <TObject.h>
#endif

class HepMC3Event;

class HepMC3Particle : public HEPParticle
{

private:
  /** Event which the particle belongs to.*/
  HepMC3Event *   event;
  /** ID number of particle as given by MC-TESTER (not the same as
    HepMC::GenParticle pdg_id or barcode).*/
  int           id ;

public:
  /** Plain constructor.*/
  HepMC3Particle();
  /** Constructor which makes a HepMC3Particle from HepMC::GenParticle. */
  HepMC3Particle(HepMC::GenParticle& particle, HEPEvent * e, int Id);
  /** Destructor*/
  ~HepMC3Particle();

  /** Set all the particle properties of "p" to this particle.*/
  const HepMC3Particle operator=(HEPParticle &p);

  /** Returns the event that this particle belongs to.*/
  HEPEvent* GetEvent()            ;
  /** returns the ID number of particle as used by MC-TESTER (not
    the same as HepMC::GenParticle pdg_id or barcode).*/
  int    const GetId()            ;
  /** Dummy function definition. Do not use.*/
  int    const GetMother()        ;
  /** Dummy function definition. Do not use.*/
  int    const GetMother2()       ;
  /** Dummy function definition. Do not use.*/
  int    const GetFirstDaughter() ;
  /** Dummy function definition. Do not use.*/
  int    const GetLastDaughter()  ;

  /** Returns the particle's energy */
  double const     GetE ()        ;
  /** Returns the x component of the particle's momentum */
  double const     GetPx()        ;
  /** Returns the y component of the particle's momentum */
  double const     GetPy()        ;
  /** Returns the z component of the particle's momentum */
  double const     GetPz()        ;
  /** Returns the particle's mass */
  double const     GetM ()        ;
  /** Returns the particle's PDG ID code. */
  int    const     GetPDGId ()    ;
  /** Returns the particle's Status code. */
  int    const     GetStatus()    ;
  /** Returns true is the particle has status code 1. */
  int    const     IsStable()     ;
  /** Returns true is the particle has status code 2
    or (for pythia 8) if it has a status < 0, has an end vertex and
    does not have any daughters of the same PDG code.*/
  int    const     Decays();
  /** Returns true is the particle has status code 3 or (for pythia 8)
   if fails both IsStable() and Decays().*/
  int    const     IsHistoryEntry();

  /** Returns the x value of the particle's production vertex */
  double const     GetVx  ()      ;
  /** Returns the y value of the particle's production vertex */
  double const     GetVy  ()      ;
  /** Returns the z value of the particle's production vertex */
  double const     GetVz  ()      ;
  /** Dummy function definition. Do not use.*/
  double const     GetTau ()      ;

  /** Sets the event that this particle belongs to */
  void   SetEvent        ( HEPEvent  *event );
  /** Sets ID (as used by MC-TESTER) of this particle */
  void   SetId           ( int id       );
  /** Dummy function definition. Do not use.*/
  void   SetMother       ( int mother   );
  /** Dummy function definition. Do not use.*/
  void   SetMother2      ( int mother   );
  /** Dummy function definition. Do not use.*/
  void   SetFirstDaughter( int daughter );
  /** Dummy function definition. Do not use.*/
  void   SetLastDaughter ( int daughter );

  /** Sets the energy of this particle */
  void   SetE  ( double E  )      ;
  /** Sets the x component of this particle's momentum */
  void   SetPx ( double px )      ;
  /** Sets the x component of this particle's momentum */
  void   SetPy ( double py )      ;
  /** Sets the x component of this particle's momentum */
  void   SetPz ( double pz )      ;
  /** Dummy function definition. Do not use.*/
  void   SetM  ( double m  )      ;

  /** Sets the PDG ID code of this particle */
  void   SetPDGId ( int pdg )     ;
  /** Sets the status code of this particle */
  void   SetStatus( int st  )     ;
  /** Sets the x value of this particle's production vertex */
  void   SetVx ( double vx  )     ;
  /** Sets the y value of this particle's production vertex */
  void   SetVy ( double vy  )     ;
  /** Sets the z value of this particle's production vertex */
  void   SetVz ( double vz  )     ;
  /** Dummy function definition. Do not use.*/
  void   SetTau( double tau )     ;

  /** Returns a list of daughter particles of this particle.
    If a list of particle is given as a parameter, the daughters
    are appended to the end. If the daughter is already found
    in the list, it is not added. The function finds daughters by
    iterating over the outgoing particles from the end vertex.
    The daughter particle must be stable of decaying to be added to
    the list. (for pythia 8) if the status code is negative, the
    daughter's daughters are searched recursively.*/

  HEPParticleList*  GetDaughterList(HEPParticleList *list);
  /** Returns a list of daughter particles of this particle.*/
  HEPParticleList*  GetMotherList(HEPParticleList *list);
public:
  HepMC::GenParticle *part;

#ifdef _USE_ROOT_
  ClassDef(HepMC3Particle,0)
#endif
};

#endif // _HepMC3Particle_H
