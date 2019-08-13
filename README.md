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

### Repository management

If you want to contribute to the source code, please follow these instructions. You should start by forking this repository. In the following instructions, replace `YourName` with your Github username.

To start a clone from scratch use this command:
```
git clone --recursive git@github.com:YourName/pyhepmc.git
```
This clones the pyhepmc-ng repository and the nested HepMC3 repository. If you have already cloned in the usual way, you need to initialize and update the nested HepMC3 repository from inside your project folder:
```
git submodule update --init
```
To develop a feature or a fix, create a branch from your master (make sure your master is in sync with the scikit-hep master)
```
git checkout -b my_cool_feature master
```
Commit to your branch and initiate a pull request when you feel the feature is ready to be reviewed.

In the meantime, the scikit-hep master may move forward. Keep the local master in your fork in sync with these commands:
```
git remote add upstream https://github.com/scikit-hep/pyhepmc.git # only needed once
git checkout master
git pull upstream master
git submodule update # update the nested HepMC3 repo if that has moved
```
If you never commit to your master and only commit to new branches, these commands always work. To rebase your feature branch onto the new master, do:
```
git checkout my_cool_feature
git rebase master
```
If there are conflicts between your changes and those in the master, you need to resolve them.

### Build the package

pyhepmc-ng depends on other Python packages. We recommend to setup a virtual environment for development, so that your build environment is isolated from your system-wide Python installation. In the project folder, install a virtual environment:
```
pip install --user virtualenv # only needed if you don't have virtualenv already
virtualenv py37 -p python3.7 # set up a virtualenv for Python3.7 (or use another Python version)
```
Now activate the environment and install the requirements.
```
. py37/bin/activate
pip install -r requirements.txt # install the dependencies
```
Now build the package in developer mode.
```
python setup.py develop
```
This should work, pyhepmc-ng is continously tested on recent versions of gcc, clang and msvc. If it doesn't, please submit an issue with the build log and your compiler version. Finally, you can run the unit tests.
```
pytest
```

### Install the modified version

If you want to use your local version of pyhepmc-ng productively, you can simply do from the project folder:
```
pip install -e .
```
The `-e` option installs the package in developer mode, which means that the installed package remains linked to the source and changes in the project folder are immediately visible for the installed package. If you don't want your installed version to be linked, simply drop the `-e` option.

## License

pyhepmc-ng is covered by the BSD 3-clause license, but the license only
applies to the binding code. The HepMC3 code is covered by the GPL-v3 license.

The BSD 3-clause license text can be found in the `LICENSE` file.

The HepMC3 code is covered by the GPL-v3 license, which can be found in `src/HepMC3/LICENSE`.
