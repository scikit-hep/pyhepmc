// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2015 The HepMC collaboration (see AUTHORS for details)
//
///
/// @file Print.cc
/// @brief Implementation of static \b class Print
///
/// @todo AB: Why a static class rather than some namespaced free functions?
///
#include "HepMC/Print.h"
#include "HepMC/Attribute.h"

using namespace std;

namespace HepMC {

void Print::content( std::ostream& os, const GenEvent &event ) {
    os<<"--------------------------------"<<endl;
    os<<"--------- EVENT CONTENT --------"<<endl;
    os<<"--------------------------------"<<endl;
    os<<endl;

    os<<"Weights (" << event.weights().size() <<"): "<<endl;
    for (std::vector<double>::const_iterator w=event.weights().begin();w!=event.weights().end();++w )
    os <<" "<<*w;


    os<<"Attributes:"<<endl;

    typedef map< string, map<int, shared_ptr<Attribute> > >::value_type value_type1;
    typedef map<int, shared_ptr<Attribute> >::value_type                value_type2;

    FOREACH( const value_type1& vt1, event.attributes() ) {
        FOREACH( const value_type2& vt2, vt1.second ) {
            os << vt2.first << ": " << vt1.first << endl;
        }
    }

    os<<"GenParticlePtr ("<<event.particles().size()<<")"<<endl;

    for ( std::vector<HepMC::GenParticlePtr>::const_iterator  p=event.particles().begin(); p!=event.particles().end(); ++p){
        HepMC::Print::line(os, *p, true);
    }

    os<<"GenVertexPtr ("<<event.vertices().size()<<")"<<endl;
    FOREACH( const GenVertexPtr &v, event.vertices() ) {
        HepMC::Print::line(os, v);
    }

    os<<"-----------------------------"<<endl;
}

void Print::listing( std::ostream& os, const GenEvent &event, unsigned short precision ) {

    // Find the current stream state
    ios_base::fmtflags orig = os.flags();
    streamsize         prec = os.precision();

    // Set precision
    os.precision( precision );

    os << "________________________________________________________________________" << endl;
    os << "GenEvent: #" << event.event_number() << endl;
    os << " Momentum units: " << Units::name(event.momentum_unit())
         << " Position units: " << Units::name(event.length_unit()) << endl;
    os << " Entries in this event: " << event.vertices().size() << " vertices, "
         << event.particles().size() << " particles, "
         << event.weights().size()   << " weights." << endl;

    const FourVector &pos = event.event_pos();
    os << " Position offset: " << pos.x() << ", " << pos.y() << ", " << pos.z() << ", " << pos.t() << endl;

    // Print a legend to describe the particle info
    os << "                                    GenParticle Legend" << endl;
    os << "         ID    PDG ID   "
         << "( px,       py,       pz,     E )"
         << "   Stat ProdVtx" << endl;
    os << "________________________________________________________________________" << endl;

    // Print all vertices
    FOREACH( const GenVertexPtr &v, event.vertices() ) {
        HepMC::Print::listing(os, v);
    }

    // Restore the stream state
    os.flags(orig);
    os.precision(prec);
    os << "________________________________________________________________________" << endl;
}

void Print::listing( std::ostream& os, const GenVertexPtr &v ) {
    os << "Vtx: ";
    os.width(6);
    os << v->id() << " stat: ";
    os.width(3);
    os << v->status();

    const FourVector &pos = v->position();
    if( !pos.is_zero() ) {
        os << " (X,cT): " << pos.x()<<" "<<pos.y()<<" "<<pos.z()<<" "<<pos.t();
    }
    else os << " (X,cT): 0";

    os << endl;

    bool printed_header = false;

    // Print out all the incoming particles
    FOREACH( const GenParticlePtr &p, v->particles_in() ) {
        if( !printed_header ) {
            os << " I: ";
            printed_header = true;
        }
        else os << "    ";

        HepMC::Print::listing(os, p);
    }

    printed_header = false;

    // Print out all the outgoing particles
    FOREACH( const GenParticlePtr &p, v->particles_out() ) {
        if( !printed_header ) {
            os << " O: ";
            printed_header = true;
        }
        else os << "    ";

        HepMC::Print::listing(os, p);
    }
}

void Print::listing( std::ostream& os, const GenParticlePtr &p ) {
    os << " ";
    os.width(6);
    os << p->id();
    os.width(9);
    os << p->pid() << " ";
    os.width(9);
    os.setf(ios::scientific, ios::floatfield);
    os.setf(ios_base::showpos);

    const FourVector &momentum = p->momentum();

    os.width(9);
    os << momentum.px() << ",";
    os.width(9);
    os << momentum.py() << ",";
    os.width(9);
    os << momentum.pz() << ",";
    os.width(9);
    os << momentum.e() << " ";
    os.setf(ios::fmtflags(0), ios::floatfield);
    os.unsetf(ios_base::showpos);
    os.width(3);
    os << p->status();

    const GenVertexPtr prod = p->production_vertex();

    if( prod ) {
        os.width(6);
        os << prod->id();
    }

    os << endl;
}
void Print::line(std::ostream& os, const GenEvent &event, bool attributes) {
    os <<"GenEvent: #" << event.event_number();
    if(attributes) for (std::vector<std::string>::const_iterator s=event.attribute_names().begin();s!=event.attribute_names().end();++s) 
    os<<" "<<*s<<"="<<event.attribute_as_string(*s);
    os<<endl;
}

void Print::line(std::ostream& os, const GenVertexPtr &v, bool attributes) {
    os << "GenVertex:  " << v->id() << " stat: ";
    os.width(3);
    os << v->status();
    os << " in: "  << v->particles_in().size();
    os.width(3);
    os << " out: " << v->particles_out().size();

    const FourVector &pos = v->position();
    os << " has_set_position: ";
    if( v->has_set_position() ) os << "true";
    else                        os << "false";

    os << " (X,cT): " << pos.x()<<", "<<pos.y()<<", "<<pos.z()<<", "<<pos.t();
    if(attributes)for (std::vector<std::string>::const_iterator s= v->attribute_names().begin();s!= v->attribute_names().end();++s)  
    os<<" "<<*s<<"="<<v->attribute_as_string(*s);
    os<< endl;

}

void Print::line(std::ostream& os, const GenParticlePtr &p, bool attributes) {

    os << "GenParticle: ";
    os.width(3);
    os << p->id() <<" PDGID: ";
    os.width(5);
    os << p->pid();

    // Find the current stream state
    ios_base::fmtflags orig = os.flags();

    os.setf(ios::scientific, ios::floatfield);
    os.setf(ios_base::showpos);
    streamsize prec = os.precision();

    // Set precision
    os.precision( 2 );

    const FourVector &momentum = p->momentum();

    os << " (P,E)=" << momentum.px()
               << "," << momentum.py()
               << "," << momentum.pz()
               << "," << momentum.e();

    // Restore the stream state
    os.flags(orig);
    os.precision(prec);

    GenVertexPtr prod = p->production_vertex();
    GenVertexPtr end  = p->end_vertex();
    int prod_vtx_id   = (prod) ? prod->id() : 0;
    int end_vtx_id    = (end)  ? end->id()  : 0;

    os << " Stat: " << p->status()
         << " PV: " << prod_vtx_id
         << " EV: " << end_vtx_id<<endl;
    os <<      (*p).attribute_names().size()<< " "<<endl;
         if(attributes)
         {
         std::vector<std::string> names	 =p->attribute_names();
         FOREACH(const std::string &ss, names)
         os<<" "<<ss<<"="<<(*p).attribute_as_string(ss);
         os<< endl;
         }
}

void Print::line(std::ostream& os, shared_ptr<GenCrossSection> &cs) {
    os << " GenCrossSection: " << cs->xsec(0)
         << " " << cs->xsec_err(0)
         << " " << cs->get_accepted_events()
         << " " << cs->get_attempted_events() 
         << " " << endl;
}

void Print::line(std::ostream& os, shared_ptr<GenHeavyIon> &hi) {
    os << " GenHeavyIon: " << hi->Ncoll_hard
         << " " << hi->Npart_proj
         << " " << hi->Npart_targ
         << " " << hi->Ncoll
         << " " << hi->spectator_neutrons
         << " " << hi->spectator_protons
         << " " << hi->N_Nwounded_collisions
         << " " << hi->Nwounded_N_collisions
         << " " << hi->Nwounded_Nwounded_collisions
         << " " << hi->impact_parameter
         << " " << hi->event_plane_angle
         << " " << hi->eccentricity
         << " " << hi->sigma_inel_NN
         << endl;
}

void Print::line(std::ostream& os, shared_ptr<GenPdfInfo> &pi) {
    os << " GenPdfInfo: " << pi->parton_id[0]
         << " " << pi->parton_id[1]
         << " " << pi->x[0]
         << " " << pi->x[1]
         << " " << pi->scale
         << " " << pi->xf[0]
         << " " << pi->xf[1]
         << " " << pi->pdf_id[0]
         << " " << pi->pdf_id[1]
         << " " << endl;
}

} // namespace HepMC
