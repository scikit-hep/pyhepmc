cmake_minimum_required(VERSION 3.13...3.17)

project(pyhepmc LANGUAGES CXX)

if(NOT CMAKE_LIBRARY_OUTPUT_DIRECTORY)
  message(
    WARNING
      "You should call this through setup.py so that all variables are set; python setup.py build_ext --inplace"
  )
endif()

set(CMAKE_CXX_STANDARD
    14
    CACHE STRING "C++ version selection")
set(CMAKE_CXX_STANDARD_REQUIRED ON) # optional, ensure standard is supported
set(CMAKE_CXX_EXTENSIONS OFF) # optional, keep compiler extensions off

# Now we can find pybind11
option(EXTERNAL_PYBIND11 "Build against an external pybind11" OFF)
if(EXTERNAL_PYBIND11)
  find_package(pybind11 CONFIG REQUIRED)
else()
  add_subdirectory(extern/pybind11)
endif()

file(GLOB SOURCES "src/*.cpp")
file(GLOB SOURCES2 "extern/HepMC3/src/*.cc")

# To satisfy LGPL, we must compile all LGPL code into a library and then link to
# that library.
add_library(HepMC3 STATIC ${SOURCES2})
target_include_directories(HepMC3 PUBLIC extern/HepMC3/include)
set_target_properties(HepMC3 PROPERTIES VISIBILITY_INLINES_HIDDEN ON)

pybind11_add_module(_core MODULE ${SOURCES})
target_include_directories(_core PRIVATE extern/cpp-member-accessor/include)
target_include_directories(_core PRIVATE extern/mp11/include)
target_compile_definitions(_core PRIVATE HepMC3_EXPORTS=1)
target_link_libraries(_core PRIVATE HepMC3)
set_target_properties(_core PROPERTIES VISIBILITY_INLINES_HIDDEN ON)

if(MSVC)
  target_compile_options(_core PRIVATE /bigobj)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
else()
  target_compile_options(_core PRIVATE -Wall -Wno-self-assign-overloaded)
endif()
