from setuptools import setup, find_packages, Extension
from distutils.filelist import findall
import os
from multiprocessing.pool import ThreadPool

# patch UnixCCompiler to inject platform-specific compiler flags,
# build in parallel and
# skip already compiled object files if they are newer than the source files
def compile(
    self,
    sources,
    output_dir=None,
    macros=None,
    include_dirs=None,
    debug=0,
    extra_preargs=None,
    extra_postargs=None,
    depends=None,
):

    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(
        output_dir, macros, include_dirs, sources, depends, extra_postargs
    )
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)

    extra_compile_flags = (
        "-std=c++11",
        "-fvisibility=hidden",
        # ignore warnings raised by HepMC3 code
        "-Wno-strict-aliasing",
        "-Wno-sign-compare",
        "-Wno-reorder",
        "-Wno-self-assign-overloaded",
        "-Wno-unused-private-field",
    )

    extra_flags_file = output_dir + "/extra_flags"
    if not os.path.exists(extra_flags_file):
        import tempfile, shutil, subprocess as subp

        cmd = self.compiler[0]
        with open(extra_flags_file, "w") as of:
            with open(os.devnull, "w") as devnull:
                tmpdir = tempfile.mkdtemp()
                try:
                    with open(tmpdir + "/main.cpp", "w") as f:
                        f.write("int main() {}")
                    for flag in extra_compile_flags:
                        retcode = subp.call(
                            (cmd, flag, "main.cpp"), cwd=tmpdir, stderr=devnull
                        )
                        if retcode == 0:
                            of.write(flag + "\n")
                finally:
                    shutil.rmtree(tmpdir)

    cc_args += open(extra_flags_file).read().strip().split("\n")

    jobs = []
    for obj in objects:
        try:
            src, ext = build[obj]
        except KeyError:
            continue
        if not os.path.exists(obj) or os.stat(obj).st_mtime < os.stat(src).st_mtime:
            jobs.append((obj, src))

    p = ThreadPool(4)
    p.map(
        lambda args: self._compile(
            args[0], args[1], ext, cc_args, extra_postargs, pp_opts
        ),
        jobs,
    )

    return objects


import distutils.unixccompiler

distutils.unixccompiler.UnixCCompiler.compile = compile


def get_version():
    vars = {}
    exec(open("src/pyhepmc_ng/_version.py").read(), vars)
    return vars["version"]


def get_description():
    content = open("README.md").read()
    range = []
    idx = 0
    while idx >= 0:
        r = [0, 0]
        for imarker, marker in enumerate(("begin", "end")):
            tag = "<!-- %s of description -->" % marker
            idx = content.find(tag, idx)
            if idx == -1:
                break
            if imarker == 0:
                idx += len(tag)
            r[imarker] = idx
        range.append(r)
    return "".join([content[a:b] for (a, b) in range])


setup(
    name="pyhepmc_ng",
    version=get_version(),
    author="Hans Dembinski",
    author_email="hans.dembinski@gmail.com",
    url="https://github.com/scikit-hep/pyhepmc",
    description="Next-generation Python interface to the HepMC3 C++ library",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish
        "License :: OSI Approved :: BSD License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="generator montecarlo simulation data hep physics particle",
    packages=find_packages("src"),
    package_dir={"": "src"},
    extras_require={"tests": ["pytest", "numpy", "graphviz", "particle"]},
    ext_modules=[
        Extension(
            "pyhepmc_ng._bindings",
            [x for x in findall("src") if x.endswith(".cpp")]
            + [x for x in findall("extern/HepMC3/src") if x.endswith(".cc")],
            include_dirs=["src", "extern/HepMC3/include", "extern/pybind11/include"],
            define_macros=[
                ("HEPMC3_HEPEVT_NMXHEP", 10000)
            ],  # increase this if necessary
            language="c++",
        )
    ],
    zip_safe=False,
)
