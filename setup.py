from pathlib import Path
from setuptools import setup
import sys

cdir = Path(__file__).parent

version = {}
with open(cdir / "src" / "pyhepmc" / "_version.py") as f:
    exec(f.read(), version)

sys.path.append(str(cdir))
from cmake_ext import CMakeExtension, CMakeBuild  # noqa: E402

setup(
    zip_safe=False,
    version=version["version"],
    ext_modules=[CMakeExtension("pyhepmc._core")],
    cmdclass={"build_ext": CMakeBuild},
)
