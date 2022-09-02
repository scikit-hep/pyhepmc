import sys
from pathlib import Path
from setuptools import setup
from distutils.command.sdist import sdist

cdir = Path(__file__).parent.absolute()

sys.path.append(str(cdir))
from cmake_ext import CMakeExtension, CMakeBuild  # noqa: E402
from setup_utils import merge_license_files  # noqa: E402


class sdist_mod(sdist):
    def run(self):
        with merge_license_files():
            sdist.run(self)


setup(
    zip_safe=False,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    ext_modules=[CMakeExtension("pyhepmc._core")],
    cmdclass={"build_ext": CMakeBuild, "sdist": sdist_mod},
)
