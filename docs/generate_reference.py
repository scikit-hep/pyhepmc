import pyhepmc
import typing as _tp

classes = []
functions = []
for name, obj in pyhepmc.__dict__.items():
    if name.startswith("_"):
        continue
    if isinstance(obj, type):
        classes.append(name)
    elif isinstance(obj, _tp.Callable):
        functions.append(name)

reference = """
.. currentmodule:: pyhepmc
"""

reference += """
Classes
-------
"""

for name in classes:
    reference += f"""
.. autoclass:: {name}
    :members:
    :undoc-members:
"""

reference += """
Functions
---------
"""

for name in functions:
    reference += f"""
.. autofunction:: {name}
"""

reference += """
.. automodule:: pyhepmc.view
    :members:
    :undoc-members:
"""

with open("generated_reference.rst.in", "w") as f:
    f.write(reference)
