project('pyhepmc', 'cpp',
        license: 'BSD-3',
        version: '2.9.x',
        default_options: ['cpp_std=c++14'])

cmake = import('cmake')

accessor = dependency('cpp-member-accessor')
mp11 = cmake.subproject('mp11').dependency('boost_mp11')
pybind11 = dependency('pybind11')
hepmc3 = dependency('hepmc3')

cpp = meson.get_compiler('cpp')

add_project_arguments(
    cpp.get_supported_arguments('-Wno-self-assign-overloaded'),
    language: 'cpp'
)

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

py = import('python').find_installation()

core = py.extension_module(
    '_core', src,
    dependencies: [
        pybind11,
        mp11,
        hepmc3,
        accessor,
    ],
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
