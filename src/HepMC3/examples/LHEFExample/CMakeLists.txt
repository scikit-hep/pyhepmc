
include_directories(${PROJECT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(LHEF_example_cat.exe ${CMAKE_CURRENT_SOURCE_DIR}/LHEF_example_cat.cc)
target_link_libraries(LHEF_example_cat.exe HepMC ${ROOT_LIBRARIES})
set_target_properties(LHEF_example_cat.exe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR})

# create environment scripts

set(bindir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}")
set(libdir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}")
 
configure_file(
${CMAKE_SOURCE_DIR}/examples/LHEFExample/LHEF_example_env.sh.in
	    ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/LHEF_example_env.sh
     	     @ONLY
      	     )

# installs 

install(TARGETS LHEF_example_cat.exe DESTINATION ${CMAKE_INSTALL_BINDIR})
install(FILES LHEF_example.lhe LHEF_example_cmp.lhe DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY ${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_BINDIR}/ DESTINATION ${CMAKE_INSTALL_BINDIR}
        FILES_MATCHING PATTERN "*.sh")
