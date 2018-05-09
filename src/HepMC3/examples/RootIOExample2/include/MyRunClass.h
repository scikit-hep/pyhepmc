#ifndef MYRUNCLASS_H
#define MYRUNCLASS_H

#include "HepMC/GenRunInfo.h"

/** @class MyRunClass
 *  @brief Sample class for root I/O test
 */
class MyRunClass {
public:

    /// @brief Default constructor
    MyRunClass();

    /// @brief Set HepMC event
    void SetRunInfo(HepMC::GenRunInfo*);

    /// @brief Get HepMC event
    HepMC::GenRunInfo* GetRunInfo();

    /// @brief Set someint
    void SetInt(int);

    /// @brief Get someint
    int GetInt();

private:
    int someint;            ///< Test int
    HepMC::GenRunInfo* run; ///< Test run info
};

#endif
