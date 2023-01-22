cmake_minimum_required(VERSION 3.13...3.17)

include(CMakePrintHelpers)

find_program(ccache_executable ccache)
if(ccache_executable)
  message(STATUS "Using ccache: ${ccache_executable}")
  set(CMAKE_CXX_COMPILER_LAUNCHER ${ccache_executable})
endif()

find_program(mold_executable mold)
find_program(
  gxx_executable
  NAMES g++-20
        g++-19
        g++-18
        g++-17
        g++-16
        g++-15
        g++-14
        g++-13
        g++-12
        g++-11
        g++-10
        g++-9
        g++-8)
if(mold_executable AND gxx_executable)
  message(STATUS "Using mold: ${mold_executable}")
  add_compile_options(-fuse-ld=mold)
  set(CMAKE_CXX_COMPILER ${gxx_executable})
endif()

project(pyhepmc LANGUAGES CXX)

if(GCC)
  # HepMC3 uses reinterpret_cast instead of const_cast
  add_compile_options(-Wno-strict-aliasing)
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

cmake_print_variables(CMAKE_BUILD_TYPE)

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
