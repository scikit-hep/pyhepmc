#include "MyClass.h"

MyClass::MyClass():someint(0), event(0){};

void MyClass::SetEvent(HepMC::GenEvent* myevt)
{
  event = myevt;
}

HepMC::GenEvent* MyClass::GetEvent()
{
  return event;
}

void MyClass::SetInt(int theint)
{
  someint = theint;
}

int MyClass::GetInt()
{
  return someint;
}
