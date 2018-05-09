// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#ifndef _PhotosHepMC3Particle_h_included_
#define _PhotosHepMC3Particle_h_included_

/**
 * @class PhotosHepMC3Particle
 *
 * @brief Interface to HepMC::GenParticle objects
 *
 * This class implements the virtual methods of
 * PhotosParticle. In this way it provides an
 * interface between the generic PhotosParticle class
 * and a HepMC::GenParticle object.
 *
 * @author Nadia Davidson
 * @date 17 June 2008
 *
 * This code is licensed under GNU General Public Licence.
 * For more informations, see: http://www.gnu.org/licenses/
 */

#include <vector>

#include "HepMC/GenParticle.h"
#include "Photos/PhotosParticle.h"

using namespace std;

namespace Photospp
{

class PhotosHepMC3Particle: public PhotosParticle{

 public:
  /** General constructor */
  PhotosHepMC3Particle();

  /** Constructor which keeps a pointer to the HepMC::GenParticle*/
  PhotosHepMC3Particle(HepMC::GenParticlePtr particle);

  /** Constructor which creates a new HepMC::GenParticle and
       sets the properties pdg_id, statu and mass. */
  PhotosHepMC3Particle(int pdg_id, int status, double mass);

  /** Destructor */
  ~PhotosHepMC3Particle();

  /** return the HepMC::GenParticlePtr */
  HepMC::GenParticlePtr getHepMC3();

  /** Set the mothers of this particle via a vector of PhotosParticle*/
  void setMothers(std::vector<PhotosParticle*> mothers);

  /** Set the daughters of this particle via a vector of PhotosParticle*/
  void setDaughters(std::vector<PhotosParticle*> daughters);

  /** Add a new daughter to the end vertex of this particle */
  void addDaughter(PhotosParticle* daughter);

  /** Returns the mothers of this particle via a vector of PhotosParticle */
  std::vector<PhotosParticle*> getMothers();

  /** Returns the daughters of this particle via a vector of PhotosParticle
      IMPORTANT: this method will remeber list from the first call. Particles
      (e.g. photons) added later will be ignored */
  std::vector<PhotosParticle*> getDaughters();

  /** Returns all particles in the decay tree of this particle
      via a vector of PhotosParticle */
  std::vector<PhotosParticle*> getAllDecayProducts();

  /** Set the PDG ID code of this particle */
  void setPdgID(int pdg_id);

  /** Set the status of this particle */
  void setStatus(int statu);

  /** Set the mass of this particle */
  void setMass(double mass);

  /** Get the PDG ID code of this particle */
  int getPdgID();

  /** Get the status of this particle */
  int getStatus();

  /** Get the barcode of this particle */
  int getBarcode();

  /** check that the 4 momentum in conserved at the vertices producing
      and ending this particle */
  bool checkMomentumConservation();

  /** Create a new particle of type PhotosHepMC3Particle, with the given
      properties. The new particle bares no relations to this
      particle, but it provides a way of creating a instance of
      this derived class. eg. createNewParticle() is used inside
      filhep_() so that a PhotosHepMC3Particle can be created without
      the method having explicit knowledge of the PhotosHepMC3Particle
      class */
  PhotosHepMC3Particle * createNewParticle(int pdg_id, int status, double mass,
                                       double px, double py,
                                       double pz, double e);

  /** Create history entry for HepMC event record.
      Creates copy of this particle with status = 3 */
  void createHistoryEntry();

  /** Create a self-decay vertex for this particle
      with 'out' being the outgoing particle in new vertex */
  void createSelfDecayVertex(PhotosParticle *out);

  /** Print some information about this particle to standard output */
  void print();

  /** Returns the px component of the four vector*/
  double getPx();

  /** Returns the py component of the four vector */
  double getPy();

  /** Returns the pz component of the four vector */
  double getPz();

  /** Returns the energy component of the four vector */
  double getE();

  /** Returns the mass taken from event record */
  double getMass();

  /** Set the px component of the four vector */
  void setPx( double px );

  /** Set the px component of the four vector */
  void setPy( double py );

  /** Set the pz component of the four vector */
  void setPz( double pz );

  /** Set the energy component of the four vector */
  void setE( double e );

 private:
  /** Internal function used to clear particles from the vector */
  void clear(std::vector<PhotosParticle*> v);

  /** A pointer to the HepMC::GenParticle particle */
  HepMC::GenParticlePtr m_particle;

  /** A vector of this particles mothers */
  std::vector<PhotosParticle*> m_mothers;

  /** A vector of this particles daughters */
  std::vector<PhotosParticle*> m_daughters;

  /** A vector of all decay products of this particle */
  std::vector<PhotosParticle*> m_decay_products;

  /** list to keep track of new particles which have been
      created from this one, so we can call their destructor later */
  std::vector<PhotosParticle*> m_created_particles;

};

} // namespace Photospp
#endif
