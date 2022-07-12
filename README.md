# pyhepmc
<!-- begin of description -->
A Pythonic wrapper for the HepMC3 C++ library.
<!-- end of description -->

pyhepmc was formerly known as pyhepmc-ng. The development of pyhepmc-ng continues in the pyhepmc package.

[![PyPI version](https://badge.fury.io/py/pyhepmc.svg)](https://badge.fury.io/py/pyhepmc)

<!-- begin of description -->
HepMC3 has its own Python bindings. Why should you use these one?

**pyhepmc is easy to install**

The command `pip install pyhepmc` should work on all Python versions >= 3.6 and all common architectures.

Under the hood, the bindings are build with the excellent
[pybind11](http://pybind11.readthedocs.io/en/stable/) library. External installations of pybind11 or HepMC3 are not required, pyhepmc includes the lightweight source code of both libraries with the submodule feature of `git`.

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

## For developers

### Repository management

If you want to contribute to the source code, please follow these instructions. Start by forking the scikit-hep repository, then clone your fork to your local compute with these commands (replace `YourName` with your Github username):
```
git clone --recursive git@github.com:YourName/pyhepmc.git
```
Now `cd` to the project folder (the rest assumes you are in the project folder). The command clones the pyhepmc repository and its nested sub-repositories. If you already cloned the fork without the `--recursive` option, you need to manually initialize the nested sub-repositories:
```
git submodule update --init
```
Add a remote endpoint called *upstream* to keep in sync with the master of the scikit-hep repository:
```
git remote add upstream https://github.com/scikit-hep/pyhepmc.git
```
This concludes the initial set up.

To develop a feature or a fix, create a branch from your master (make sure your master is in sync with the scikit-hep master):
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
If you have followed the rule to never commit to the master, then these commands always work. Rebase your feature branch onto the updated master:
```
git checkout my_cool_feature
git rebase master
```
If conflicts between your changes and those in the master appear, you need to resolve them. Follow the instructions printed by git.

### Build the package

pyhepmc depends on other Python packages. We recommend to use a virtual environment for development which is isolated from your system-wide Python installation. Install a virtual environment in the project folder:
```
pip install --user virtualenv # only needed if you don't have virtualenv already
virtualenv py37 -p python3.7 # or use another Python version
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
This should work since pyhepmc is continously tested on recent versions of gcc, clang and msvc. If it does not, please submit an issue with the build log and your compiler version. You can now change the source code. Run the previous command again to build the project after you made changes. Finally, run the unit tests:
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
The `--user` option is not necessary when you are inside a virtualenv or if you have write-permission to the system-wise Python directories. The `--upgrade` option makes sure that an already existing pyhepmc version is replaced.

## License

pyhepmc is covered by the BSD 3-clause license, see the `LICENSE` file for details. This license only applies to the pyhepmc code. The connected external libraries HepMC3 and pybind11 are covered by other licenses, as described in their respective `LICENSE` files.
