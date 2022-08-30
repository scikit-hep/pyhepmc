from pathlib import Path
from setuptools import setup
import sys

cdir = Path(__file__).parent.absolute()

sys.path.append(str(cdir))
from cmake_ext import CMakeExtension, CMakeBuild  # noqa: E402

setup(
    zip_safe=False,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    ext_modules=[CMakeExtension("pyhepmc._core")],
    cmdclass={"build_ext": CMakeBuild},
)
