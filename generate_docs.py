from pathlib import Path  # noqa
import pyhepmc
import subprocess as subp

subp.check_call(["doxygen", "docs/Doxyfile"])

for key, obj in pyhepmc.__dict__.items():
    if key.startswith("_"):
        continue
    if not obj.__doc__:
        print(key)
