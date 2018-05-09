// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2015 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_HEAVYION_H
#define  HEPMC_HEAVYION_H
/**
 *  @file GenHeavyIon.h
 *  @brief Definition of attribute \b class GenHeavyIon
 *
 *  @class HepMC::GenHeavyIon
 *  @brief Stores additional information about Heavy Ion generator
 *
 *  This is an example of event attribute used to store Heavy Ion information
 *
 *  @ingroup attributes
 *
 */
#include <iostream>
#include "HepMC/Attribute.h"

namespace HepMC {


class GenHeavyIon : public Attribute {

//
// Fields
//
public:
    int    Ncoll_hard;                   ///< Number of hard collisions
  /* We should define the meaning of "hard" */
    int    Npart_proj;                   ///< Number of participating nucleons in the projectile
  /* Does "participating" mean (non-) diffractively wounded? */
    int    Npart_targ;                   ///< Number of participating nucleons in the target
    int    Ncoll;                        ///< Number of collisions
  /* I assume this is not "hard" (whatever that means) but what is it exactly? */
    int    spectator_neutrons;           ///< Number of spectator neutrons
  /* Completely non-interacting? Why is it not seaparatly for target and projectile? */
    int    spectator_protons;            ///< Number of spectator protons
    int    N_Nwounded_collisions;        ///< @todo Describe!
    int    Nwounded_N_collisions;        ///< @todo Describe!
    int    Nwounded_Nwounded_collisions; ///< @todo Describe!
  /* Yes, please describe! */
    double impact_parameter;             ///< Impact parameter
  /* In the standard units of HepMC (CM/MM)? */
    double event_plane_angle;            ///< Event plane angle
  /* I asume this is the angle of the impact parameter vector + pi/2. */
    double eccentricity;                 ///< Eccentricity
  /* I'm sure there is a standard definition of this. */
    double sigma_inel_NN;                ///< Assumed nucleon-nucleon cross-section
  /* I assume this is the total - elastic cross section. Or is it the
   * non-diffractive cross section. I assume that this would be the
   * same for all events in a run. */
    double centrality;                   ///< Centrality
  /* I assume this is a number between 0 and 1, where 0 is the
   * maximally central. Or is in percent? */

  /* For all these, there should be a default value (set in the
   * constructor) indicating that the corresponding information was
   * not given. I guess -1 would do for all of them. Currently the
   * is_valid() function requres that all fields should be non-zero,
   * but I guess that not all generators are able to supply all the
   * information.*/

//
// Functions
//
public:
    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att);

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const;

    /** @brief Set all fields */
    void set( int nh, int np, int nt, int nc, int ns, int nsp,
              int nnw=0, int nwn=0, int nwnw=0,
              float im=0., float pl=0., float ec=0., float s=0., float cent=0. );

    bool operator==( const GenHeavyIon& ) const; ///< Operator ==
    bool operator!=( const GenHeavyIon& ) const; ///< Operator !=
    bool is_valid()                       const; ///< Verify that the instance contains non-zero information
};


#ifndef HEPMC_NO_DEPRECATED
typedef GenHeavyIon HeavyIon; ///< Backward compatibility typedef
#endif


} // namespace HepMC

#endif
