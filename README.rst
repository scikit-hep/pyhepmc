pyhepmc
=======

A Pythonic wrapper for the HepMC3 C++ library.

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
  :target: https://scikit-hep.org

.. image:: https://badge.fury.io/py/pyhepmc.svg
  :target: https://pypi.org/project/pyhepmc

.. image:: https://coveralls.io/repos/github/scikit-hep/pyhepmc/badge.svg?branch=develop
  :target: https://coveralls.io/github/scikit-hep/pyhepmc?branch=develop

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7013498.svg
  :target: https://doi.org/10.5281/zenodo.7013498

pyhepmc was formerly known as pyhepmc-ng. The development of pyhepmc-ng continues in the pyhepmc package.

HepMC3 has its own Python bindings. Why should you use these?

**pyhepmc is easy to install**

The command ``pip install pyhepmc`` just works on all common platforms. Since we publish binary wheels, you don't need to compile anything. Since we include the HepMC3 library, you don't need to install it separately either.

However, building from source is also easy. External software is not required. Just download the repository with ``git clone --recursive`` and run ``pip install -v -e .``.

**pyhepmc is Pythonic and Jupyter notebook-friendly**

pyhepmc is a hand-crafted mapping of C++ code to Python, see documentation for details. Python idioms are supported where appropriate. The classes are designed to render well in Jupyter notebooks.

- C++ methods which act like properties are represented as properties,
  e.g. ``GenParticle::set_status`` and ``GenParticle::status`` are mapped to a single
  ``GenParticle.status`` field in Python.
- Tuples and lists are implicitly convertible to ``FourVector`` and ``ToolInfo`` objects.
- Vectors of objects on the C++ side are mapped to Python lists.
- ``Reader`` and ``Writer`` classes support the context manager protocol. ``Reader`` objects can be iterated over.
- A convenient ``open`` function is provided for reading and writing HepMC files.

**pyhepmc supports visualizations powered by graphviz**

pyhepmc can optionally visualize events, using the mature `graphviz <https://graphviz.org>`_ library as a backend.

.. image:: docs/_static/pyhepmc.svg

**pyhepmc is actively maintained**

pyhepmc is part of the Scikit-HEP project, which aims to provide all tools needed by particle physicists to do data analysis in Python. There is also official collaboration with the HepMC3 project.

**pyhepmc is thoroughly unit tested**

We aim for 100% coverage, not quite there yet.

Documentation
-------------

pyhepmc mirrors the C++ interface of the `HepMC3 library, which is documented here <http://hepmc.web.cern.ch/hepmc>`_. The documentation is mostly copied from HepMC3 and available as Python docstrings, so you can use Python's ``help()`` browser to learn about the API. Alternatively, you can consult our online reference generated from these docstrings.

License
-------

pyhepmc is covered by the BSD 3-clause license, see the ``LICENSE`` file for details. This license only applies to the pyhepmc code. The connected external libraries HepMC3 and pybind11 are covered by other licenses, as described in their respective ``LICENSE`` files.
