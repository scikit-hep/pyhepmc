import pybind11
import os
from pathlib import Path

p = Path(pybind11.get_include())
print(p.relative_to(os.getcwd()))
