cmake_minimum_required(VERSION 3.13...3.17)
cmake_policy(CMP0077 NEW)

project(pyhepmc LANGUAGES CXX)

if(NOT CMAKE_LIBRARY_OUTPUT_DIRECTORY)
  message(
    WARNING
      "You should call this through setup.py so that all variables are set; python setup.py build_ext --inplace"
  )
endif()

set(CMAKE_CXX_STANDARD
    11
    CACHE STRING "C++ version selection") 
set(CMAKE_CXX_STANDARD_REQUIRED ON) # optional, ensure standard is supported
set(CMAKE_CXX_EXTENSIONS OFF) # optional, keep compiler extensionsn off

# Now we can find pybind11
option(EXTERNAL_PYBIND11 "Build against an external pybind11" OFF)
if(EXTERNAL_PYBIND11)
  find_package(pybind11 CONFIG REQUIRED)
else()
  add_subdirectory(extern/pybind11)
endif()

option(HEPMC3_ENABLE_ROOTIO OFF)
option(HEPMC3_ENABLE_PYTHON OFF)
add_subdirectory(extern/HepMC3)

file(GLOB SOURCES_A "src/*.cpp")

pybind11_add_module(_core MODULE ${SOURCES_A})
# target_include_directories(_core PRIVATE extern/HepMC3/include)
target_link_libraries(_core PRIVATE HepMC3)

if(MSVC)
  target_compile_options(_core PRIVATE /std:c++14 /Y-)
else()
  # ignore warnings raised by HepMC3 code
  target_compile_options(_core PRIVATE
        -fvisibility=hidden
        -Wall
        -Wno-strict-aliasing
        -Wno-sign-compare
        -Wno-reorder
        -Wno-self-assign-overloaded
        -Wno-unused-private-field
        -Wno-unused-value
  )
endif()
set_target_properties(_core PROPERTIES VISIBILITY_INLINES_HIDDEN ON)
target_compile_definitions(_core PRIVATE HEPMC3_HEPEVT_NMXHEP=100000)