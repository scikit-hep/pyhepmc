// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2015 The HepMC collaboration (see AUTHORS for details)
//
#ifndef  HEPMC_ATTRIBUTE_H
#define  HEPMC_ATTRIBUTE_H
/**
 *  @file Attribute.h
 *  @brief Definition of \b class Attribute, \b class IntAttribute and \b class StringAttribute
 *
 *  @class HepMC::Attribute
 *  @brief Base class for all attributes
 *
 *  Contains virtual functions to_string and from_string that
 *  each attribute must implement, as well as init function that
 *  attributes should overload to initialize parsed attribute
 *
 *  @ingroup attributes
 *
 */
#include <cstdio> // sprintf
#include <string>
#include <limits>
#include <sstream>
#include <iomanip>

#include "HepMC/Common.h"
#include "HepMC/Data/SmartPointer.h"

using std::string;

namespace HepMC {

/** @brief Forward declaration of GenEvent. */
class GenEvent;

/** @brief Forward declaration of GenRunInfo. */
class GenRunInfo;

/** @brief Forward declaration of GenParticle. */
// class GenParticle;

class Attribute {
//
// Constructors
//
public:
    /** @brief Default constructor */
    //Note: m_event should be set to nullptr in case event is deleted!
    Attribute():m_is_parsed(true) {    m_event=nullptr; }

    /** @brief Virtual destructor */
    virtual ~Attribute() {}

protected:
    /** @brief Protected constructor that allows to set string
     *
     *  Used when parsing attributes from file. An StringAttribute class
     *  object is made, which uses this constructor to signify that
     *  it just holds string without parsing it.
     *
     *  @note There should be no need for user class to ever use this constructor
     */
    //Note: m_event should be set to nullptr in case event is deleted!
    Attribute(const string &st):m_is_parsed(false),m_string(st) { m_event=nullptr; }

    /** @brief GenEvent is a friend */
    friend class GenEvent;
    
//
// Virtual Functions
//
public:
    /** @brief Fill class content from string.
     */
    virtual bool from_string(const string & att) = 0;

    /** @brief Optionally initialize the attribute after from_string.
     */
    virtual bool init() {
        return true;
    }

    /** @brief Optionally initialize the attribute after from_string
     *
     * Is passed a reference to the GenRunInfo object to which the
     * Attribute belongs.
     */
    virtual bool init(const GenRunInfo & ) {
	return true;
    }

    /** @brief Fill string from class content */
    virtual bool to_string(string &att) const = 0;

//
// Accessors
//
public:
    /** @brief Check if this attribute is parsed */
    bool is_parsed() const { return m_is_parsed; }

    /** @brief Get unparsed string */
    const string& unparsed_string() const { return m_string; }

    /** return the GenEvent to which this Attribute belongs, if at all. */
    const GenEvent * event() const {
        return m_event;
    }

    /** return the GenParticle to which this Attribute belongs, if at all. */
    GenParticlePtr particle() const {
        return m_particle;
    }

    /** return the GenVertex to which this Attribute belongs, if at all. */
    GenVertexPtr vertex() const {
        return m_vertex;
    }

protected:
    /** @brief Set is_parsed flag */
    void set_is_parsed(bool flag) { m_is_parsed = flag; }

    /** @brief Set unparsed string */
    void set_unparsed_string(const string &st) { m_string = st; }

//
// Fields
//
private:
    bool   m_is_parsed;             //!< Is this attribute parsed?
    string m_string;                //!< Raw (unparsed) string
    const GenEvent * m_event;       //!< Possibility to be aware of the
                                    //!  controlling GenEvent object.
    GenParticlePtr m_particle; //!< Particle to which assigned.
    GenVertexPtr m_vertex;      //!< Vertex to which assigned.
};

/**
 *  @class HepMC::IntAttribute
 *  @brief Attribute that holds an Integer implemented as an int
 *
 *  @ingroup attributes
 */
class IntAttribute : public Attribute {
public:

    /** @brief Default constructor */
    IntAttribute():Attribute(),m_val(0) {}

    /** @brief Constructor initializing attribute value */
    IntAttribute(int val):Attribute(),m_val(val) {}

    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att) {
        m_val = atoi( att.c_str() );
        return true;
    }

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const {
#ifdef HEPMC_HAS_CXX11
        att = std::to_string(m_val);
#else
        char buf[24];
        sprintf(buf,"%23i",m_val);
        att = buf;
#endif
        return true;
    }

    /** @brief get the value associated to this Attribute. */
    int value() const {
	return m_val;
    }

    /** @brief set the value associated to this Attribute. */
    void set_value(const int& i) {
	m_val = i;
    }

private:
    int m_val; ///< Attribute value
};

/**
 *  @class HepMC::LongAttribute
 *  @brief Attribute that holds an Integer implemented as an int
 *
 *  @ingroup attributes
 */
class LongAttribute : public Attribute {
public:

    /** @brief Default constructor */
    LongAttribute(): Attribute(), m_val(0) {}

    /** @brief Constructor initializing attribute value */
    LongAttribute(long val): Attribute(), m_val(val) {}

    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att) {
        m_val = atoi( att.c_str() );
        return true;
    }

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const {
#ifdef HEPMC_HAS_CXX11
        att = std::to_string(m_val);
#else
        char buf[24];
        sprintf(buf,"%23li",m_val);
        att = buf;
#endif
        return true;
    }

    /** @brief get the value associated to this Attribute. */
    long value() const {
	return m_val;
    }

    /** @brief set the value associated to this Attribute. */
    void set_value(const long& l) {
	m_val = l;
    }

private:

    long m_val; ///< Attribute value

};

/**
 *  @class HepMC::DoubleAttribute
 *  @brief Attribute that holds a real number as a double.
 *
 *  @ingroup attributes
 */
class DoubleAttribute : public Attribute {
public:

    /** @brief Default constructor */
    DoubleAttribute(): Attribute(), m_val(0.0) {}

    /** @brief Constructor initializing attribute value */
    DoubleAttribute(double val): Attribute(), m_val(val) {}

    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att) {
        m_val = atof( att.c_str() );
        return true;
    }

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const {
      std::ostringstream oss;
      oss << std::setprecision(std::numeric_limits<double>::digits10)
	  << m_val;
      att = oss.str();
      return true;
    }

    /** @brief get the value associated to this Attribute. */
    double value() const {
	return m_val;
    }

    /** @brief set the value associated to this Attribute. */
    void set_value(const double& d) {
	m_val = d;
    }

private:

    double m_val; ///< Attribute value
};

/**
 *  @class HepMC::FloatAttribute
 *  @brief Attribute that holds a real number as a float.
 *
 *  @ingroup attributes
 */
class FloatAttribute : public Attribute {
public:

    /** @brief Default constructor */
    FloatAttribute(): Attribute(), m_val(0.0) {}

    /** @brief Constructor initializing attribute value */
    FloatAttribute(float val): Attribute(), m_val(val) {}

    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att) {
        m_val = float(atof( att.c_str() ));
        return true;
    }

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const {
      std::ostringstream oss;
      oss << std::setprecision(std::numeric_limits<float>::digits10)
	  << m_val;
      att = oss.str();
      return true;
    }

    /** @brief get the value associated to this Attribute. */
    float value() const {
	return m_val;
    }

    /** @brief set the value associated to this Attribute. */
    void set_value(const float& f) {
	m_val = f;
    }

private:

    float m_val; ///< Attribute value
};

/**
 *  @class HepMC::StringAttribute
 *  @brief Attribute that holds a string
 *
 *  Default attribute constructed when reading input files.
 *  It can be then parsed by other attributes or left as a string.
 *
 *  @ingroup attributes
 *
 */
class StringAttribute : public Attribute {
public:

    /** @brief Default constructor - empty string */
    StringAttribute():Attribute() {}

    /** @brief String-based constructor
     *
     *  The Attribute constructor used here marks that this is an unparsed
     *  string that can be (but does not have to be) parsed
     *
     */
    StringAttribute(const string &st):Attribute(st) {}

    /** @brief Implementation of Attribute::from_string */
    bool from_string(const string &att) {
        set_unparsed_string(att);
        return true;
    }

    /** @brief Implementation of Attribute::to_string */
    bool to_string(string &att) const {
        att = unparsed_string();
        return true;
    }

    /** @brief get the value associated to this Attribute. */
    string value() const {
	return unparsed_string();
    }

    /** @brief set the value associated to this Attribute. */
    void set_value(const string& s) {
	set_unparsed_string(s);
    }

};

} // namespace HepMC

#endif
