// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2015 The HepMC collaboration (see AUTHORS for details)
//
/**
 *  @file GenEvent.cc
 *  @brief Implementation of \b class GenEvent
 *
 */
#include "HepMC/GenEvent.h"
#include "HepMC/GenParticle.h"
#include "HepMC/GenVertex.h"
#include "HepMC/Data/GenEventData.h"

#include <deque>
#include <algorithm> // sort
using namespace std;

namespace HepMC {

GenEvent::GenEvent(Units::MomentumUnit mu,
		   Units::LengthUnit lu)
  : m_event_number(0), m_weights(std::vector<double>(1, 1.0)),
    m_momentum_unit(mu), m_length_unit(lu),
    m_rootvertex(make_shared<GenVertex>()) {}


GenEvent::GenEvent(shared_ptr<GenRunInfo> run,
	 Units::MomentumUnit mu,
	 Units::LengthUnit lu)
  : m_event_number(0), m_weights(std::vector<double>(1, 1.0)),
    m_momentum_unit(mu), m_length_unit(lu),
    m_rootvertex(make_shared<GenVertex>()),
    m_run_info(run) {
  if ( run && !run->weight_names().empty() )
    m_weights = std::vector<double>(run->weight_names().size(), 1.0);
}


// void GenEvent::add_particle( const GenParticlePtr &p ) {
void GenEvent::add_particle( GenParticlePtr p ) {
    if( p->in_event() ) return;
  
    m_particles.push_back(p);

    p->m_event = this;
    p->m_id = particles().size();

    // Particles without production vertex are added to the root vertex
    if( !p->production_vertex() )
      m_rootvertex->add_particle_out(p);
}


GenEvent::GenEvent(const GenEvent&e) {
    if (this != &e)
    {
    std::lock(m_lock_attributes, e.m_lock_attributes);
    std::lock_guard<std::recursive_mutex> lhs_lk(m_lock_attributes, std::adopt_lock);
    std::lock_guard<std::recursive_mutex> rhs_lk(e.m_lock_attributes, std::adopt_lock);  
    GenEventData tdata;
    e.write_data(tdata);
    read_data(tdata);
}
}

GenEvent::~GenEvent() {
    for ( std::map< string, std::map<int, shared_ptr<Attribute> > >::iterator attm=m_attributes.begin();attm!=m_attributes.end();++attm)
    for ( std::map<int, shared_ptr<Attribute> >::iterator att=attm->second.begin();att!=attm->second.end();++att) att->second->m_event = nullptr;
     
    for  ( std::vector<GenVertexPtr>::iterator v=m_vertices.begin();v!=m_vertices.end();++v ) if ((*v)->m_event==this) (*v)->m_event=nullptr;
    for  ( std::vector<GenParticlePtr>::iterator p=m_particles.begin();p!=m_particles.end();++p ) if ((*p)->m_event==this)  (*p)->m_event=nullptr;
}

GenEvent& GenEvent::operator=(const HepMC::GenEvent& e){
     if (this != &e)
     {
        std::lock(m_lock_attributes, e.m_lock_attributes);
        std::lock_guard<std::recursive_mutex> lhs_lk(m_lock_attributes, std::adopt_lock);
        std::lock_guard<std::recursive_mutex> rhs_lk(e.m_lock_attributes, std::adopt_lock);     
        GenEventData tdata;
        e.write_data(tdata);
        read_data(tdata);
     }
     return *this;
} 


// void GenEvent::add_vertex( const GenVertexPtr &v ) {
void GenEvent::add_vertex( GenVertexPtr v ) {
    if( v->in_event() ) return;
    m_vertices.push_back(v);

    v->m_event = this;
    v->m_id = -(int)vertices().size();

    // Add all incoming and outgoing particles and restore their production/end vertices
    FOREACH( GenParticlePtr &p, v->m_particles_in ) {
        if(!p->in_event()) add_particle(p);
        p->m_end_vertex = v->m_this.lock();
    }

    FOREACH( GenParticlePtr &p, v->m_particles_out ) {
        if(!p->in_event()) add_particle(p);
        p->m_production_vertex = v->m_this.lock();
    }
}


void GenEvent::remove_particle( GenParticlePtr p ) {
    if( !p || p->parent_event() != this ) return;
  
    DEBUG( 30, "GenEvent::remove_particle - called with particle: "<<p->id() );
    GenVertexPtr end_vtx = p->end_vertex();
    if( end_vtx ) {
        end_vtx->remove_particle_in(p);

        // If that was the only incoming particle, remove vertex from the event
        if( end_vtx->particles_in().size() == 0 )  remove_vertex(end_vtx);
    }

    GenVertexPtr prod_vtx = p->production_vertex();
    if( prod_vtx ) {
        prod_vtx->remove_particle_out(p);

        // If that was the only outgoing particle, remove vertex from the event
        if( prod_vtx->particles_out().size() == 0 ) remove_vertex(prod_vtx);
    }

    DEBUG( 30, "GenEvent::remove_particle - erasing particle: " << p->id() )

    int idx = p->id();
    vector<GenParticlePtr>::iterator it = m_particles.erase(m_particles.begin() + idx-1 );

    // Remove attributes of this particle
    std::lock_guard<std::recursive_mutex> lock(m_lock_attributes);
    vector<string> atts = p->attribute_names();
    FOREACH( string s, atts) {
        p->remove_attribute(s);
    }

    //
    // Reassign id of attributes with id above this one
    //
#ifndef HEPMC_HAS_CXX0X_GCC_ONLY
       vector<att_val_t> changed_attributes;

    FOREACH( att_key_t& vt1, m_attributes ) {
        changed_attributes.clear();

      FOREACH( const att_val_t& vt2, vt1.second ) {
            if( vt2.first > p->id() ) {
                changed_attributes.push_back(vt2);
            }
        }

        FOREACH( att_val_t val, changed_attributes ) {
            vt1.second.erase(val.first);
            vt1.second[val.first-1] = val.second;
        }
    }
#else
       vector< pair< int, shared_ptr<Attribute> > > changed_attributes;

    FOREACH( att_key_t& vt1, m_attributes ) {
        changed_attributes.clear();

        for ( std::map<int, shared_ptr<Attribute> >::iterator vt2=vt1.second.begin();vt2!=vt1.second.end();++vt2){
            if( (*vt2).first > p->id() ) {
                   changed_attributes.push_back(*vt2);
            }
        }

        FOREACH( att_val_t val, changed_attributes ) {
            vt1.second.erase(val.first);
            vt1.second[val.first-1] = val.second;
        }
    }
#endif
    // Reassign id of particles with id above this one
    for(;it != m_particles.end(); ++it) {
        --((*it)->m_id);
    }

    // Finally - set parent event and id of this particle to 0
    p->m_event = nullptr;
    p->m_id    = 0;
}

    struct sort_by_id_asc {
        inline bool operator()(const GenParticlePtr& p1, const GenParticlePtr& p2) {
            return (p1->id() > p2->id());
        }
    };

void GenEvent::remove_particles( vector<GenParticlePtr> v ) {
    /// @todo Currently the only optimization is sort by id in ascending order.
    ///       Needs better optimization!

    sort( v.begin(), v.end(), sort_by_id_asc() );

    for (std::vector<GenParticlePtr>::iterator p=v.begin();p!=v.end();++p) {
        remove_particle(*p);
    }
}

void GenEvent::remove_vertex( GenVertexPtr v ) {
    if( !v || v->parent_event() != this ) return;
  
    DEBUG( 30, "GenEvent::remove_vertex   - called with vertex:  "<<v->id() );
    shared_ptr<GenVertex> null_vtx;

    FOREACH( GenParticlePtr &p, v->m_particles_in ) {
        p->m_end_vertex.reset();
    }

    FOREACH( GenParticlePtr &p, v->m_particles_out ) {
        p->m_production_vertex.reset();

        // recursive delete rest of the tree
        remove_particle(p);
    }

    // Erase this vertex from vertices list
    DEBUG( 30, "GenEvent::remove_vertex   - erasing vertex: " << v->id() )

    int idx = -v->id();
    vector<GenVertexPtr>::iterator it = m_vertices.erase(m_vertices.begin() + idx-1 );
    // Remove attributes of this vertex
    std::lock_guard<std::recursive_mutex> lock(m_lock_attributes);
    vector<string> atts = v->attribute_names();
    FOREACH( string s, atts) {
        v->remove_attribute(s);
    }

    //
    // Reassign id of attributes with id below this one
    //
#ifndef HEPMC_HAS_CXX0X_GCC_ONLY
    vector<att_val_t> changed_attributes;

    FOREACH( att_key_t& vt1, m_attributes ) {
        changed_attributes.clear();

        FOREACH( const att_val_t& vt2, vt1.second ) {
            if( vt2.first < v->id() ) {
                changed_attributes.push_back(vt2);
            }
        }

        FOREACH( att_val_t val, changed_attributes ) {
            vt1.second.erase(val.first);
            vt1.second[val.first+1] = val.second;
        }
    }

    // Reassign id of particles with id above this one
    for(;it != m_vertices.end(); ++it) {
        ++((*it)->m_id);
    }

    // Finally - set parent event and id of this vertex to 0
    v->m_event = nullptr;
    v->m_id    = 0;
#else
    vector< pair< int, shared_ptr<Attribute> > > changed_attributes;

    FOREACH( att_key_t& vt1, m_attributes ) {
        changed_attributes.clear();

        for ( std::map<int, shared_ptr<Attribute> >::iterator vt2=vt1.second.begin();vt2!=vt1.second.end();++vt2){
            if( (*vt2).first < v->id() ) {
                  changed_attributes.push_back(*vt2);
            }
        }

        FOREACH( att_val_t val, changed_attributes ) {
            vt1.second.erase(val.first);
            vt1.second[val.first+1] = val.second;
        }
    }

    // Reassign id of particles with id above this one
    for(;it != m_vertices.end(); ++it) {
        ++((*it)->m_id);
    }

    // Finally - set parent event and id of this vertex to 0
    v->m_event = nullptr;
    v->m_id    = 0;
#endif
}
static bool visit_children(std::map<const GenVertexPtr,int>  &a,const GenVertexPtr& v)
{
for ( std::vector<GenParticlePtr>::const_iterator p=v->particles_out().begin();p!=v->particles_out().end();++p) 
 if ((*p)->end_vertex()) 
 { 
  if (a[(*p)->end_vertex()]!=0) return true;
  else a[(*p)->end_vertex()]++;
  if (visit_children(a,(*p)->end_vertex())) return true;
 }
return false;
}

void GenEvent::add_tree( const vector<GenParticlePtr> &parts ) {

    shared_ptr<IntAttribute> existing_hc=attribute<IntAttribute>("cycles");
    bool has_cycles=false;
    std::map<const GenVertexPtr,int>  sortingv;
    std::vector<GenVertexPtr> noinv;
    if (existing_hc)     if (existing_hc->value()!=0) has_cycles=true;
    if(!existing_hc)
    {
    FOREACH( const GenParticlePtr &p, parts ) {
        const GenVertexPtr &v = p->production_vertex();
        if(v) sortingv[v]=0;
        if( !v || v->particles_in().size()==0 ) {
            const GenVertexPtr &v2 = p->end_vertex();
            if(v2) {noinv.push_back(v2); sortingv[v2]=0;}
        }
    }
    for (std::vector<GenVertexPtr>::const_iterator v=noinv.begin();v!=noinv.end();++v){
    std::map<const GenVertexPtr,int>  sorting_temp=sortingv;
    has_cycles=(has_cycles||visit_children(sorting_temp,*v));
    } 
    }
    if (has_cycles) {	
    add_attribute("cycles", std::make_shared<HepMC::IntAttribute>(1));
    for( std::map<const GenVertexPtr,int>::iterator vi=sortingv.begin();vi!=sortingv.end();++vi) if( !vi->first->in_event() ) add_vertex(vi->first);
    return;
    }
    
    deque<GenVertexPtr> sorting;

    // Find all starting vertices (end vertex of particles that have no production vertex)
    FOREACH( const GenParticlePtr &p, parts ) {
        const GenVertexPtr &v = p->production_vertex();
        if( !v || v->particles_in().size()==0 ) {
            const GenVertexPtr &v2 = p->end_vertex();
            if(v2) sorting.push_back(v2);
        }
    }

    DEBUG_CODE_BLOCK(
        unsigned int sorting_loop_count = 0;
        unsigned int max_deque_size     = 0;
    )

    // Add vertices to the event in topological order
    while( !sorting.empty() ) {
        DEBUG_CODE_BLOCK(
            if( sorting.size() > max_deque_size ) max_deque_size = sorting.size();
            ++sorting_loop_count;
        )

        GenVertexPtr &v = sorting.front();

        bool added = false;

        // Add all mothers to the front of the list
        FOREACH( const GenParticlePtr &p, v->particles_in() ) {
            GenVertexPtr v2 = p->production_vertex();
            if( v2 && !v2->in_event() ) {
                sorting.push_front(v2);
                added = true;
            }
        }

        // If we have added at least one production vertex,
        // our vertex is not the first one on the list
        if( added ) continue;

        // If vertex not yet added
        if( !v->in_event() ) {

            add_vertex(v);

            // Add all end vertices to the end of the list
            FOREACH( const GenParticlePtr &p, v->particles_out() ) {
                GenVertexPtr v2 = p->end_vertex();
                if( v2 && !v2->in_event() ) {
                    sorting.push_back(v2);
                }
            }
        }

        sorting.pop_front();
    }

    DEBUG_CODE_BLOCK(
        DEBUG( 6, "GenEvent - particles sorted: "
                   <<this->particles().size()<<", max deque size: "
                   <<max_deque_size<<", iterations: "<<sorting_loop_count )
    )
return;
}


void GenEvent::reserve(const size_t& parts, const size_t& verts) {
    m_particles.reserve(parts);
    m_vertices.reserve(verts);
}


void GenEvent::set_units( Units::MomentumUnit new_momentum_unit, Units::LengthUnit new_length_unit) {
    if( new_momentum_unit != m_momentum_unit ) {
        FOREACH( GenParticlePtr &p, m_particles ) {
            Units::convert( p->m_data.momentum, m_momentum_unit, new_momentum_unit );
        }

        m_momentum_unit = new_momentum_unit;
    }

    if( new_length_unit != m_length_unit ) {
        FOREACH( GenVertexPtr &v, m_vertices ) {
            FourVector &fv = v->m_data.position;
            if( !fv.is_zero() ) Units::convert( fv, m_length_unit, new_length_unit );
        }

        m_length_unit = new_length_unit;
    }
}


const FourVector& GenEvent::event_pos() const {
    return m_rootvertex->data().position;
}

const vector<GenParticlePtr>& GenEvent::beams() const {
    return m_rootvertex->particles_out();
}

void GenEvent::shift_position_by( const FourVector & delta ) {
    m_rootvertex->set_position( event_pos() + delta );

    // Offset all vertices
    FOREACH ( GenVertexPtr &v, m_vertices ) {
        if ( v->has_set_position() )
            v->set_position( v->position() + delta );
    }
}


void GenEvent::clear() {
    std::lock_guard<std::recursive_mutex> lock(m_lock_attributes);
    m_event_number = 0;
    m_rootvertex = make_shared<GenVertex>();
    m_weights.clear();
    m_attributes.clear();
    m_particles.clear();
    m_vertices.clear();
}




void GenEvent::remove_attribute(const string &name,  const int& id) {
    std::lock_guard<std::recursive_mutex> lock(m_lock_attributes);
    map< string, map<int, shared_ptr<Attribute> > >::iterator i1 =
      m_attributes.find(name);
    if( i1 == m_attributes.end() ) return;

    map<int, shared_ptr<Attribute> >::iterator i2 = i1->second.find(id);
    if( i2 == i1->second.end() ) return;

    i1->second.erase(i2);
}

vector<string> GenEvent::attribute_names( const int& id) const {
    vector<string> results;

    FOREACH( const att_key_t& vt1, m_attributes ) {
        FOREACH( const att_val_t& vt2, vt1.second ) {
            if( vt2.first == id ) results.push_back( vt1.first );
        }
    }

    return results;
}

void GenEvent::write_data(GenEventData& data) const {
    // Reserve memory for containers
    data.particles.reserve( this->particles().size() );
    data.vertices.reserve( this->vertices().size() );
    data.links1.reserve( this->particles().size()*2 );
    data.links2.reserve( this->particles().size()*2 );
    data.attribute_id.reserve( m_attributes.size() );
    data.attribute_name.reserve( m_attributes.size() );
    data.attribute_string.reserve( m_attributes.size() );

    // Fill event data
    data.event_number  = this->event_number();
    data.momentum_unit = this->momentum_unit();
    data.length_unit   = this->length_unit();
    data.event_pos     = this->event_pos();

    // Fill containers
    data.weights = this->weights();

    FOREACH( const GenParticlePtr &p, this->particles() ) {
        data.particles.push_back( p->data() );
    }

    FOREACH( const GenVertexPtr &v, this->vertices() ) {
        data.vertices.push_back( v->data() );
        int v_id = v->id();

        FOREACH( const GenParticlePtr &p, v->particles_in() ) {
            data.links1.push_back( p->id() );
            data.links2.push_back( v_id    );
        }

        FOREACH( const GenParticlePtr &p, v->particles_out() ) {
            data.links1.push_back( v_id    );
            data.links2.push_back( p->id() );
        }
    }

    FOREACH( const att_key_t& vt1, m_attributes ) {
        FOREACH( const att_val_t& vt2, vt1.second ) {

            string st;

            bool status = vt2.second->to_string(st);

            if( !status ) {
                WARNING( "GenEvent::write_data: problem serializing attribute: "<<vt1.first )
            }
            else {
                data.attribute_id.push_back(vt2.first);
                data.attribute_name.push_back(vt1.first);
                data.attribute_string.push_back(st);
            }
        }
    }
}


void GenEvent::read_data(const GenEventData &data) {
    this->clear();
    this->set_event_number( data.event_number );
    this->set_units( data.momentum_unit, data.length_unit );
    this->shift_position_to( data.event_pos );

    // Fill weights
    this->weights() = data.weights;

    // Fill particle information
    FOREACH( const GenParticleData &pd, data.particles ) {
      GenParticlePtr p = make_shared<GenParticle>(pd);

        m_particles.push_back(p);

        p->m_event = this;
        p->m_id    = particles().size();
    }

    // Fill vertex information
    FOREACH( const GenVertexData &vd, data.vertices ) {
      GenVertexPtr v = make_shared<GenVertex>(vd);

        m_vertices.push_back(v);

        v->m_event = this;
        v->m_id    = -(int)vertices().size();
    }

    // Restore links
    for( unsigned int i=0; i<data.links1.size(); ++i) {
      int id1 = data.links1[i];
      int id2 = data.links2[i];

      if( id1 > 0 ) m_vertices[ (-id2)-1 ]->add_particle_in ( m_particles[ id1-1 ] );
      else          m_vertices[ (-id1)-1 ]->add_particle_out( m_particles[ id2-1 ] );
    }

    // Read attributes
    for( unsigned int i=0; i<data.attribute_id.size(); ++i) {
        add_attribute( data.attribute_name[i],
                       make_shared<StringAttribute>(data.attribute_string[i]),
                       data.attribute_id[i] );
    }
}


#ifndef HEPMC_NO_DEPRECATED

//
// Deprecated functions
//

void GenEvent::add_particle( GenParticle *p ) {
    add_particle( GenParticlePtr(p) );
}


void GenEvent::add_vertex( GenVertex *v ) {
    add_vertex( GenVertexPtr(v) );
}

bool GenEvent::valid_beam_particles() const {
    /// @todo Change this definition to require status = 4... and in principle there don't have to be two of them
    return (m_rootvertex->particles_out().size()==2);
}

pair<GenParticlePtr,GenParticlePtr> GenEvent::beam_particles() const {
    /// @todo Change this definition to require status = 4... and in principle there don't have to be two of them
    switch( m_rootvertex->particles_out().size() ) {
        case 0:  return make_pair(GenParticlePtr(),              GenParticlePtr());
        case 1:  return make_pair(m_rootvertex->particles_out()[0], GenParticlePtr());
        default: return make_pair(m_rootvertex->particles_out()[0], m_rootvertex->particles_out()[1]);
    }
}

void GenEvent::set_beam_particles(const GenParticlePtr& p1, const GenParticlePtr& p2) {
    /// @todo Require/set status = 4
    m_rootvertex->add_particle_out(p1);
    m_rootvertex->add_particle_out(p2);
}

void GenEvent::set_beam_particles(const pair<GenParticlePtr,GenParticlePtr>& p) {
    /// @todo Require/set status = 4
    m_rootvertex->add_particle_out(p.first);
    m_rootvertex->add_particle_out(p.second);
}

#endif

string GenEvent::attribute_as_string(const string &name, const int& id) const {
    std::lock_guard<std::recursive_mutex> lock(m_lock_attributes);
    std::map< string, std::map<int, shared_ptr<Attribute> > >::iterator i1 =
      m_attributes.find(name);
    if( i1 == m_attributes.end() ) {
        if ( id == 0 && run_info() ) {
            return run_info()->attribute_as_string(name);
        }
        return string();
    }

    std::map<int, shared_ptr<Attribute> >::iterator i2 = i1->second.find(id);
    if (i2 == i1->second.end() ) return string();

    if( !i2->second ) return string();

    string ret;
    i2->second->to_string(ret);

    return ret;
}

} // namespace HepMC
