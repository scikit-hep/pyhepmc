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
file(GLOB HEPMC3_SOURCES "extern/HepMC3/src/*.cc")

# pyhepmc falls under Section 5 "Combined Libraries" of the LGPL-v3. Since we
# satisfy a) and b), we do not need to compile the code into a separate library.
pybind11_add_module(_core MODULE ${SOURCES} ${HEPMC3_SOURCES})
target_include_directories(_core PRIVATE extern/cpp-member-accessor/include)
target_include_directories(_core PRIVATE extern/mp11/include)
target_include_directories(_core PRIVATE extern/HepMC3/include)
target_compile_definitions(_core PRIVATE HepMC3_EXPORTS=1)

if(MSVC)
  target_compile_options(_core PRIVATE /bigobj)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
else()
  target_compile_options(_core PRIVATE -Wall -Wno-self-assign-overloaded)
endif()
