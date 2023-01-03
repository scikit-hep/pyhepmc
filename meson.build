project('pyhepmc', 'cpp',
        version: '2.9.x',
        default_options: ['cpp_std=c++14'])

cmake = import('cmake')
python = import('python')

accessor = dependency('cpp-member-accessor')
mp11 = cmake.subproject('mp11').dependency('boost_mp11')
pybind11 = dependency('pybind11')
hepmc3 = dependency('hepmc3')

compiler = meson.get_compiler('cpp')

if compiler.get_argument_syntax() == 'gcc'
    add_project_arguments('-Wno-self-assign-overloaded', language: 'cpp')
endif

src = files([
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

py = python.find_installation('python3')

py.extension_module(
    'pyhepmc', src,
    dependencies: [
        pybind11,
        mp11,
        hepmc3,
        accessor,
    ],
)
