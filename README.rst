pyhepmc
=======

A Pythonic wrapper for the `HepMC3 C++ library <http://hepmc.web.cern.ch/hepmc>`_.

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
  :target: https://scikit-hep.org

.. image:: https://badge.fury.io/py/pyhepmc.svg
  :target: https://pypi.org/project/pyhepmc

.. image:: https://img.shields.io/conda/vn/conda-forge/pyhepmc.svg
  :target: https://github.com/conda-forge/pyhepmc-feedstock

.. image:: https://coveralls.io/repos/github/scikit-hep/pyhepmc/badge.svg?branch=main
  :target: https://coveralls.io/github/scikit-hep/pyhepmc?branch=main

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7013498.svg
  :target: https://doi.org/10.5281/zenodo.7013498

pyhepmc was formerly known as pyhepmc-ng. The development of pyhepmc-ng continues in the pyhepmc package.

HepMC3 has its own Python bindings. Why should you use these?

**pyhepmc is easy to install**

The command

.. code:: bash

   python -m pip install pyhepmc

just works on all common platforms. Since we publish binary wheels, you don't need to compile anything. Since we include the HepMC3 library, you don't need to install it separately either.

However, building from source is also easy. External software is not required. Just download the repository with ``git clone --recursive`` and run ``python -m pip install -v -e .``.

``pyhepmc`` is also available on conda-forge

.. code:: bash

   conda install --channel conda-forge pyhepmc

**pyhepmc is Pythonic, Numpy-friendy, and Jupyter notebook-friendly**

pyhepmc is a hand-crafted mapping of C++ code to Python, `see documentation for details <https://scikit-hep.org/pyhepmc/reference.html>`_, while the official HepMC3 bindings are generated by a script. The pyhepmc API has been optimised for safety, usability, and efficiency by a human expert, something that an automatic tool cannot provide. pyhepmc brings these unique features:

- Python idioms are supported where appropriate.
- Simple IO with ``pyhepmc.open``.
- An alternative Numpy API accelerates event processing up to **70x** compared to the standard API.
- The public API is fully documented with Python docstrings.
- Objects are inspectable in Jupyter notebooks (have useful ``repr`` strings).
- Events render as graphs in Jupyter notebooks (see next item).

**pyhepmc supports visualizations powered by graphviz**

pyhepmc can optionally visualize events, using the mature `graphviz <https://graphviz.org>`_ library as a backend.

.. image:: docs/_static/pyhepmc.svg

**pyhepmc is actively maintained**

pyhepmc is part of the Scikit-HEP project, which aims to provide all tools needed by particle physicists to do data analysis in Python. It is developed in close collaboration with the HepMC3 project.

**pyhepmc is thoroughly unit tested**

We have close to 100% coverage for the Python API.

Documentation
-------------

`Documentation is available here <https://scikit-hep.org/pyhepmc/>`_, and includes some examples (Jupyter notebooks). Furthermore, you can use Python's ``help()`` browser to learn about the API. The documentation is generated from Python docstrings, which are translated from the `HepMC3 library, which is documented here <http://hepmc.web.cern.ch/hepmc>`_.

License
-------

The pyhepmc code is covered by the BSD 3-clause license, but its main functionality comes from bundled software which is released under different licenses. The HepMC3 library is licensed under LGPL-v3 and bundles other software which is released under different licenses. See the files ``LICENSE`` and ``LICENSE_bundled`` in the source directory for details.
