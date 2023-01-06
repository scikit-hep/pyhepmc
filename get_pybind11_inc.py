import pybind11
import os

p = pybind11.get_include()
if p.find(os.getcwd()) == 0:
    p = p[len(os.getcwd()) + 1 :]
print(p)
