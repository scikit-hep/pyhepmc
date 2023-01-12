project(
    'pyhepmc', 'cpp',
    license: 'BSD-3',
    default_options: [
        'cpp_std=c++14',
        # for release mode
        # 'b_lto=true',
        # 'b_lto_mode=thin',
    ]
)

accessor = dependency('cpp-member-accessor')
mp11 = dependency('boost-mp11')
# hepmc3 = dependency('hepmc3', static:true).as_link_whole()

py = import('python').find_installation(pure: false)

# pybind11 include directory - needed in several submodules.
# We have to use get_pybind11_include to work around a stupid
# Meson restriction when installing from a venv created inside
# the project directory.
incdir_pybind11 = run_command(py,
    ['get_pybind11_include.py'],
    check: true
).stdout().strip()

inc_pybind11 = include_directories(incdir_pybind11)

cpp = meson.get_compiler('cpp')

inc_hepmc3 = include_directories('extern/HepMC3/include')

src_hepmc3 = files([
    'extern/HepMC3/src/GenCrossSection.cc',
    'extern/HepMC3/src/GenEvent.cc',
    'extern/HepMC3/src/GenHeavyIon.cc',
    'extern/HepMC3/src/GenParticle.cc',
    'extern/HepMC3/src/GenPdfInfo.cc',
    'extern/HepMC3/src/GenRunInfo.cc',
    'extern/HepMC3/src/GenVertex.cc',
    'extern/HepMC3/src/HEPEVT_Wrapper.cc',
    'extern/HepMC3/src/LHEFAttributes.cc',
    'extern/HepMC3/src/Print.cc',
    'extern/HepMC3/src/ReaderAscii.cc',
    'extern/HepMC3/src/ReaderAsciiHepMC2.cc',
    'extern/HepMC3/src/ReaderHEPEVT.cc',
    'extern/HepMC3/src/ReaderLHEF.cc',
    'extern/HepMC3/src/ReaderPlugin.cc',
    'extern/HepMC3/src/Setup.cc',
    'extern/HepMC3/src/WriterAscii.cc',
    'extern/HepMC3/src/WriterAsciiHepMC2.cc',
    'extern/HepMC3/src/WriterHEPEVT.cc',
    'extern/HepMC3/src/WriterPlugin.cc',
])

hepmc3 = static_library('hepmc3', src_hepmc3,
    include_directories: inc_hepmc3,
    cpp_args: ['-DHepMC3_EXPORTS=1'] + cpp.get_supported_arguments(
        '-Wno-deprecated-declarations',
        '-Wno-strict-aliasing',
    ),
)

src_core = files([
    'src/attribute_conversion.cpp',
    'src/attributes_view.cpp',
    'src/core.cpp',
    'src/crosssection_patches.cpp',
    'src/equal.cpp',
    'src/from_hepevt.cpp',
    'src/io.cpp',
    'src/pyiostream.cpp',
    'src/repr.cpp',
    'src/runinfo_attributes_view.cpp',
])

py.extension_module(
    '_core', src_core,
    include_directories: [inc_pybind11, inc_hepmc3],
    dependencies: [
        mp11,
        accessor,
    ],
    link_whole: hepmc3,
    cpp_args: cpp.get_supported_arguments('-Wno-self-assign-overloaded'),
    subdir: 'pyhepmc',
    install: true
)

py.install_sources(
    'src/pyhepmc/__init__.py',
    'src/pyhepmc/_attributes.py',
    'src/pyhepmc/_autodoc.py',
    'src/pyhepmc/_deprecated.py',
    'src/pyhepmc/_doc.py',
    'src/pyhepmc/_graphviz.py',
    'src/pyhepmc/_prettify.py',
    'src/pyhepmc/_setup.py',
    'src/pyhepmc/io.py',
    'src/pyhepmc/view.py',
    subdir: 'pyhepmc'
)
