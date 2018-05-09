#include "HepMC/GenEvent.h"

class RootTool2_serialized_class {
public:

    RootTool2_serialized_class():event(0) {
    }

    void SetEvent(HepMC::GenEvent *myevt) {
      event = myevt;
    }

    HepMC::GenEvent* GetEvent() {
      return event;
    }

private:
    HepMC::GenEvent* event;
};
