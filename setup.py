from setuptools import setup, find_packages, Extension
import sys
import os
import glob
import tempfile
import shutil
import subprocess as subp


compile_flags = {
    'unix': (
        '-std=c++11',
        '-fvisibility=hidden',
        '-stdlib=libc++',
        # ignore warnings raised by HepMC3 code
        '-Wno-strict-aliasing',
        '-Wno-sign-compare',
        '-Wno-reorder',
    )
}


# override class method to inject platform-specific compiler flags
def patched_compile(self, sources, **kwargs):
    if not hasattr(self, "my_extra_flags"):
        self.my_extra_flags = []
        cmd = self.compiler[0]
        with open(os.devnull, 'w') as devnull:
            tmpdir = tempfile.mkdtemp()
            try:
                with open(tmpdir + "/main.cpp", "w") as f:
                    f.write('int main() {}')
                for flag in compile_flags.get(self.compiler_type, []):
                    retcode = subp.call((cmd, flag, "main.cpp"),
                                        cwd=tmpdir,
                                        stderr=devnull)
                    if retcode == 0:
                        self.my_extra_flags.append(flag)
            finally:
                shutil.rmtree(tmpdir)
    kwargs['extra_preargs'] = kwargs.get('extra_preargs', []) + self.my_extra_flags
    return self.original_compile(sources, **kwargs)

import distutils.ccompiler
distutils.ccompiler.CCompiler.original_compile = distutils.ccompiler.CCompiler.compile
distutils.ccompiler.CCompiler.compile = patched_compile


def get_version():
    vars = {}
    exec(open("src/pyhepmc_ng/_version.py").read(), vars)
    return vars['version']


def get_description():
    descr = []
    for line in open("README.md").readlines():
        if line.startswith("##"):
            break
        if line.startswith("#"):
            continue
        descr.append(line)
    return "".join(descr)


setup(
    name='pyhepmc_ng',
    version=get_version(),
    author='Hans Dembinski',
    author_email='hans.dembinski@gmail.com',
    url='https://github.com/scikit-hep/pyhepmc',
    description='Next-generation Python interface to the HepMC high-energy physics event record API',
    long_description=get_description(),
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
        'Programming Language :: Python :: 3.7',
    ],
    keywords='generator montecarlo simulation data hep physics particle',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        "tests": ['pytest', 'numpy', 'graphviz', 'particle'],
    },
    ext_modules=[
        Extension('pyhepmc_ng._bindings',
            ['src/bindings.cpp'] + glob.glob('extern/HepMC3/src/*.cc')
            + glob.glob('extern/HepMC3/src/Search/*.cc'),
            include_dirs=[
                'extern/HepMC3/include',
                'extern/pybind11/include',
                'src',
            ],
            language='c++')
    ],
    zip_safe=False,
)
