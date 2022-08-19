# pyhepmc
<!-- begin of description -->
A Pythonic wrapper for the HepMC3 C++ library.
<!-- end of description -->

pyhepmc was formerly known as pyhepmc-ng. The development of pyhepmc-ng continues in the pyhepmc package.

[![PyPI version](https://badge.fury.io/py/pyhepmc.svg)](https://badge.fury.io/py/pyhepmc)
[![Coverage](https://github.com/scikit-hep/pyhepmc/actions/workflows/coverage.yml/badge.svg)](https://github.com/scikit-hep/pyhepmc/actions/workflows/coverage.yml)
[![Scikit-HEP](https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg)](https://scikit-hep.org/)

<!-- begin of description -->
HepMC3 has its own Python bindings. Why should you use these one?

**pyhepmc is easy to install**

The command `pip install pyhepmc` should work on all Python versions >= 3.6 and all common architectures, since we publish binary wheels.

Building from source is also easy. External software is not required, pyhepmc comes with the source of both pybind11 for the bindings and HepMC3.

**pyhepmc is actively developed**

pyhepmc is part of the Scikit-HEP project, which aims to provide all tools needed by particle physicists to do data analysis in Python. It also gets official support from the HepMC3 project.

**pyhepmc is unit tested**

Everything in pyhepmc is unit tested.

**pyhepmc is Pythonic**

pyhepmc is a hand-crafted mapping of C++ code to Python. It supports Python idioms
where appropriate.

- C++ methods which act like properties are represented as properties,
  e.g. GenParticle::set_status and GenParticle::status are mapped to a single
  GenParticle.status field in Python
- Tuples and lists are implicitly convertible to FourVectors
- Vectors of objects on the C++ side are mapped to Python lists
- ReaderAscii and WriterAscii support the context manager protocol
- A convenient `open` function is provided for reading and writing HepMC files

## Documentation

pyhepmc currently has no separate documentation, but it mirrors the C++ interface of the HepMC3 library, which is documented here: http://hepmc.web.cern.ch/hepmc.
<!-- end of description -->

## License

pyhepmc is covered by the BSD 3-clause license, see the `LICENSE` file for details. This license only applies to the pyhepmc code. The connected external libraries HepMC3 and pybind11 are covered by other licenses, as described in their respective `LICENSE` files.
