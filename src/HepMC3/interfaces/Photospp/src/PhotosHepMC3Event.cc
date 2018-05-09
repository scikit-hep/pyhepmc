// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#include <vector>
#include "Photos/PhotosHepMC3Particle.h"
#include "Photos/PhotosHepMC3Event.h"
#include "Photos/Log.h"

#include "HepMC/Common.h"
#include "HepMC/Print.h"

using namespace std;

namespace Photospp
{

PhotosHepMC3Event::PhotosHepMC3Event(HepMC::GenEvent * event)
{
        m_event=event;
        FOREACH( const HepMC::GenParticlePtr &p, m_event->particles() )
        {
                PhotosParticle *particle = new PhotosHepMC3Particle(p);
                particles.push_back(particle);
        }
}

PhotosHepMC3Event::~PhotosHepMC3Event()
{
        while(particles.size())
        {
                PhotosParticle *p = particles.back();
                particles.pop_back();
                if(p) delete p;
        }
}

HepMC::GenEvent * PhotosHepMC3Event::getEvent()
{
        return m_event;
}

void PhotosHepMC3Event::print()
{
        if(!m_event) return;
        HepMC::Print::listing(*m_event);
}

vector<PhotosParticle*> PhotosHepMC3Event::getParticleList()
{
        return particles;
}

} // namespace Photospp
