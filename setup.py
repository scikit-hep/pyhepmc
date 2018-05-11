from setuptools import setup, Extension
from distutils.command.build_ext import build_ext
from setuptools import distutils
import sys
import os
import glob
import os

__version__ = '0.1'


class lazy_get_pybind_include:
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
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
        'pyhepmc3',
        ['src/main.cpp'] + hepmc_source,
        include_dirs=[
            hepmc_include,
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
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except CompileError:
            return False
    return True


def cpp_flag(compiler):
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Compiler does not support C++11')


class BuildExt(build_ext):
    compile_flags = dict(msvc=['/EHsc'], unix=[])

    if sys.platform == 'darwin':
        compile_flags['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.compile_flags.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


setup(
    name='pyhepmc3',
    version=__version__,
    author='Hans Dembinski',
    author_email='hans.dembinski@gmail.com',
    url='https://github.com/hdembinski/pyhepmc',
    description='Python bindings for HepMC3',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.2'],
    cmdclass=dict(build_ext=BuildExt),
    zip_safe=False,
)
