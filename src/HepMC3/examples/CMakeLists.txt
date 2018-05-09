# building examples
#------------------
cmake_minimum_required(VERSION 2.8.9 FATAL_ERROR)


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
