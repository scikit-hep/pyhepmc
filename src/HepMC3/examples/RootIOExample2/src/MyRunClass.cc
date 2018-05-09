#include "MyRunClass.h"

MyRunClass::MyRunClass():someint(0), run(0){};

void MyRunClass::SetRunInfo(HepMC::GenRunInfo* myrun)
{
  run = myrun;
}

HepMC::GenRunInfo* MyRunClass::GetRunInfo()
{
  return run;
}

void MyRunClass::SetInt(int theint)
{
  someint = theint;
}

int MyRunClass::GetInt()
{
  return someint;
}

