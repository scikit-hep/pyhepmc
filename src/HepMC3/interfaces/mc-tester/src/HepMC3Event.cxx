#include "HepMC3Event.h"
#include <iostream>
using namespace std;

#ifdef _USE_ROOT_
ClassImp(HepMCEvent)
#endif

HepMC3Event::HepMC3Event( HepMC::GenEvent &e, bool include_self_decay){

  evt = &e;
  // Make a list of the particles in the event.
  // (Modifying these will not effect the GenParticles
  // in the HepMC::GenEvent). The pcle IDs given start at 1
  // (and may differ from "id" in the GenEvent)
  count_self_decays=include_self_decay;

  m_particle_count = e.particles().size();

  particles = new HepMC3Particle*[m_particle_count];

  for(int i=0; i<m_particle_count; ++i) {
    particles[i] = new HepMC3Particle(*e.particles()[i],this,i+1);
  }
}

int HepMC3Event::GetNumOfParticles(){
  return m_particle_count;
}

void  HepMC3Event::SetNumOfParticles(int num){
  // Should throw some error as this can not be set
  cout << "Warning, should not be doing this for HepMCEvent" << endl;
}

int HepMC3Event::GetEventNumber(){
  return evt->event_number();
}

void HepMC3Event::SetEventNumber(int num){
  evt->set_event_number( num );
}


HEPParticle* HepMC3Event::GetParticle(int idx){
  if(idx < 1 || idx > GetNumOfParticles()){
    cout << "Warning can not get particle "<< idx;
    cout <<", particle ID not valid" << endl;
    return 0;
  }
  return particles[idx-1]; //Particle ID starts at 1
}

//Only implemented in HepMCEvent. Returns particle by HepMC id.
HepMC3Particle* HepMC3Event::GetParticleWithId( int id ){
  for(int i=0; i <  GetNumOfParticles(); i++){
    if(particles[i]->part->id()==id)
      return particles[i];
  }
  cout << "Could not find particle with id "<<id<<endl;
  return 0; //and have some error about not finding the
            //particle
}

HEPParticleList* HepMC3Event::FindParticle(int pdg, HEPParticleList *list)
{
  // if list is not provided, it is created
  if (!list) list=new HEPParticleList();

  //loop over all particles in the event
  for (int i=1; i<=GetNumOfParticles(); i++) {
    HEPParticle * p = GetParticle(i);
    if(p->GetPDGId()==pdg){
      list->push_back(p);
      HepMC::GenVertexPtr end = ((HepMC3Particle *) p)->part->end_vertex();
      //if we want to ignore cases like tau->tau+gamma:
      if(!CountSelfDecays()&&end){
        //Check for daughters that are the same particle type
        //If found, remove from list.
        for(unsigned int i=0; i<end->particles_out().size(); ++i) {
          if(end->particles_out()[i]->pid() == pdg)
            list->remove(p);
        }
      }
    }
  }
  return list;
}


//Methods not implemented
void  HepMC3Event::AddParticle( HEPParticle *p){}
void  HepMC3Event::SetParticle(int idx,HEPParticle *p){}
void  HepMC3Event::InsertParticle(int at_idx,HEPParticle *p){}
void  HepMC3Event::Clear(int fromIdx=1){}
void  HepMC3Event::AddParticle( int id,
                                         int pdgid,
                                         int status,
                                         int mother,
                                         int mother2,
                                         int firstdaughter,
                                         int lastdaughter,
                                         double E,
                                         double px,
                                         double py,
                                         double pz,
                                         double m,
                                         double vx,
                                         double vy,
                                         double vz,
                               double tau){}

vector<double> * HepMC3Event::Sum4Momentum(){
  vector<double> * sum = new vector<double>(4,0.0);

  for(int i=0; i < GetNumOfParticles(); i++){
    if(particles[i]->IsStable()){
      sum->at(0)+=particles[i]->GetPx();
      sum->at(1)+=particles[i]->GetPy();
      sum->at(2)+=particles[i]->GetPz();
      sum->at(3)+=particles[i]->GetE();
    }
  }
  return sum;
}

HepMC3Event::~HepMC3Event(){
  for(int i=0; i < GetNumOfParticles(); i++){
    delete particles[i];
  }
  delete[] particles;
}

#ifdef _USE_ROOT_
void HepMC3Event::Streamer(TBuffer &)
{
  // streamer class for ROOT compatibility
}
#endif
