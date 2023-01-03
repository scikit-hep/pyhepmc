project(
    'HepMC3', 'cpp',
    version: '3.2.5-38-g591bccc',
    license: 'LGPLv3',
    default_options: ['cpp_std=c++14']
)

compiler = meson.get_compiler('cpp')

if compiler.get_argument_syntax() == 'gcc'
    add_project_arguments('-Wno-deprecated-declarations', language: 'cpp')
endif

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

lib = library('hepmc3', src,
    include_directories: inc,
    cpp_args: '-DHepMC3_EXPORTS=1'
)

hepmc3_dep = declare_dependency(
    include_directories: inc,
    link_with: lib,
    compile_args: '-DHepMC3_EXPORTS=1'
)
