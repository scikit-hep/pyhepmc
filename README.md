# pyhepmc-ng

An alternative wrapper of the HepMC-v3 C++ library.

[![PyPI version](https://badge.fury.io/py/pyhepmc_ng.svg)](https://badge.fury.io/py/pyhepmc_ng)
[![Build Status](https://travis-ci.org/HDembinski/pyhepmc.svg?branch=master)](https://travis-ci.org/HDembinski/pyhepmc)

The official wrapper is [pyhepmc](https://pypi.org/project/pyhepmc/).
Why should you use this one?

**pyhepmc-ng is easy to install**

The command `pip install pyhepmc-ng` just works! You only need a compiler that
supports C++14, everything else is handled by pip.

Under the hood, the bindings are build with the excellent
[pybind11](http://pybind11.readthedocs.io/en/stable/) library.
pybind11 is automatically installed as a requirement by pip. You don't need an
external installation of the HepMC library, either. A copy of this
light-weight library is included.

The original pyhepmc package is not easy to install. It uses SWIG to create
the bindings, which has to be installed separately. It also requires you to
install the C++ library HepMC separately. When you try a pip-install, it will
in general not work out-of-the-box. Instead you will get intimidating error
messages, which are difficult to decipher.

**pyhepmc-ng is actively developed and maintained**

The last release of pyhepmc was May 2013.

**pyhepmc-ng is unit tested**

Everything in pyhepmc-ng is unit tested. A few bugs were already found in
HepMC3 in this way, notably in the `HEPEVT_Wrapper` class.

**pyhepmc-ng supports Pythonic code**

pyhepmc-ng is not a blind mapping of C++ code to Python. It uses Python idioms
where it is appropriate.

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

pyhepmc-ng is provided under a BSD 3-clause license that can be found in the `LICENSE` file.

The HepMC code included in the repository is covered by the GPL-v3 license, which can be found in `src/HepMC3/LICENSE`.
