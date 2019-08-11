# pyhepmc-ng

A Python wrapper for the HepMC3 C++ library.

[![PyPI version](https://badge.fury.io/py/pyhepmc-ng.svg)](https://badge.fury.io/py/pyhepmc-ng)
[![Build Status](https://travis-ci.org/scikit-hep/pyhepmc.svg?branch=master)](https://travis-ci.org/scikit-hep/pyhepmc)

Another wrapper is [pyhepmc](https://pypi.org/project/pyhepmc/).
Why should you use this one?

**pyhepmc-ng is easy to install**

The command `pip install pyhepmc-ng` just works! You only need a compiler that
supports C++14, everything else is handled by pip.

Under the hood, the bindings are build with the excellent
[pybind11](http://pybind11.readthedocs.io/en/stable/) library.
pybind11 is automatically installed as a requirement by pip. You don't need an
external installation of the HepMC3 library, either. A copy of this
light-weight library is included.

**pyhepmc-ng is actively developed**

pyhepmc-ng is part of the Scikit-HEP project, which aims to provide all tools needed by particle physicists to do data analysis in Python.

**pyhepmc-ng is unit tested**

Everything in pyhepmc-ng is unit tested.

**pyhepmc-ng supports Pythonic code**

pyhepmc-ng is a hand-crafted mapping of C++ code to Python. It supports Python idioms
where appropriate.

- C++ methods which act like properties are represented as properties,
  e.g. GenParticle::set_status and GenParticle::status are mapped to a single
  GenParticle.status field in Python
- Tuples and lists are implicitly convertible to FourVectors
- ReaderAscii and WriterAscii support the context manager protocol

## For developers

If you want to play with the source code, clone this repository and start
hacking.

Local installation for testing

    python setup.py build_ext -i

If you are on Linux or OSX, you can alternatively do (and save a bit of typing)

    make

User-wide installation

    python setup.py install --user

Running the tests requires `pytest`. Do

    pytest tests

or simply

    make test

## License

pyhepmc-ng is covered by the BSD 3-clause license, but the license only
applies to the binding code. The HepMC3 code is covered by the GPL-v3 license.

The BSD 3-clause license text can be found in the `LICENSE` file.

The HepMC3 code is covered by the GPL-v3 license, which can be found in `src/HepMC3/LICENSE`.
