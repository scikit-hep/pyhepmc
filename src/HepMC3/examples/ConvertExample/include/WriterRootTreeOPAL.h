#ifndef  HEPMC_WRITERROOTTREEOPAL_H
#define  HEPMC_WRITERROOTTREEOPAL_H
#include "HepMC/WriterRootTree.h"
#include "HepMC/GenEvent.h"
#include "HepMC/GenParticle.h"
#include "HepMC/Data/GenEventData.h"
namespace HepMC
{
class WriterRootTreeOPAL : public WriterRootTree
{
public:
    WriterRootTreeOPAL(const std::string &filename,shared_ptr<GenRunInfo> run = shared_ptr<GenRunInfo>());
    void init_branches();
    void write_event(const GenEvent &evt);
    void set_run_number(const int nr);
private:
    float  m_Ebeam;
    int    m_Irun;
    int    m_Ievnt;
};
}
#endif
