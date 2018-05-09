#--------
#-root IO

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR} ${ROOT_INCLUDE_DIRS})

#----------------------------------------------------------------------------
# Generate dictionaries
#
ROOT_GENERATE_DICTIONARY(rootIO_Classes include/rootIO_Classes.hh LINKDEF include/LinkDef.hh OPTIONS -inlineInputHeader)

add_library(HepMCrootIO SHARED ${PROJECT_SOURCE_DIR}/rootIO/src/WriterRoot.cc ${PROJECT_SOURCE_DIR}/rootIO/src/ReaderRoot.cc ${PROJECT_SOURCE_DIR}/rootIO/src/WriterRootTree.cc ${PROJECT_SOURCE_DIR}/rootIO/src/ReaderRootTree.cc ${PROJECT_SOURCE_DIR}/rootIO/src/Streamers.cc rootIO_Classes.cxx)

target_link_libraries(HepMCrootIO ${ROOT_LIBRARIES} HepMC)
set_target_properties(HepMCrootIO PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_LIBDIR})


# installs 
install(TARGETS HepMCrootIO DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT rootIO-libs)
install(DIRECTORY ${PROJECT_BINARY_DIR}/rootIO/ DESTINATION  ${CMAKE_INSTALL_LIBDIR}  COMPONENT rootIO-libs  FILES_MATCHING PATTERN "*.pcm" PATTERN "CMakeFiles"  EXCLUDE  PATTERN "src"  EXCLUDE PATTERN "include"  EXCLUDE)
install(DIRECTORY include/HepMC DESTINATION ${CMAKE_INSTALL_INCLUDEDIR} COMPONENT rootIO-devel)
add_custom_target(move_rootIO_headers ALL ${CMAKE_COMMAND} -DPREFIX=${CMAKE_BINARY_DIR}/outputs
                                   -DCOMPONENTS="rootIO-devel"
                                   -P ${CMAKE_SOURCE_DIR}/cmake/Modules/local_install.cmake )
