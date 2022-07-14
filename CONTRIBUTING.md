# Contributing to pyhepmc

## Repository management

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

## Building

pyhepmc depends on other Python packages. We recommend using a virtual environment for development which is isolated from your system-wide Python installation. Install a virtual environment in the project folder:
```
python3 -m venv venv
```
Activate the virtualenv and install the required packages for development:
```
. venv/bin/activate
pip install -v -e .'[test]'
```
This builds the package in develop mode and installs the extra libraries used for testing. The build should work fine if you have a reasonably recent C++ compiler, since pyhepmc is continuously tested on against gcc, clang and msvc. If it does not, please submit an issue with the build log and your compiler version.

You can now change the source code. Run pip again to build the project after you made changes. To run the unit tests:
```
python -m pytest
```
If you add new features, don't forget to add unit tests for them.

To leave the virtualenv, call `deactivate` or close the shell.

### Install your local version

If you want to use your local version for productive work, install it from the local project folder:
```
pip install --upgrade <project folder>
```
The `--upgrade` option makes sure that an already existing pyhepmc version is replaced.
