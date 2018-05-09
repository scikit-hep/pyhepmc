#include "Tauola/TauolaHepMC3Particle.h"
#include "Tauola/Log.h"

#include "HepMC/GenVertex.h"
#include "HepMC/Common.h"
#include "HepMC/Print.h"
using namespace HepMC;

namespace Tauolapp
{

TauolaHepMC3Particle::TauolaHepMC3Particle(){
  m_particle = make_shared<HepMC::GenParticle>();
}

TauolaHepMC3Particle::~TauolaHepMC3Particle(){

  //delete the mother and daughter pointers
  while(m_mothers.size()!=0){
    TauolaParticle * temp = m_mothers.back();
    m_mothers.pop_back();
    delete temp;
  }
  while(m_daughters.size()!=0){
    TauolaParticle * temp = m_daughters.back();
    m_daughters.pop_back();
    delete temp;
  }

  while(m_created_particles.size()!=0){
    TauolaHepMC3Particle * temp = (TauolaHepMC3Particle*) m_created_particles.back();
    m_created_particles.pop_back();
    //if(temp->getHepMC3()->id()==0) delete temp->getHepMC3();
    delete temp;
  }

}

// NOTE: Not executed by release examples
TauolaHepMC3Particle::TauolaHepMC3Particle(int pdg_id, int status, double mass){
  m_particle = make_shared<HepMC::GenParticle>();
  m_particle->set_pid(pdg_id);
  m_particle->set_status(status);
  m_particle->set_generated_mass(mass);
}

TauolaHepMC3Particle::TauolaHepMC3Particle(HepMC::GenParticlePtr particle){
  m_particle = particle;
}

HepMC::GenParticlePtr TauolaHepMC3Particle::getHepMC3(){
  return m_particle;
}

void TauolaHepMC3Particle::undecay(){
/* NO DELETING YET
  std::vector<TauolaParticle*> daughters = getDaughters();
  std::vector<TauolaParticle*>::iterator dIter = daughters.begin();

  for(; dIter != daughters.end(); dIter++)
    (*dIter)->undecay();

  if(m_particle->end_vertex())
  {
  while(m_particle->end_vertex()->particles_out().size())
  {
    HepMC::GenParticlePtr p = m_particle->end_vertex()->remove_particle(*(m_particle->end_vertex()->particles_out_const_begin()));
    delete p;
  }
  delete m_particle->end_vertex();
  }

  m_daughters.clear();
  m_particle->set_status(TauolaParticle::STABLE);

  for(unsigned int i=0;i<daughters.size();i++)
    delete daughters[i];
*/
}

void TauolaHepMC3Particle::setMothers(vector<TauolaParticle*> mothers){

  /******** Deal with mothers ***********/

  //If there are mothers
  if(mothers.size()>0){

    HepMC::GenParticlePtr part;
    part=dynamic_cast<TauolaHepMC3Particle*>(mothers.at(0))->getHepMC3();

    //Use end vertex of first mother as production vertex for particle
    HepMC::GenVertexPtr production_vertex = part->end_vertex();
    HepMC::GenVertexPtr orig_production_vertex = production_vertex;

    //If production_vertex does not exist - create it
    //If it's tau decay - set the time and position including the tau lifetime correction
    //otherwise - copy the time and position of decaying particle
    if(!production_vertex){
      production_vertex = make_shared<HepMC::GenVertex>();
      HepMC::FourVector point = part->production_vertex()->position();
      production_vertex->set_position(point);
      part->parent_event()->add_vertex(production_vertex);
    }

    //Loop over all mothers to check that the end points to the right place
    vector<TauolaParticle*>::iterator mother_itr;
    for(mother_itr = mothers.begin(); mother_itr != mothers.end();
        mother_itr++){

      HepMC::GenParticlePtr moth;
      moth = dynamic_cast<TauolaHepMC3Particle*>(*mother_itr)->getHepMC3();

      if(moth->end_vertex()!=orig_production_vertex)
        Log::Fatal("Mother production_vertices point to difference places. Can not override. Please delete vertices first.",1);
      else
        production_vertex->add_particle_in(moth);

      //update status info
      if(moth->status()==TauolaParticle::STABLE)
        moth->set_status(TauolaParticle::DECAYED);
    }
    production_vertex->add_particle_out(m_particle);
  }
}

void TauolaHepMC3Particle::setDaughters(vector<TauolaParticle*> daughters){

  if(!m_particle->parent_event())
    Log::Fatal("New particle needs the event set before it's daughters can be added",2);

  //If there are daughters
  if(daughters.size()>0){
    // NOTE: Not executed by release examples
    //       because daughters.size() is always 0

    //Use production vertex of first daughter as end vertex for particle
    HepMC::GenParticlePtr first_daughter;
    first_daughter = (dynamic_cast<TauolaHepMC3Particle*>(daughters.at(0)))->getHepMC3();

    HepMC::GenVertexPtr end_vertex;
    end_vertex=first_daughter->production_vertex();
    HepMC::GenVertexPtr orig_end_vertex = end_vertex;

    if(!end_vertex){ //if it does not exist create it
      end_vertex = make_shared<HepMC::GenVertex>();
      m_particle->parent_event()->add_vertex(end_vertex);
    }

    //Loop over all daughters to check that the end points to the right place
    vector<TauolaParticle*>::iterator daughter_itr;
    for(daughter_itr = daughters.begin(); daughter_itr != daughters.end();
        daughter_itr++){

      HepMC::GenParticlePtr daug;
      daug = dynamic_cast<TauolaHepMC3Particle*>(*daughter_itr)->getHepMC3();


      if(daug->production_vertex()!=orig_end_vertex)
        Log::Fatal("Daughter production_vertices point to difference places. Can not override. Please delete vertices first.",3);
      else
        end_vertex->add_particle_out(daug);
    }
    end_vertex->add_particle_in(m_particle);
  }
}

std::vector<TauolaParticle*> TauolaHepMC3Particle::getMothers(){

  if(m_mothers.size()==0&&m_particle->production_vertex()){
    FOREACH( const HepMC::GenParticlePtr &p, m_particle->production_vertex()->particles_in() ) {
      m_mothers.push_back(new TauolaHepMC3Particle(p));
    }
  }
  return m_mothers;
}

std::vector<TauolaParticle*> TauolaHepMC3Particle::getDaughters(){

  if(m_daughters.size()==0&&m_particle->end_vertex()){
    FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_out() ) {
      m_daughters.push_back(new TauolaHepMC3Particle(p));
    }
  }
  return m_daughters;
}

void TauolaHepMC3Particle::checkMomentumConservation(){

  if(!m_particle->end_vertex()) return;

  // HepMC version of check_momentum_conservation
  // with added energy check

  HepMC::FourVector sum;
  FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_in() ) {
    sum += p->momentum();
  }

  FOREACH( const HepMC::GenParticlePtr &p, m_particle->end_vertex()->particles_out() ) {
    sum -= p->momentum();
  }

  if( sum.length() > Tauola::momentum_conservation_threshold ) {
    Log::Warning()<<"Momentum not conserved in the vertex:"<<endl;
    Log::RedirectOutput(Log::Warning(false));
    HepMC::Print::line(m_particle->end_vertex());
    Log::RevertOutput();
    return;
  }

  return;
}

// NOTE: Not executed by release examples
void TauolaHepMC3Particle::setPdgID(int pdg_id){
  m_particle->set_pid(pdg_id);
}

void TauolaHepMC3Particle::setMass(double mass){
  m_particle->set_generated_mass(mass);
}

// NOTE: Not executed by release examples
void TauolaHepMC3Particle::setStatus(int status){
  m_particle->set_status(status);
}

int TauolaHepMC3Particle::getPdgID(){
  return m_particle->pid();
}

int TauolaHepMC3Particle::getStatus(){
  return m_particle->status();
}

int TauolaHepMC3Particle::getBarcode(){
  return m_particle->pid();
}

// Set (X,T) Position of tau decay trees
void TauolaHepMC3Particle::decayEndgame(){

  double lifetime = Tauola::tau_lifetime * (-log( Tauola::randomDouble() ));
  HepMC::FourVector tau_momentum = m_particle->momentum();

  double mass     = sqrt(abs(  tau_momentum.e()*tau_momentum.e()
                             - tau_momentum.px()*tau_momentum.px()
                             - tau_momentum.py()*tau_momentum.py()
                             - tau_momentum.pz()*tau_momentum.pz()
                            ) );

  // Get previous position
  HepMC::FourVector previous_position = m_particle->production_vertex()->position();

  // Calculate new position
  HepMC::FourVector new_position(previous_position.x()+tau_momentum.px()/mass*lifetime,
                                 previous_position.y()+tau_momentum.py()/mass*lifetime,
                                 previous_position.z()+tau_momentum.pz()/mass*lifetime,
                                 previous_position.t()+tau_momentum.e() /mass*lifetime);

  // Set new position
  m_particle->end_vertex()->set_position(new_position);
  recursiveSetPosition(m_particle,new_position);
}

void TauolaHepMC3Particle::recursiveSetPosition(HepMC::GenParticlePtr p, HepMC::FourVector pos){

  if(!p->end_vertex()) return;

  // Iterate over all outgoing particles
  FOREACH( const HepMC::GenParticlePtr &pp, p->end_vertex()->particles_out() ) {
    if( !pp->end_vertex() ) continue;

    // Set position
    /// @bug Position cannot be set (for now)
    //pp->end_vertex()->set_position(pos);
    recursiveSetPosition(pp,pos);
  }
}

TauolaHepMC3Particle * TauolaHepMC3Particle::createNewParticle(
                        int pdg_id, int status, double mass,
                        double px, double py, double pz, double e){

  TauolaHepMC3Particle * new_particle = new TauolaHepMC3Particle();
  new_particle->getHepMC3()->set_pid(pdg_id);
  new_particle->getHepMC3()->set_status(status);
  new_particle->getHepMC3()->set_generated_mass(mass);

  HepMC::FourVector momentum(px,py,pz,e);
  new_particle->getHepMC3()->set_momentum(momentum);

  m_created_particles.push_back(new_particle);

  return new_particle;
}

void TauolaHepMC3Particle::print(){
  HepMC::Print::line(m_particle);
}


/******** Getter and Setter methods: ***********************/

inline double TauolaHepMC3Particle::getPx(){
  return m_particle->momentum().px();
}

inline double TauolaHepMC3Particle::getPy(){
  return m_particle->momentum().py();
}

double TauolaHepMC3Particle::getPz(){
  return m_particle->momentum().pz();
}

double TauolaHepMC3Particle::getE(){
  return m_particle->momentum().e();
}

void TauolaHepMC3Particle::setPx(double px){
  //make new momentum as something is wrong with
  //the HepMC momentum setters

  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPx(px);
  m_particle->set_momentum(momentum);
}

void TauolaHepMC3Particle::setPy(double py){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPy(py);
  m_particle->set_momentum(momentum);
}


void TauolaHepMC3Particle::setPz(double pz){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setPz(pz);
  m_particle->set_momentum(momentum);
}

void TauolaHepMC3Particle::setE(double e){
  HepMC::FourVector momentum(m_particle->momentum());
  momentum.setE(e);
  m_particle->set_momentum(momentum);
}

} // namespace Tauolapp
