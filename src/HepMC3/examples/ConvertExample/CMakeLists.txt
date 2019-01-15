

if(ROOT_FOUND)
include_directories(${PROJECT_SOURCE_DIR}/rootIO/include ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR}  ${ROOT_INCLUDE_DIRS})

#----------------------------------------------------------------------------
# Generate dictionaries
#


add_executable(convert_example.exe
        ${CMAKE_CURRENT_SOURCE_DIR}/convert_example.cc
        ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.c
        ${CMAKE_CURRENT_SOURCE_DIR}/src/WriterRootTreeOPAL.cc 
        ${CMAKE_CURRENT_SOURCE_DIR}/src/WriterHEPEVTZEUS.cc )
target_link_libraries(convert_example.exe ${ROOT_LIBRARIES} HepMC HepMCrootIO)
set_target_properties(convert_example.exe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR})
target_compile_definitions(convert_example.exe PRIVATE HEPMCCONVERT_EXTENSION_ROOTTREEOPAL=1 HEPMCCONVERT_EXTENSION_HEPEVTZEUS=1)
add_dependencies( convert_example.exe dictionary )



# create environment scripts

set(bindir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}")
set(libdir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}:${ROOT_LIBRARY_DIR}")
else()
include_directories(${PROJECT_SOURCE_DIR}/rootIO/include ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR})
#----------------------------------------------------------------------------
# Generate dictionaries
#
add_executable(convert_example.exe
        ${CMAKE_CURRENT_SOURCE_DIR}/convert_example.cc
        ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.c
        ${CMAKE_CURRENT_SOURCE_DIR}/src/WriterHEPEVTZEUS.cc )
target_link_libraries(convert_example.exe HepMC )
set_target_properties(convert_example.exe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR})
target_compile_definitions(convert_example.exe PRIVATE  HEPMCCONVERT_EXTENSION_HEPEVTZEUS=1)
# create environment scripts
set(bindir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}")
set(libdir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}")
endif()
 
configure_file(
${CMAKE_SOURCE_DIR}/examples/ConvertExample/convert_example_env.sh.in
	    ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/convert_example_env.sh
     	     @ONLY
      	     )

# installs 
install(TARGETS convert_example.exe DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY ${PROJECT_BINARY_DIR}/examples/ConvertExample/ DESTINATION ${CMAKE_INSTALL_BINDIR} FILES_MATCHING PATTERN "*.pcm" PATTERN "CMakeFiles" EXCLUDE )
install(DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/ DESTINATION ${CMAKE_INSTALL_BINDIR}
        FILES_MATCHING PATTERN "*.sh")






#The cmdline.c and cmdline.h for this example are generated from file below
#gengetopt -N  --no-version --input=hepmcconvert.ggo --include-getopt --show-required -u"inputfile outputfile"
#version "3.1"
#package "hepmcconvert"
#purpose "Convert between different file formats of Monte Carlo event record.
#Example:
#         hepmcconvert -i hepmc2 -o treeroot input.hepmc output.root
#"
#option "input-format" i "Input format" string required values="hepmc2", "hepmc3", "hpe" ,"root", "treeroot","lhef"
#option "output-format" o "Output format" string required values="hepmc2", "hepmc3", "hpe" ,"root", "treeroot" ,"treerootopal","hpezeus", "dump"
#option "extensions" e "Extensions, in a form extension=value, could be passed to readers/writers" multiple optional string
#option "events-limit" - "Limit of events to read from input" optional long default="100000000"
#option "first-event-number" -       "Lowest allowed event number" optional long default="-100000000"
#option "last-event-number" -        "Highest allowed event number" optional long default="100000000"
#option "print-every-events-parsed" - "Frequency of parsing information printouts" optional long default="100"
