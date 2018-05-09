cmake_minimum_required(VERSION 2.8.9 FATAL_ERROR)
#----------------------------------------------------------------------------
project(HepMC)
set(PROJECT_VERSION 3)
#---Enable FORTRAN (unfortunatelly is not not possible in all cases)-------------------------------
if(NOT CMAKE_GENERATOR STREQUAL Xcode)
  enable_language(Fortran OPTIONAL)
endif()


set(CMAKE_VERBOSE_MAKEFILE ON)

#---Setting HepMC Build type-----------------------------------------------
if(CMAKE_BUILD_TYPE)
  message(STATUS "HepMC3 Build type: ${CMAKE_BUILD_TYPE}")
else(CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release")
  message(STATUS "HepMC3 Build type not specified, use: ${CMAKE_BUILD_TYPE}")
endif(CMAKE_BUILD_TYPE)

string(TOUPPER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE)

#-------------Options-------------------------------------------------------

option(HEPMC_ENABLE_ROOTIO "Enables building with ROOT O/I." ON)
option(HEPMC_BUILD_EXAMPLES "Enables building of examples." OFF)
option(HEPMC_INSTALL_INTERFACES "Enables installation of HepMC3 interfaces." OFF)


message(STATUS "HepMC: HEPMC_ENABLE_ROOTIO         ${HEPMC_ENABLE_ROOTIO}") 
message(STATUS "HepMC: HEPMC_BUILD_EXAMPLES        ${HEPMC_BUILD_EXAMPLES}") 
message(STATUS "HepMC: HEPMC_INSTALL_INTERFACES    ${HEPMC_INSTALL_INTERFACES}")

if(HEPMC_ENABLE_ROOTIO)
  if( EXISTS "$ENV{ROOTSYS}" )
    message(STATUS "HepMC: ROOTSYS provided $ENV{ROOTSYS}")
  elseif(ROOT_DIR)
    message(STATUS "HepMC: ROOT_DIR provided ${ROOT_DIR}")
  else() 
    message(STATUS "HepMC warning: Building of ROOTIO requested but no ROOTSYS or ROOT_DIR provided")
    message(STATUS "HepMC warning: Build will use ROOTConfig.cmake or FindROOT.cmake")
  endif()
endif()

# - Prepend our own CMake Modules to the search path
# This allows us to customize, add, and factor out functionality
# NB: if our custom modules include others that we don't supply, those in the
# base path will be used, so watch for incompatibilities!!
#
set(CMAKE_MODULE_PATH
    ${PROJECT_SOURCE_DIR}/cmake/Modules
    ${CMAKE_MODULE_PATH})

#---Compilation and Link options---------------------------------------------

if(CMAKE_SYSTEM_NAME MATCHES Darwin)
  set(CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS "${CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS} -flat_namespace -single_module -undefined dynamic_lookup")
endif()

set(CMAKE_CXX_FLAGS                "${CMAKE_CXX_FLAGS} -fPIC")
set(CMAKE_CXX_FLAGS_DEBUG          "-g3 -Wall")
set(CMAKE_CXX_FLAGS_MINSIZEREL     "-Os -DNDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE        "-O2 -DNDEBUG")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-g3 -O2")

# fortran flags needed for some tests and examples

# FFLAGS depend on the compiler
get_filename_component (Fortran_COMPILER_NAME ${CMAKE_Fortran_COMPILER} NAME)
if ("${CMAKE_Fortran_FLAGS}" STREQUAL "" )
if (Fortran_COMPILER_NAME MATCHES "gfortran.*")
   set(CMAKE_Fortran_FLAGS            "-fno-automatic -fno-backslash -ffixed-line-length-132")
elseif (Fortran_COMPILER_NAME MATCHES "ifort.*")
   set(CMAKE_Fortran_FLAGS            "-fno-automatic -fno-backslash -extend-source 132")	
endif()
message(STATUS "Fortran compiler : ${Fortran_COMPILER_NAME}")
elseif()

endif()

# setting linker flags

IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin") 
  SET(CMAKE_EXE_LINKER_FLAGS "-Wl,-dead_strip_dylibs")
  SET(CMAKE_SHARED_LINKER_FLAGS "-Wl,-dead_strip_dylibs") 
  SET(STATIC_LIBRARY_FLAGS "-Wl,-dead_strip_dylibs")
ELSEIF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  SET(CMAKE_EXE_LINKER_FLAGS "-Wl,--as-needed")
  SET(CMAKE_SHARED_LINKER_FLAGS "-Wl,--as-needed")
  SET(STATIC_LIBRARY_FLAGS "-Wl,--as-needed")	
ENDIF()

#----------------------------------------------------------------------------


include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support.")
endif()

message(STATUS "HepMC: Fortran FLAGS ${CMAKE_Fortran_FLAGS}")
message(STATUS "HepMC: CXX FLAGS ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${CMAKE_BUILD_TYPE}}  " )


#This module respects HFS, e.g. defines lib or lib64 when it is needed. 
include("GNUInstallDirs")
#### RPATH handling #####

set(CMAKE_MACOSX_RPATH 1)

# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 

SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}")

# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# the RPATH to be used when installing, but only if it's not a system directory
LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}" isSystemDir)
IF("${isSystemDir}" STREQUAL "-1")
   SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}")
ENDIF("${isSystemDir}" STREQUAL "-1")


#---Optional build of rootIO-------------------------------------------------

if(HEPMC_ENABLE_ROOTIO)
  set (ROOT_FIND_COMPONENTS Core RIO Tree)
  list(APPEND CMAKE_PREFIX_PATH $ENV{ROOTSYS})
  list(APPEND CMAKE_PREFIX_PATH ${ROOT_DIR})
  find_package(ROOT REQUIRED COMPONENTS Core RIO Tree)
  message(STATUS "ROOT_USE_FILE ${ROOT_USE_FILE}")
  include(${ROOT_USE_FILE})

  message(STATUS "ROOT includes: ${ROOT_INCLUDE_DIRS}")
  message(STATUS "ROOT libraries: ${ROOT_LIBRARIES}")
  message(STATUS "ROOT_FOUND: ${ROOT_FOUND}")

  if(ROOT_FOUND)
    include_directories(${ROOT_INCLUDE_DIRS})
    add_definitions(-DHEPMC_ROOTIO)
    set(HEPMC_ROOTIO_LIBRARY "-lHepMCrootIO" )
  else()
    message(STATUS "HepMC warning: ROOT needed for ROOTIO but not found")
    message(STATUS "HepMC warning: Skipping HepMC ROOT IO libraries")
    set(HEPMC_ENABLE_ROOTIO OFF)
  endif()
endif()


#---Select sources for the various libraries---------------------------------
file(GLOB hepmc3_sources ${PROJECT_SOURCE_DIR}/src/*.cc ${PROJECT_SOURCE_DIR}/src/Search/*.cc)

add_library(objlib OBJECT ${hepmc3_sources})
include_directories(include)
# shared libraries need PIC:
set_property(TARGET ${objlib} PROPERTY POSITION_INDEPENDENT_CODE 1)

add_library(HepMC SHARED $<TARGET_OBJECTS:objlib>)
add_library(HepMC_static STATIC $<TARGET_OBJECTS:objlib>)

configure_file(HepMC-config.in  ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/HepMC-config )

#SET_TARGET_PROPERTIES(... PROPERTIES LINK_FLAGS "$ENV{MYLDFLAGS}")


set_target_properties(HepMC PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_LIBDIR})
set_target_properties(HepMC_static PROPERTIES OUTPUT_NAME HepMC ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_LIBDIR})

#---Install build products---------------------------------------------------
install(TARGETS HepMC DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT libs)
install(TARGETS HepMC_static DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT libs)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR} COMPONENT devel)

if (HEPMC_INSTALL_INTERFACES)
  install(DIRECTORY interfaces DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/../ COMPONENT devel)
endif()

install(FILES  ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/HepMC-config  DESTINATION  ${CMAKE_INSTALL_BINDIR} COMPONENT libs)

if(ROOT_FOUND)
   add_subdirectory(rootIO)
endif()
# Add the examples subdirectories

if(HEPMC_BUILD_EXAMPLES)
  set(HepMC_DIR ${CMAKE_BINARY_DIR} CACHE PATH "Current build directory")
  add_subdirectory(examples)
endif()

add_custom_target(move_headers ALL ${CMAKE_COMMAND} -DPREFIX=${CMAKE_BINARY_DIR}/outputs
                                   -DCOMPONENTS="devel"
                                   -P ${CMAKE_SOURCE_DIR}/cmake/Modules/local_install.cmake )

#------------------------------------------------------------------------------
# Add the validation subdirectories
if(HEPMC_ENABLE_VALIDATION)
  add_subdirectory(validation)
endif()


# Generate config CMake files to be used by other projects
#

include(CMakePackageConfigHelpers)

set(INCLUDE_INSTALL_DIR include )
set(LIB_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR})
set(CONFIG_INSTALL_DIR share/HepMC/cmake )

configure_package_config_file(cmake/Templates/HepMCConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/outputs/share/HepMC/cmake/HepMCConfig.cmake
                                 INSTALL_DESTINATION ${CONFIG_INSTALL_DIR}
                                 PATH_VARS INCLUDE_INSTALL_DIR LIB_INSTALL_DIR)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/outputs/share/HepMC/cmake/HepMCConfig.cmake 
           DESTINATION ${CONFIG_INSTALL_DIR} COMPONENT devel)

if(HEPMC_BUILD_EXAMPLES)
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/
           DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT examples)
endif()

#General CPACK settings
INCLUDE(InstallRequiredSystemLibraries)
set(CPACK_PACKAGE_NAME "HepMC")
set(CPACK_PACKAGE_VENDOR "HepMC Developers")
#Should the version be defined above?
set(CPACK_PACKAGE_VERSION 3)
set(CPACK_PACKAGE_VERSION_MAJOR 3)
set(CPACK_PACKAGE_VERSION_MINOR 0)
set(CPACK_PACKAGE_VERSION_PATCH 0)
set(CPACK_PACKAGE_RELEASE 0)
set(CPACK_PACKAGE_FILE_NAME "HepMC")
set(CPACK_PACKAGE_DESCRIPTION "Event record library for high energy physics Monte Carlo")

set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
SET(CPACK_INSTALL_PREFIX "/usr")
SET(CPACK_OUTPUT_FILE_PREFIX binpackages)


SET(CPACK_BINARY_RPM "ON")
#RPM-specific settings
set(CPACK_RPM_PACKAGE_DEBUG ON)
set(CPACK_RPM_PACKAGE_NAME "HepMC")
set(CPACK_RPM_COMPONENT_INSTALL ON)
set(CPACK_RPM_PACKAGE_LICENSE "GPL")
set(CPACK_RPM_PACKAGE_GROUP "General")
set(CPACK_RPM_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}-${CPACK_PACKAGE_RELEASE}")
set(CPACK_RPM_libs_PACKAGE_SUMMARY  "HepMC libraries")
set(CPACK_RPM_devel_PACKAGE_SUMMARY "Headers for HepMC libraries")
set(CPACK_RPM_examples_PACKAGE_SUMMARY "Examples for HepMC library")
set(CPACK_RPM_libs_PACKAGE_DESCRIPTION  ${CPACK_PACKAGE_DESCRIPTION})
set(CPACK_RPM_devel_PACKAGE_DESCRIPTION ${CPACK_PACKAGE_DESCRIPTION})
set(CPACK_RPM_examples_PACKAGE_DESCRIPTION ${CPACK_PACKAGE_DESCRIPTION})
set(CPACK_RPM_devel_PACKAGE_REQUIRES "${CPACK_RPM_PACKAGE_NAME}-libs")
set(CPACK_RPM_examples_PACKAGE_REQUIRES "${CPACK_RPM_PACKAGE_NAME}-libs" "${CPACK_RPM_PACKAGE_NAME}-rootIO-libs")
#Everything that goes before  HepMC , i.e. top level directories,should be excluded
#This feature is working fine only in the recent CPackRPM module -- see cmake/modules directory.
set(CPACK_RPM_EXCLUDE_FROM_AUTO_FILELIST_ADDITION ${CPACK_PACKAGING_INSTALL_PREFIX} ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}  ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}  ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR} )



SET(CPACK_BINARY_DEB "ON")
#DEB-specific settings
set(CPACK_DEBIAN_PACKAGE_NAME "HepMC")
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_DEBIAN_PACKAGE_LICENSE "GPL")
set(CPACK_DEBIAN_PACKAGE_GROUP "General")
set(CPACK_DEBIAN_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}-${CPACK_PACKAGE_RELEASE}")
set(CPACK_DEBIAN_devel_PACKAGE_DEPENDS "${CPACK_DEBIAN_PACKAGE_NAME}-libs")
set(CPACK_DEBIAN_examples_PACKAGE_DEPENDS "${CPACK_DEBIAN_PACKAGE_NAME}-libs" "${CPACK_DEBIAN_PACKAGE_NAME}-rootIO-libs")
set(CPACK_DEBIAN_EXCLUDE_FROM_AUTO_FILELIST_ADDITION ${CPACK_PACKAGING_INSTALL_PREFIX} ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}  ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}  ${CPACK_PACKAGING_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR} )
SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "HepMC Developers")


if(ROOT_FOUND)
set(CPACK_COMPONENTS_ALL   devel libs rootIO-devel rootIO-libs examples)
set(CPACK_RPM_rootIO-libs_PACKAGE_SUMMARY  "HepMC libraries with ROOT I/O support")
set(CPACK_RPM_rootIO-devel_PACKAGE_SUMMARY "Headers for HepMC libraries with ROOT I/O support")
set(CPACK_RPM_rootIO-libs_PACKAGE_DESCRIPTION  ${CPACK_PACKAGE_DESCRIPTION})
set(CPACK_RPM_rootIO-devel_PACKAGE_DESCRIPTION ${CPACK_PACKAGE_DESCRIPTION})
set(CPACK_RPM_rootIO-libs_PACKAGE_REQUIRES   "root, ${CPACK_RPM_PACKAGE_NAME}-libs")
set(CPACK_RPM_rootIO-devel_PACKAGE_REQUIRES   "${CPACK_RPM_PACKAGE_NAME}-devel, ${CPACK_RPM_PACKAGE_NAME}-rootIO-libs")
SET(CPACK_DEBIAN_rootIO-libs_PACKAGE_DEPENDS "libroot, ${CPACK_DEBIAN_PACKAGE_NAME}-libs")
SET(CPACK_DEBIAN_rootIO-devel_PACKAGE_DEPENDS "${CPACK_DEBIAN_PACKAGE_NAME}-devel, ${CPACK_DEBIAN_PACKAGE_NAME}-rootIO-libs")
else()
set(CPACK_COMPONENTS_ALL   devel libs)
endif()
INCLUDE(CPack)
