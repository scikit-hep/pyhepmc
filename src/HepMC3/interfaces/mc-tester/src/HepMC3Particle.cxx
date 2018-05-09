#include "HepMC3Particle.h"
#include "HepMC3Event.h"
#include <iostream>

using namespace std;

#ifdef _USE_ROOT_
ClassImp(HepMC3Particle)
#endif

HepMC3Particle::HepMC3Particle(){}

HepMC3Particle::HepMC3Particle(HepMC::GenParticle & particle, HEPEvent * e, int Id){

  part = &particle;
  SetEvent(e);
  SetId(Id);
}

HepMC3Particle::~HepMC3Particle(){
}

const HepMC3Particle HepMC3Particle::operator=(HEPParticle &p)
{
  if (this == &p)
    return *this;

  // SetId(p.GetId());

  SetPDGId(p.GetPDGId());
  SetStatus(p.GetStatus());
  SetMother(p.GetMother());
  SetMother2(p.GetMother2());
  SetFirstDaughter(p.GetFirstDaughter());
  SetLastDaughter(p.GetLastDaughter());
  SetE(p.GetE());
  SetPx(p.GetPx());
  SetPy(p.GetPy());
  SetPz(p.GetPz());
  SetM(p.GetM());
  SetVx(p.GetVx());
  SetVy(p.GetVy());
  SetVz(p.GetVz());
  SetTau(p.GetTau());

  return *this;

}

HEPEvent* HepMC3Particle::GetEvent(){
  return event;
}

int const HepMC3Particle::GetId(){
  return id;
}

//GetMother and Daughter methods not implemented here
//GetDaughterList() and GetMotherList() should be used
//instead. Still to do: some errors should be thrown.
int const HepMC3Particle::GetMother(){
  return 0;
}

int const HepMC3Particle::GetMother2(){
  return 0;
}

int const HepMC3Particle::GetFirstDaughter(){
  return 0;
}

int const HepMC3Particle::GetLastDaughter(){
  return 0;
}

double const HepMC3Particle::GetE(){
  return part->momentum().e();
}

double const HepMC3Particle::GetPx(){
  return part->momentum().px();
}

double const HepMC3Particle::GetPy(){
  return part->momentum().py();
}

double const HepMC3Particle::GetPz(){
  return part->momentum().pz();
}

double const HepMC3Particle::GetM(){
  return part->momentum().m();
}

int const HepMC3Particle::GetPDGId(){
  return part->pid();
}

int const HepMC3Particle::GetStatus(){
  return part->status();
}

int const HepMC3Particle::IsStable(){
  return (GetStatus() == 1 || !part->end_vertex());
}

int const HepMC3Particle::Decays(){
  return (!IsHistoryEntry() && !IsStable());
}

int const HepMC3Particle::IsHistoryEntry(){
  return (GetStatus() == 3);
}

double const HepMC3Particle::GetVx(){
  if(part->production_vertex()) return part->production_vertex()->position().x();
  return 0.;
}

double const HepMC3Particle::GetVy(){
  if(part->production_vertex()) return part->production_vertex()->position().y();
  return 0.;
}

double const HepMC3Particle::GetVz(){
  if(part->production_vertex()) return part->production_vertex()->position().z();
  return 0.;
}

double const HepMC3Particle::GetTau(){
  //Not implemented
  if(part->end_vertex()&&part->production_vertex())
    return (part->end_vertex()->position().t()-part->production_vertex()->position().t()); //not correct, but will see if it's empty
  else
    return 0;
}

//methods not implemented. Not done for HepMC.
/**void HepMC3Particle::SetP4(MC4Vector &v){ }
void HepMC3Particle::SetP3(MC3Vector &v){ }
void HepMC3Particle::SetV3(MC3Vector &v){ }
**/

void HepMC3Particle::SetEvent(HEPEvent * event){
  this->event=(HepMC3Event*)event;
}

void HepMC3Particle::SetId( int id ){
  this->id = id;
}

//Can not use these methods for HepMC
void HepMC3Particle::SetMother( int mother ){}
void HepMC3Particle::SetMother2( int mother ){}
void HepMC3Particle::SetFirstDaughter( int daughter ){}
void HepMC3Particle::SetLastDaughter ( int daughter ){}

void HepMC3Particle::SetE( double E ){
  HepMC::FourVector temp_mom(part->momentum());
  temp_mom.setE(E);
  part->set_momentum(temp_mom);
}

void HepMC3Particle::SetPx( double px ){
  HepMC::FourVector temp_mom(part->momentum());
  temp_mom.setPx(px);
  part->set_momentum(temp_mom);
}

void HepMC3Particle::SetPy( double py ){
  HepMC::FourVector temp_mom(part->momentum());
  temp_mom.setPy(py);
  part->set_momentum(temp_mom);
}

void HepMC3Particle::SetPz( double pz ){
  HepMC::FourVector temp_mom(part->momentum());
  temp_mom.setPz(pz);
  part->set_momentum(temp_mom);
}

void HepMC3Particle::SetM( double m ){
  //Can not set in HepMC::GenEvent
  cout << "Can not set mass in HepMC3Particle. Set e, px, py, pz instead" <<endl;
}

void HepMC3Particle::SetPDGId ( int pdg ){
  part->set_pid( pdg );
}

void HepMC3Particle::SetStatus( int st){
  part->set_status( st );
}

void HepMC3Particle::SetVx ( double vx){
  //Not implemented
}

void HepMC3Particle::SetVy ( double vy){
  //Not implemented
}

void HepMC3Particle::SetVz ( double vz){
  //Not implemented
}

void HepMC3Particle::SetTau( double tau){
  //Not implemented
}


HEPParticleList* HepMC3Particle::GetDaughterList(HEPParticleList *list)
{
  // if list is not provided, it is created.
  if (!list) list=new HEPParticleList();

  if(!part->end_vertex()) //no daughters
    return list;

  HepMC::GenVertexPtr end = part->end_vertex();

  //iterate over daughters
  for(unsigned int i=0; i<end->particles_out().size(); ++i) {
    HepMC3Particle * daughter = event->GetParticleWithId((end->particles_out()[i])->id());
    if(!list->contains(daughter->GetId())){
      if(!daughter->IsHistoryEntry())
        list->push_back(daughter);
    }
  }
  return list;
}

HEPParticleList* HepMC3Particle::GetMotherList(HEPParticleList *list)
{
   // if list is not provided, it is created.
   if (!list) list=new HEPParticleList();

   if(!part->production_vertex()) //no mothers
     return list;

   HepMC::GenVertexPtr prod = part->production_vertex();

   //iterate over daughters
   for(unsigned int i=0; i<prod->particles_in().size(); ++i) {
       list->push_back(event->GetParticleWithId((prod->particles_in()[i])->id()));
   }

   return list;
}


#ifdef _USE_ROOT_
void HepMC3Particle::Streamer(TBuffer &)
{
  // streamer class for ROOT compatibility
}

#endif
