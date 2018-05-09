#!/bin/bash   
FILE1=$1 #first generation step file
FILE2=$2 #second generation step file

MCTESTER_DIR=~/mc-tester-1.25.0 #location of MC-TESTER
export LD_LIBRARY_PATH=${MCTESTER_DIR}/lib

MCTESTER_ANALYZE_DIR=${MCTESTER_DIR}/analyze
export MC_TESTER_LIBS_DIR=${MCTESTER_DIR}/lib

WORKING_DIR=`pwd`

#change to MCTester directory and run macros
mkdir -p /tmp/mc-tester
cp SETUP.C /tmp/mc-tester/.
cd $MCTESTER_ANALYZE_DIR 
root -b -q "ANALYZE.C(\"/tmp/mc-tester\",\"${WORKING_DIR}/${FILE1}\",\"${WORKING_DIR}/${FILE2}\")" 
root -b -q "BOOKLET.C(\"/tmp/mc-tester\")"
cp tester.tex /tmp/mc-tester

cd /tmp/mc-tester
latex tester.tex
latex tester.tex
dvipdf tester.dvi
cp tester.pdf $WORKING_DIR

cd $WORKING_DIR

