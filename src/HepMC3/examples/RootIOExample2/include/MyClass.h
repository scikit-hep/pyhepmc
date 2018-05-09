#ifndef MYCLASS_H
#define MYCLASS_H

#include "HepMC/GenEvent.h"

/** @class MyClass
 *  @brief Sample class for root I/O test
 */
class MyClass {
public:

    /// @brief Default constructor
    MyClass();

    /// @brief Set HepMC event
    void SetEvent(HepMC::GenEvent*);

    /// @brief Get HepMC event
    HepMC::GenEvent* GetEvent();

    /// @brief Set someint
    void SetInt(int);

    /// @brief Get someint
    int GetInt();


private:
    int someint;            ///< Test int
    HepMC::GenEvent* event; ///< Test event
};

#endif
