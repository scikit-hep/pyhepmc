// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014 The HepMC collaboration (see AUTHORS for details)
//
#include "HepMC/GenEvent.h"
#include "HepMC/GenVertex.h"
#include "HepMC/GenParticle.h"
#include "HepMC/Common.h"
#include "HepMC/Print.h"
#include "Photos/PhotosHepMC3Particle.h"
#include "Photos/Log.h"
#include "Photos/Photos.h"

using namespace HepMC;

namespace Photospp
{

PhotosHepMC3Particle::PhotosHepMC3Particle(){
  m_particle = make_shared<HepMC::GenParticle>();
}

PhotosHepMC3Particle::PhotosHepMC3Particle(int pdg_id, int status, double mass){
  m_particle = make_shared<HepMC::GenParticle>();
  m_particle->set_pid(pdg_id);
  m_particle->set_status(status);
  m_particle->set_generated_mass(mass);
}

PhotosHepMC3Particle::PhotosHepMC3Particle(HepMC::GenParticlePtr particle){
  m_particle = particle;
}

PhotosHepMC3Particle::~PhotosHepMC3Particle(){
  clear(m_mothers);
  clear(m_daughters);
  //  clear(m_created_particles);
}


//delete the TauolaHepMC3Particle objects
void PhotosHepMC3Particle::clear(std::vector<PhotosParticle*> v){
  while(v.size()!=0){
    PhotosParticle * temp = v.back();
    v.pop_back();
    delete temp;
  }
}

HepMC::GenParticlePtr PhotosHepMC3Particle::getHepMC3(){
  return m_particle;
}

void PhotosHepMC3Particle::setMothers(vector<PhotosParticle*> mothers){

  /******** Deal with mothers ***********/

  clear(m_mothers);

  //If there are mothers
  if(mothers.size()>0){

    HepMC::GenParticlePtr part;
    part=dynamic_cast<PhotosHepMC3Particle*>(mothers.at(0))->getHepMC3();

    //Use end vertex of first mother as production vertex for particle
    HepMC::GenVertexPtr production_vertex = part->end_vertex();
    HepMC::GenVertexPtr orig_production_vertex = production_vertex;

    if(!production_vertex){ //if it does not exist create it
      production_vertex = make_shared<HepMC::GenVertex>();
      part->parent_event()->add_vertex(production_vertex);
    }

    //Loop over all mothers to check that the end points to the right place
    vector<PhotosParticle*>::iterator mother_itr;
    for(mother_itr = mothers.begin(); mother_itr != mothers.end();
        mother_itr++){

      HepMC::GenParticlePtr moth;
      moth = dynamic_cast<PhotosHepMC3Particle*>(*mother_itr)->getHepMC3();

      if(moth->end_vertex()!=orig_production_vertex)
        Log::Fatal("PhotosHepMC3Particle::setMothers(): Mother production_vertices point to difference places. Can not override. Please delete vertices first.",1);
      else
        production_vertex->add_particle_in(moth);

      //update status info
      if(moth->status()==PhotosParticle::STABLE)
        moth->set_status(PhotosParticle::DECAYED);
    }
    production_vertex->add_particle_out(m_particle);
  }
}



void PhotosHepMC3Particle::addDaughter(PhotosParticle* daughter){

  //add to this classes internal list as well.
  m_daughters.push_back(daughter);

  //this assumes there is already an end vertex for the particle

  if(!m_particle->end_vertex())
    Log::Fatal("PhotosHepMC3Particle::addDaughter(): This method assumes an end_vertex exists. Maybe you really want to use setDaughters.",2);

  HepMC::GenParticlePtr daugh = (dynamic_cast<PhotosHepMC3Particle*>(daughter))->getHepMC3();
  m_particle->end_vertex()->add_particle_out(daugh);

}

void PhotosHepMC3Particle::setDaughters(vector<PhotosParticle*> daughters){

  if(!m_particle->parent_event())
    Log::Fatal("PhotosHepMC3Particle::setDaughters(): New particle needs the event set before it's daughters can be added",3);

  clear(m_daughters);

  //If there are daughters
  if(daughters.size()>0){

    //Use production vertex of first daughter as end vertex for particle
    HepMC::GenParticlePtr first_daughter;
    first_daughter = (dynamic_cast<PhotosHepMC3Particle*>(daughters.at(0)))->getHepMC3();

    HepMC::GenVertexPtr end_vertex;
    end_vertex=first_daughter->production_vertex();
    HepMC::GenVertexPtr orig_end_vertex = end_vertex;

    if(!end_vertex){ //if it does not exist create it
      end_vertex = make_shared<HepMC::GenVertex>();
      m_particle->parent_event()->add_vertex(end_vertex);
    }

    //Loop over all daughters to check that the end points to the right place
    vector<PhotosParticle*>::iterator daughter_itr;
    for(daughter_itr = daughters.begin(); daughter_itr != daughters.end();
        daughter_itr++){

      HepMC::GenParticlePtr daug;
      daug = dynamic_cast<PhotosHepMC3Particle*>(*daughter_itr)->getHepMC3();


      if(daug->production_vertex()!=orig_end_vertex)
        Log::Fatal("PhotosHepMC3Particle::setDaughters(): Daughter production_vertices point to difference places. Can not override. Please delete vertices first.",4);
      else
        end_vertex->add_particle_out(daug);
    }
    end_vertex->add_particle_in(m_particle);
  }

}

std::vector<PhotosParticle*> PhotosHepMC3Particle::getMothers(){

  if(m_mothers.size()==0&&m_particle->production_vertex()){

    FOREACH( const HepMC::GenParticlePtr &p, m_particle->production_vertex()->particles_in() ) {
      m_mothers.push_back(new PhotosHepMC3Particle(p));
    }
  }
  return m_mothers;
}

std::vector<PhotosParticle*> PhotosHepMC3Particle::getDaughters(){

  if(m_daughters.size()==0&&m_particle->end_vertex()){

    FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_out() ) {

      // ommit particles if their status code is ignored by Photos
      if( Photos::isStatusCodeIgnored( p->status() ) ) continue;

      m_daughters.push_back(new PhotosHepMC3Particle(p));
    }
  }
  return m_daughters;

}

std::vector<PhotosParticle*> PhotosHepMC3Particle::getAllDecayProducts(){

  m_decay_products.clear();

  if(!hasDaughters()) // if this particle has no daughters
    return m_decay_products;

  std::vector<PhotosParticle*> daughters = getDaughters();

  // copy daughters to list of all decay products
  m_decay_products.insert(m_decay_products.end(),daughters.begin(),daughters.end());

  // Now, get all daughters recursively, without duplicates.
  // That is, for each daughter:
  // 1)  get list of her daughters
  // 2)  for each particle on this list:
  //  a) check if it is already on the list
  //  b) if it's not, add her to the end of the list
  for(unsigned int i=0;i<m_decay_products.size();i++)
  {
    std::vector<PhotosParticle*> daughters2 = m_decay_products[i]->getDaughters();

    if(!m_decay_products[i]->hasDaughters()) continue;
    for(unsigned int j=0;j<daughters2.size();j++)
    {
      bool add=true;
      for(unsigned int k=0;k<m_decay_products.size();k++)
        if( daughters2[j]->getBarcode() == m_decay_products[k]->getBarcode() )
        {
          add=false;
          break;
        }

      if(add) m_decay_products.push_back(daughters2[j]);
    }
  }
  return m_decay_products;
}

bool PhotosHepMC3Particle::checkMomentumConservation(){

  if(!m_particle->end_vertex()) return true;

  // HepMC version of check_momentum_conservation
  // with added energy check
  HepMC::FourVector sum;

  FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_in() ) {
    if( Photos::isStatusCodeIgnored(p->status()) ) continue;

    sum += p->momentum();
  }

  FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_out() ) {
    if( Photos::isStatusCodeIgnored(p->status()) ) continue;

    sum -= p->momentum();
  }

  if( sum.length() > Photos::momentum_conservation_threshold ) {
    Log::Warning()<<"Momentum not conserved in the vertex:"<<endl;
    Log::RedirectOutput(Log::Warning(false));
    HepMC::Print::line(m_particle->end_vertex());
    Log::RevertOutput();
    return false;
  }

  return true;
}

void PhotosHepMC3Particle::setPdgID(int pdg_id){
  m_particle->set_pid(pdg_id);
}

void PhotosHepMC3Particle::setMass(double mass){
  m_particle->set_generated_mass(mass);
}

void PhotosHepMC3Particle::setStatus(int status){
  m_particle->set_status(status);
}

int PhotosHepMC3Particle::getPdgID(){
  return m_particle->pid();
}

int PhotosHepMC3Particle::getStatus(){
  return m_particle->status();
}

int PhotosHepMC3Particle::getBarcode(){
  return m_particle->id();
}


PhotosHepMC3Particle * PhotosHepMC3Particle::createNewParticle(
                        int pdg_id, int status, double mass,
                        double px, double py, double pz, double e){

  PhotosHepMC3Particle * new_particle = new PhotosHepMC3Particle();
  new_particle->getHepMC3()->set_pid(pdg_id);
  new_particle->getHepMC3()->set_status(status);
  new_particle->getHepMC3()->set_generated_mass(mass);

  HepMC::FourVector momentum(px,py,pz,e);
  new_particle->getHepMC3()->set_momentum(momentum);

  m_created_particles.push_back(new_particle);
  return new_particle;
}

void PhotosHepMC3Particle::createHistoryEntry(){

  if(!m_particle->production_vertex())
  {
    Log::Warning()<<"PhotosHepMC3Particle::createHistoryEntry(): particle without production vertex."<<endl;
    return;
  }

  HepMC::GenParticlePtr part = make_shared<HepMC::GenParticle>(*m_particle);
  part->set_status(Photos::historyEntriesStatus);
  m_particle->production_vertex()->add_particle_out(part);
}

void PhotosHepMC3Particle::createSelfDecayVertex(PhotosParticle *out)
{
  if(m_particle->end_vertex())
  {
    Log::Error()<<"PhotosHepMC3Particle::createSelfDecayVertex: particle already has end vertex!"<<endl;
    return;
  }

  if(getHepMC3()->parent_event()==NULL)
  {
    Log::Error()<<"PhotosHepMC3Particle::createSelfDecayVertex: particle not in the HepMC event!"<<endl;
    return;
  }

  // Add new vertex and new particle to HepMC
  HepMC::GenParticlePtr outgoing = make_shared<HepMC::GenParticle>( *(dynamic_cast<PhotosHepMC3Particle*>(out)->m_particle) );
  HepMC::GenVertexPtr v          = make_shared<HepMC::GenVertex>();

  // Copy vertex position from parent vertex
  v->set_position( m_particle->production_vertex()->position() );

  v->add_particle_in (m_particle);
  v->add_particle_out(outgoing);

  getHepMC3()->parent_event()->add_vertex(v);

  // If this particle was stable, set its status to 2
  if(getStatus()==1) setStatus(2);
}

void PhotosHepMC3Particle::print(){
  HepMC::Print::line(m_particle);
}


/******** Getter and Setter methods: ***********************/

inline double PhotosHepMC3Particle::getPx(){
  return m_particle->momentum().px();
}

inline double PhotosHepMC3Particle::getPy(){
  return m_particle->momentum().py();
}

double PhotosHepMC3Particle::getPz(){
  return m_particle->momentum().pz();
}

double PhotosHepMC3Particle::getE(){
  return m_particle->momentum().e();
}

void PhotosHepMC3Particle::setPx(double px){
  //make new momentum as something is wrong with
  //the HepMC momentum setters

  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPx(px);
  m_particle->set_momentum(momentum);
}

void PhotosHepMC3Particle::setPy(double py){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPy(py);
  m_particle->set_momentum(momentum);
}


void PhotosHepMC3Particle::setPz(double pz){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPz(pz);
  m_particle->set_momentum(momentum);
}

void PhotosHepMC3Particle::setE(double e){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setE(e);
  m_particle->set_momentum(momentum);
}

double PhotosHepMC3Particle::getMass()
{
        return m_particle->generated_mass();
}

} // namespace Photospp
