"""
License: pyhepmc-ng is covered by the BSD license, but the license only
applies to the binding code. The HepMC3 code is covered by the GPL-v3 license.
"""
from setuptools import setup, find_packages, Extension
from distutils.command.build_ext import build_ext
from setuptools import distutils
import sys
import os
import glob


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


hepmc_source = glob.glob('extern/HepMC3/src/*.cc') + glob.glob('extern/HepMC3/src/Search/*.cc')
hepmc_include = 'extern/HepMC3/include'
pybind11_include = 'extern/pybind11/include'
ext_modules = [
    Extension(
        'pyhepmc_ng._bindings',
        ['src/bindings.cpp'] + hepmc_source,
        include_dirs=[
            hepmc_include,
            pybind11_include,
            'src',
        ],
        language='c++'
    ),
]


def has_flag(compiler, flagname):
    sys.stdout.write("TESTING compiler flag: %s\n" % flagname)
    import tempfile
    from distutils.errors import CompileError
    try:
        with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
            f.write('int main() {}')
            compiler.compile([f.name], extra_postargs=[flagname], quiet=True)
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
                                '-fvisibility=hidden',
                                '-stdlib=libc++',
                                '-std=c++14',
                                # ignore warnings raised by HepMC3 code
                                '-Wno-deprecated-register',
                                '-Wno-strict-aliasing',
                                '-Wno-sign-compare'
                                '-Wno-reorder')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


def get_version():
    vars = {}
    exec(open("src/pyhepmc_ng/_version.py").read(), vars)
    return vars['version']


setup(
    name='pyhepmc_ng',
    version=get_version(),
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
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        "tests": ['pytest', 'numpy', 'graphviz', 'particle'],
    },
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
