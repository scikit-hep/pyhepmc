#!/bin/bash
rm -f dist/*
python setup.py sdist
if [ "$1" = "final" ]; then
  twine upload dist/*
else
  twine upload -r testpypi dist/*
fi
