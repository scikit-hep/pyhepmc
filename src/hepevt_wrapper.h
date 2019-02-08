#ifndef PYHEPMC_NG_HEPEVT_WRAPPER_H
#define PYHEPMC_NG_HEPEVT_WRAPPER_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "HepMC3/FourVector.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/GenVertex.h"
#include <map>
#include <utility>

template <typename RealType>
bool fill_genevent_from_hepevt(HepMC3::GenEvent& evt,
                               int event_number,
                               pybind11::array_t<RealType> p_array, // N x 4
                               pybind11::array_t<RealType> m_array, // N
                               pybind11::array_t<RealType> v_array, // N x 4
                               pybind11::array_t<int> pid_array,    // N
                               pybind11::array_t<int> parents_array, // N x 2
                               pybind11::array_t<int> /* children_array */, // N x 2, not used
                               pybind11::array_t<int> particle_status_array, // N
                               pybind11::array_t<int> vertex_status_array, // N
                               RealType momentum_scaling,
                               RealType length_scaling) {
    using namespace HepMC3;
    namespace py = pybind11;

    evt.clear();
    evt.set_event_number(event_number);

    // see https://stackoverflow.com/questions/610245/where-and-why-do-i-have-to-put-the-template-and-typename-keywords
    auto pa = p_array.template unchecked<2>();
    auto va = v_array.template unchecked<2>();
    auto ma = m_array.template unchecked<1>();
    auto pid = pid_array.template unchecked<1>();
    auto par = parents_array.template unchecked<2>();
    // auto chi = children_array.template unchecked<2>();
    auto psta = particle_status_array.template unchecked<1>();
    auto vsta = vertex_status_array.template unchecked<1>();

    const int nentries = pa.shape(0);

    assert(va.shape(0) == nentries);
    assert(ma.shape(0) == nentries);
    assert(pid.shape(0) == nentries);
    assert(par.shape(0) == nentries);
    // assert(chi.shape(0) == nentries);
    assert(psta.shape(0) == nentries);
    assert(vsta.shape(0) == nentries);

    /*
        first pass: add all particles to the event
    */
    for (int i = 0; i < nentries; ++i) {
        GenParticlePtr p = std::make_shared<GenParticle>();
        p->set_momentum(FourVector(pa(i, 0) / momentum_scaling,
                                   pa(i, 1) / momentum_scaling,
                                   pa(i, 2) / momentum_scaling,
                                   pa(i, 3) / momentum_scaling));
        p->set_status(psta(i));
        p->set_pid(pid(i));
        p->set_generated_mass(ma(i) * momentum_scaling);
        evt.add_particle(p);
    }
    assert(evt.particles().size() == nentries);

    /*
        second pass: add all vertices and connect topology

        Production vertices are duplicated for each outgoing particle in
        HEPEVT. Common production vertices are identified by having the same
        parents.

        Production vertices for particles without parents are not added.

        Children information is redundant and not used here, but could be used
        in Debug mode to check consistency of the event topology (TODO).
    */
    std::map<std::pair<int, int>, GenVertexPtr> vertex_map;
    for (int i = 0; i < nentries; ++i) {
        // HEPEVT uses Fortran style indices, convert to C++ style
        const auto parents = std::make_pair(par(i, 0)-1, par(i, 1)-1);
        // skip particles without parents
        if (parents.first < 0 || parents.second < 0 ||
            parents.first > parents.second)
            continue;
        assert(parents.second < nentries);
        // get unique production vertex for each particles with parents
        auto vi = vertex_map.find(parents);
        if (vi == vertex_map.end()) {
            GenVertexPtr v = std::make_shared<GenVertex>();
            v->set_position(FourVector(va(i, 0) / length_scaling,
                                       va(i, 1) / length_scaling,
                                       va(i, 2) / length_scaling,
                                       va(i, 3) / length_scaling));
            for (auto j = parents.first; j <= parents.second; ++j)
              v->add_particle_in(evt.particles()[j]);
            v->set_status(vsta(i));
            evt.add_vertex(v);
            vi = vertex_map.insert(std::make_pair(parents, v)).first;
        }
        vi->second->add_particle_out(evt.particles()[i]);
    }

    return true;
}

#endif
