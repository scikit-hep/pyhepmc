project(
    'HepMC3', 'cpp',
    version: '3.2.5-38-g591bccc',
    license: 'LGPLv3')

inc = include_directories('include')

src = files([
    'src/GenCrossSection.cc',
    'src/GenEvent.cc',
    'src/GenHeavyIon.cc',
    'src/GenParticle.cc',
    'src/GenPdfInfo.cc',
    'src/GenRunInfo.cc',
    'src/GenVertex.cc',
    'src/HEPEVT_Wrapper.cc',
    'src/LHEFAttributes.cc',
    'src/Print.cc',
    'src/ReaderAscii.cc',
    'src/ReaderAsciiHepMC2.cc',
    'src/ReaderHEPEVT.cc',
    'src/ReaderLHEF.cc',
    'src/ReaderPlugin.cc',
    'src/Setup.cc',
    'src/WriterAscii.cc',
    'src/WriterAsciiHepMC2.cc',
    'src/WriterHEPEVT.cc',
    'src/WriterPlugin.cc',
])

library('hepmc3', src,
    include_directories: inc
)

hepmc3_dep = declare_dependency(
    include_directories: inc,
    compile_args: '-DHepMC3_EXPORTS=1'
)
