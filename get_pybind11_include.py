import pybind11
import os
from pathlib import Path

p = Path(pybind11.get_include())
try:
    p = p.relative_to(os.environ.get("MESON_SOURCE_ROOT", os.getcwd()))
except ValueError:
    pass

print(p)
