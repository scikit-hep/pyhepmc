"""
pyhepmc-ng is a wrapper of the HepMC-v3 C++ library.

Another wrapper is [pyhepmc](https://pypi.org/project/pyhepmc/).
Why should you use this one?

**pyhepmc-ng is easy to install**

The command `pip install pyhepmc-ng` just works! You only need a compiler that
supports C++11, everything else is handled by pip.

Under the hood, the bindings are build with the excellent
[pybind11](http://pybind11.readthedocs.io/en/stable/) library.
pybind11 is automatically installed as a requirement by pip. You don't need an
external installation of the HepMC library, either. A copy of this
light-weight library is included.

**pyhepmc-ng is actively developed**

pyhepmc-ng is part of the Scikit-HEP project, which aims to provide all tools needed by particle physicists to do data analysis in Python.

**pyhepmc-ng is unit tested**

Everything in pyhepmc-ng is unit tested.

**pyhepmc-ng supports Pythonic code**

pyhepmc-ng is a hand-crafted mapping of C++ code to Python. It supports Python idioms
where appropriate.

- C++ methods which act like properties are represented as properties,
  e.g. GenParticle::set_status and GenParticle::status are mapped to a single
  GenParticle.status field in Python
- Tuples and lists are implicitly convertible to FourVectors
- ReaderAscii and WriterAscii support the context manager protocol

License: pyhepmc-ng is covered by the BSD license, but the license only
applies to the binding code. The HepMC3 code is covered by the GPL-v3 license.
"""
from __future__ import print_function
from setuptools import setup, Extension, find_packages
from distutils.command.build_ext import build_ext
from setuptools import distutils
import sys
import os
import glob

__version__ = '0.4.2'


class lazy_get_pybind_include:
    def __init__(self, user=False):
        self.user = user

    def __str__(self): # delay import of pybind11 until requirements are installed
        import pybind11
        return pybind11.get_include(self.user)


def lazy_compile(self, sources, output_dir=None, macros=None,
                 include_dirs=None, debug=0, extra_preargs=None,
                 extra_postargs=None, depends=None):
    macros, objects, extra_postargs, pp_opts, build = \
            self._setup_compile(output_dir, macros, include_dirs, sources,
                                depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)

    for obj in objects:
        try:
            src, ext = build[obj]
        except KeyError:
            continue
        if not os.path.exists(obj) or os.stat(obj).st_mtime < os.stat(src).st_mtime:
            self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
    return objects


import distutils.ccompiler
distutils.ccompiler.CCompiler.compile = lazy_compile


hepmc_source = glob.glob('src/HepMC3/src/*.cc') + glob.glob('src/HepMC3/src/Search/*.cc')
hepmc_include = 'src/HepMC3/include'
ext_modules = [
    Extension(
        'pyhepmc_ng.cpp',
        ['src/main.cpp'] + hepmc_source,
        include_dirs=[
            hepmc_include,
            'src',
            lazy_get_pybind_include(user=True),
            lazy_get_pybind_include(),
        ],
        language='c++'
    ),
]


def has_flag(compiler, flagname):
    import tempfile
    from distutils.errors import CompileError
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main() {}')
        try:
            print("testing flag: " + flagname)
            compiler.compile([f.name], extra_postargs=[flagname])
        except CompileError:
            return False
    return True


def flag_filter(compiler, *flags):
    key = " ".join((compiler.compiler[0],) + flags)
    import shelve
    sh = shelve.open(".flag_filter_cache")
    if key in sh:
        result = sh[key]
    else:
        result = []
        for flag in flags:
            if has_flag(compiler, flag):
                result.append(flag)
        sh[key] = result
    sh.close()
    return result


class BuildExt(build_ext):
    # these flags are not checked and always added
    compile_flags = {"msvc": ['/EHsc'], "unix": ["-std=c++11"]}

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.compile_flags.get(ct, [])
        if ct == 'unix':
            # only add flags which pass the flag_filter
            opts += flag_filter(self.compiler,
                                '-fvisibility=hidden', '-stdlib=libc++',
                                '-std=c++14',
                                '-Wno-deprecated-register')
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


setup(
    name='pyhepmc_ng',
    version=__version__,
    author='Hans Dembinski',
    author_email='hans.dembinski@gmail.com',
    url='https://github.com/scikit-hep/pyhepmc',
    description='Next-generation Python interface to the HepMC high-energy physics event record API',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='generator montecarlo simulation data hep physics particle',
    packages=find_packages(),
    install_requires=['pybind11>=2.2'],
    extras_require={
        "tests": ['pytest', 'graphviz', 'particle'],
    },
    ext_modules=ext_modules,
    cmdclass=dict(build_ext=BuildExt),
    zip_safe=False,
)
