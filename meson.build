project('pyhepmc', 'cpp',
        default_options : ['cpp_std=c++14'])

# cmake = import('cmake')
python = import('python')

pybind11 = dependency('pybind11')

py = python.find_installation('python3')

src = files(['src/core.cpp'])

py.extension_module(
    'pyhepmc', src,
    dependencies: pybind11
)
