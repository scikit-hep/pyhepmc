# building examples
#------------------
cmake_minimum_required(VERSION 2.8.9 FATAL_ERROR)
#

find_package(HepMC2 QUIET)

if(NOT HEPMC2_FOUND)
  message(STATUS "Validation: HEPMC2 package not found. Please check if HEPMC2_ROOT_DIR is set properly.") 
endif()

find_package(Pythia8 QUIET)

if(NOT PYTHIA8_FOUND)
  message(STATUS "Validation: Pythia8 package not found. Please check if PYTHIA8_ROOT_DIR is set properly.") 
endif()


set(PHOTOSPP_ROOT_DIR ${PHOTOSPP_HEPMC3_ROOT_DIR}) 
find_package(Photospp QUIET)

if(NOT PHOTOSPP_FOUND)
  message(STATUS "Validation: Photos package not found. Please check if PHOTOSPP_HEPMC3_ROOT_DIR is set properly.") 
else()
  set(PHOTOSPP_HEPMC3_LIBRARIES ${PHOTOSPP_LIBRARIES})
  set(PHOTOSPP_HEPMC3_INCLUDE_DIRS ${PHOTOSPP_INCLUDE_DIRS})
endif()

message(STATUS "PHOTOSPP_HEPMC3_LIBRARIES ${PHOTOSPP_HEPMC3_LIBRARIES}")
message(STATUS "PHOTOSPP_HEPMC3_INCLUDE_DIRS ${PHOTOSPP_HEPMC3_INCLUDE_DIRS}")

set(PHOTOSPP_ROOT_DIR ${PHOTOSPP_HEPMC2_ROOT_DIR})
find_package(Photospp QUIET)
if(NOT PHOTOSPP_FOUND)
  message(STATUS "Validation: PhotosHepMC2 package not found. Please check if PHOTOSPP_HEPMC2_ROOT_DIR is set properly.") 
else()
  set(PHOTOSPP_HEPMC2_LIBRARIES ${PHOTOSPP_LIBRARIES})
  set(PHOTOSPP_HEPMC2_INCLUDE_DIRS ${PHOTOSPP_INCLUDE_DIRS})
endif()


message(STATUS "PHOTOSPP_HEPMC2_LIBRARIES ${PHOTOSPP_HEPMC2_LIBRARIES}")
message(STATUS "PHOTOSPP_HEPMC2_INCLUDE_DIRS ${PHOTOSPP_HEPMC2_INCLUDE_DIRS}")


# validation with HepMC3

#add_executable(validation.exe ${PROJECT_SOURCE_DIR}/validation/validation.cc ${CMAKE_CURRENT_SOURCE_DIR} src/ValidationControl.cc ${CMAKE_CURRENT_SOURCE_DIR}/src/SimpleEventTool.cc ${CMAKE_CURRENT_SOURCE_DIR}/src/FileValidationTool.cc )
#target_include_directories(validation.exe PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include ${PROJECT_SOURCE_DIR}/include ${PHOTOSPP_HEPMC3_INCLUDE_DIRS})
#target_link_libraries(validation.exe HepMC ${PHOTOSPP_HEPMC3_LIBRARIES} )
#set_target_properties(validation.exe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/bin)

# validation with HepMC2
add_definitions(-DHEPMC2)
message(STATUS "HEPMC2_INCLUDE_DIRS ${HEPMC2_INCLUDE_DIRS}") 
add_executable(validation_HEPMC2.exe
${PROJECT_SOURCE_DIR}/validation/validation.cc ${CMAKE_CURRENT_SOURCE_DIR}/src/ValidationControl.cc ${CMAKE_CURRENT_SOURCE_DIR}/src/SimpleEventTool.cc ${CMAKE_CURRENT_SOURCE_DIR}/src/FileValidationTool.cc )
target_include_directories(validation_HEPMC2.exe PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include  ${HEPMC2_INCLUDE_DIRS} ${PHOTOSPP_HEPMC2_INCLUDE_DIRS})
target_link_libraries(validation_HEPMC2.exe ${HEPMC2_LIBRARIES} ${PHOTOSPP_HEPMC2_LIBRARIES})
set_target_properties(validation_HEPMC2.exe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/bin)


