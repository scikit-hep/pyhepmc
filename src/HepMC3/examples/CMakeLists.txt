# building examples
#------------------
cmake_minimum_required(VERSION 2.8.9 FATAL_ERROR)
include_directories(${PROJECT_SOURCE_DIR}/include )

include(CheckLanguage)
check_language(Fortran)
if (CMAKE_Fortran_COMPILER)
enable_language(Fortran)
get_filename_component (Fortran_COMPILER_NAME ${CMAKE_Fortran_COMPILER} NAME)
message(STATUS "Fortran compiler : ${Fortran_COMPILER_NAME}")
if (CMAKE_Fortran_COMPILER_ID STREQUAL "GNU")
set( CMAKE_Fortran_FLAGS  "${CMAKE_Fortran_FLAGS} -fno-automatic -fno-backslash -ffixed-line-length-132")
elseif (CMAKE_Fortran_COMPILER_ID STREQUAL "Intel")
set( CMAKE_Fortran_FLAGS  "${CMAKE_Fortran_FLAGS} -fno-automatic -fno-backslash -extend-source 132")
elseif()
message(STATUS "HepMC: Don't know how to set Fortran FLAGS for  ${Fortran_COMPILER_NAME} with ID ${Fortran_COMPILER_ID}")
endif ()
if(CMAKE_SYSTEM_NAME MATCHES Darwin)
  set(CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS "${CMAKE_SHARED_LIBRARY_CREATE_Fortran_FLAGS} -flat_namespace -single_module -undefined dynamic_lookup")
else()
endif()
message(STATUS "HepMC: Fortran FLAGS ${CMAKE_Fortran_FLAGS}")
add_subdirectory(Pythia6Example)
else()
message(STATUS "HepMC: Fortran compiler not found")
endif()



add_subdirectory(BasicExamples)

add_subdirectory(LHEFExample)

add_subdirectory(ConvertExample)

set(PYTHIA8_ROOT_DIR "" CACHE PATH "Location of Pythia8 installation.")
find_package(Pythia8 QUIET)

if(PYTHIA8_FOUND)
  add_subdirectory(Pythia8Example)
else()
  message(STATUS "Examples: Pythia8 package not found. Please check if PYTHIA8_ROOT_DIR is set properly.")
  message(STATUS "pythia8_example disabled")
endif()

if(ROOT_FOUND)
  add_subdirectory(RootIOExample)
  add_subdirectory(RootIOExample2)
  add_subdirectory(RootIOExample3)
else()
  message(STATUS "Examples: ROOT package not found. ")
  message(STATUS "rootIO_example disabled")
endif()
