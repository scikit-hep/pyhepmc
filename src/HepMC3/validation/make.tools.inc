INTERFACEDIRECTORY = $(HEPMC3INTERFACES)

#
# ROOT
#
ifneq ($(ROOTCONFIG), )
  override INCLUDES      += -I$(shell $(ROOTCONFIG) --incdir)
  override LINKS_HEPMC3  += -lHepMCrootIO $(shell $(ROOTCONFIG) --glibs)
  override DEFS_HEPMC3   += -DHEPMC_ROOTIO -DROOTCONFIG

  override LINKS_HEPMC2  += $(shell $(ROOTCONFIG) --glibs)
  override DEFS_HEPMC2   += -DROOTCONFIG_HEPMC2

  override VALIDATION_SRC+= src/RootTool.cc src/RootTool2.cc
endif

#
# Photos++
#
PHOTOSINTERFACE = $(INTERFACEDIRECTORY)/Photospp

ifneq ($(PHOTOSLOCATION_HEPMC3), )
  override INTERFACES    += libPhotosHepMC3Interface.so
  override INCLUDES      += -I$(PHOTOSLOCATION_HEPMC3)/include \
                            -I$(PHOTOSINTERFACE)/include
  override RPATHS_HEPMC3 += -Wl,-rpath,$(PHOTOSLOCATION_HEPMC3)/lib \
                            -Wl,-rpath,$(PHOTOSINTERFACE)/lib
  override LINKS_HEPMC3  += -L$(PHOTOSLOCATION_HEPMC3)/lib -lPhotospp \
                            -L$(PHOTOSINTERFACE)/lib -lPhotosHepMC3Interface
  override DEFS_HEPMC3   += -DPHOTOSPP
  override VALIDATION_SRC+= src/PhotosValidationTool.cc
ifneq ($(PHOTOSLOCATION_HEPMC2), )
  override RPATHS_HEPMC2 += -Wl,-rpath,$(PHOTOSLOCATION_HEPMC2)/lib
  override LINKS_HEPMC2  += -L$(PHOTOSLOCATION_HEPMC2)/lib -lPhotospp -lPhotosppHepMC
  override DEFS_HEPMC2   += -DPHOTOSPP_HEPMC2
endif
endif

libPhotosHepMC3Interface.so: $(PHOTOSINTERFACE)/src/PhotosHepMC3Event.o \
                             $(PHOTOSINTERFACE)/src/PhotosHepMC3Particle.o
	mkdir -p $(PHOTOSINTERFACE)/lib/
	$(LD) $(LDFLAGS) $(SOFLAGS) -o $(PHOTOSINTERFACE)/lib/$@ $^

#
# Tauola++
#
TAUOLAINTERFACE = $(INTERFACEDIRECTORY)/Tauolapp

ifneq ($(TAUOLALOCATION_HEPMC3), )
  override INTERFACES    += libTauolaHepMC3Interface.so
  override INCLUDES      += -I$(TAUOLALOCATION_HEPMC3)/include \
                            -I$(TAUOLAINTERFACE)/include
  override RPATHS_HEPMC3 += -Wl,-rpath,$(TAUOLALOCATION_HEPMC3)/lib \
                            -Wl,-rpath,$(TAUOLAINTERFACE)/lib
  override LINKS_HEPMC3  += -L$(TAUOLALOCATION_HEPMC3)/lib -lTauolaCxxInterface -lTauolaFortran \
                            -L$(TAUOLAINTERFACE)/lib -lTauolaHepMC3Interface
  override DEFS_HEPMC3   += -DTAUOLAPP
  override VALIDATION_SRC+= src/TauolaValidationTool.cc
ifneq ($(TAUOLALOCATION_HEPMC2), )
  override RPATHS_HEPMC2 += -Wl,-rpath,$(TAUOLALOCATION_HEPMC2)/lib
  override LINKS_HEPMC2  += -L$(TAUOLALOCATION_HEPMC2)/lib -lTauolaCxxInterface -lTauolaFortran
  override DEFS_HEPMC2   += -DTAUOLAPP_HEPMC2
endif
endif

libTauolaHepMC3Interface.so: $(TAUOLAINTERFACE)/src/TauolaHepMC3Event.o \
                             $(TAUOLAINTERFACE)/src/TauolaHepMC3Particle.o
	mkdir -p $(TAUOLAINTERFACE)/lib/
	$(LD) $(LDFLAGS) $(SOFLAGS) -o $(TAUOLAINTERFACE)/lib/$@ $^

#
# pythia8
#
PYTHIA8INTERFACE = $(INTERFACEDIRECTORY)/pythia8

ifneq ($(PYTHIA8LOCATION_HEPMC3), )
  override INTERFACES    += libpythia8tohepmc3.so
  override INCLUDES      += -I$(PYTHIA8LOCATION_HEPMC3)/include \
                            -I$(PYTHIA8INTERFACE)/include
  override RPATHS_HEPMC3 += -Wl,-rpath,$(PYTHIA8LOCATION_HEPMC3)/lib \
                            -Wl,-rpath,$(PYTHIA8INTERFACE)/lib
  override LINKS_HEPMC3  += -L$(PYTHIA8LOCATION_HEPMC3)/lib/archive -lpythia8 -llhapdfdummy \
                            -L$(PYTHIA8INTERFACE)/lib -lpythia8tohepmc3
  override DEFS_HEPMC3   += -DPYTHIA8
  override VALIDATION_SRC+= src/PythiaValidationTool.cc
ifneq ($(PYTHIA8LOCATION_HEPMC2), )
  override RPATHS_HEPMC2 += -Wl,-rpath,$(PYTHIA8LOCATION_HEPMC2)/lib
  override LINKS_HEPMC2  += -L$(PYTHIA8LOCATION_HEPMC2)/lib/archive -lpythia8 -llhapdfdummy \
                            -L$(PYTHIA8INTERFACE)/lib -lpythia8tohepmc
  override DEFS_HEPMC2   += -DPYTHIA8_HEPMC2
endif
endif

libpythia8tohepmc3.so: $(PYTHIA8INTERFACE)/src/Pythia8ToHepMC3.o
	mkdir -p $(PYTHIA8INTERFACE)/lib/
	$(LD) $(LDFLAGS) $(SOFLAGS) -o $(PYTHIA8INTERFACE)/lib/$@ $^

#
# MC-TESTER
#
MCTESTERINTERFACE = $(INTERFACEDIRECTORY)/mc-tester

ifneq ($(MCTESTERLOCATION_HEPMC3), )
  override INTERFACES    += libHepMC3Interface.so
  override INCLUDES      += -I$(MCTESTERLOCATION_HEPMC3)/include \
                            -I$(MCTESTERINTERFACE)/include \
                            -I$(shell root-config --incdir)
  override RPATHS_HEPMC3 += -Wl,-rpath,$(MCTESTERLOCATION_HEPMC3)/lib \
                            -Wl,-rpath,$(MCTESTERINTERFACE)/lib \
                            -Wl,-rpath,$(shell root-config --libdir)
  override LINKS_HEPMC3  += -L$(MCTESTERLOCATION_HEPMC3)/lib -lHEPEvent -lMCTester \
                            -L$(MCTESTERINTERFACE)/lib -lHepMC3Interface \
                            $(shell root-config --glibs)
  override DEFS_HEPMC3   += -DMCTESTER
  override VALIDATION_SRC+= src/McTesterValidationTool.cc
ifneq ($(MCTESTERLOCATION_HEPMC2), )
  override RPATHS_HEPMC2 += -Wl,-rpath,$(MCTESTERLOCATION_HEPMC2)/lib \
                            -Wl,-rpath,$(shell root-config --libdir)
  override LINKS_HEPMC2  += -L$(MCTESTERLOCATION_HEPMC2)/lib -lHEPEvent -lMCTester -lHepMCEvent \
                            $(shell root-config --glibs)
  override DEFS_HEPMC2   += -DMCTESTER_HEPMC2
endif
endif

libHepMC3Interface.so: $(MCTESTERINTERFACE)/src/HepMC3Event.o \
                       $(MCTESTERINTERFACE)/src/HepMC3Particle.o
	mkdir -p $(MCTESTERINTERFACE)/lib/
	$(LD) $(LDFLAGS) $(SOFLAGS) -o $(MCTESTERINTERFACE)/lib/$@ $^
