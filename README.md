# pyhepmc-ng

A Python wrapper for the HepMC3 C++ library.

[![PyPI version](https://badge.fury.io/py/pyhepmc-ng.svg)](https://badge.fury.io/py/pyhepmc-ng)
[![Build Status](https://travis-ci.org/scikit-hep/pyhepmc.svg?branch=master)](https://travis-ci.org/scikit-hep/pyhepmc)

Another wrapper is [pyhepmc](https://pypi.org/project/pyhepmc/).
Why should you use this one?

**pyhepmc-ng is easy to install**

The command `pip install pyhepmc-ng` just works! You only need a compiler that
supports C++11, everything else is handled by pip.

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

Start from scratch by cloning your fork. Then `cd` to the project folder.
```
git clone --recursive git@github.com:YourName/pyhepmc.git
cd pyhepmc
```
The first command clones the pyhepmc-ng repository and its nested sub-repositories. If you already cloned the fork without the `--recursive` option, you need to manually initialize the nested sub-repository. `cd` to the project folder and do:
```
git submodule update --init
```
To keep in sync with the master from the scikit-hep repository, add another remote called *upstream*:
```
git remote add upstream https://github.com/scikit-hep/pyhepmc.git
```
This concludes the initial set up.

To develop a feature or a fix, create a branch from your master (make sure your master is in sync with the scikit-hep master)
```
git checkout -b my_cool_feature master
```
Commit to your branch and initiate a pull request from the Github web page when you feel the feature is ready to be reviewed. Note: Never commit to the master, only to feature branches.

The scikit-hep master may have moved forward in the meantime. Keep your local master branch in sync with these commands:
```
git checkout master
git pull upstream master
git submodule update # update the nested sub-repositories if necessary
```
If you have followed the rule to never commit to the master, then these commands always work. To rebase your feature branch onto the updated master, do:
```
git checkout my_cool_feature
git rebase master
```
If there are conflicts between your changes and those in the master, you need to resolve them. Follow the instructions printed by git.

### Build the package

pyhepmc-ng depends on other Python packages. We recommend to setup a virtual environment for development, so that your build environment is isolated from your system-wide Python installation. In the project folder, install a virtual environment:
```
pip install --user virtualenv # only needed if you don't have virtualenv already
virtualenv py37 -p python3.7 # set up a virtualenv for Python3.7 (or use another Python version)
```
Activate the virtualenv and install the required packages for development:
```
. py37/bin/activate
pip install -r requirements.txt
```
Now build the package in develop mode.
```
python setup.py develop
```
This should work since pyhepmc-ng is continously tested on recent versions of gcc, clang and msvc. If it does not, please submit an issue with the build log and your compiler version. Finally, run the unit tests from the project folder.
```
pytest tests
```
These should all pass. If you add new features, don't forget to add unit tests for them.

To leave the virtualenv, call `deactivate` or close the shell.

### Install your local version

If you want to use your local version for productive work, pip-install it from within the local project folder:
```
pip install --user --upgrade .
```
The `--user` option is not necessary when you are inside a virtualenv if you have write-permission to the system-wise Python directories. The `--upgrade` option is only needed if you already have a pyhepmc-ng version installed.

## License

pyhepmc-ng is covered by the BSD 3-clause license, but the license only
applies to the binding code. The HepMC3 code is covered by the GPL-v3 license.

The BSD 3-clause license text can be found in the `LICENSE` file.

The HepMC3 code is covered by the GPL-v3 license, which can be found in `src/HepMC3/LICENSE`.
