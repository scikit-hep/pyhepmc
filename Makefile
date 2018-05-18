_pyhepmc_ng.so: src/*.* setup.py
	python setup.py build_ext -i

clean:
	rm -rf build/*/*.o *.so

distclean:
	rrm -rf build dist *.so

test: _pyhepmc_ng.so
	@pytest tests -sv

dist: setup.py src/main.cpp
	rm -rf dist
	python setup.py sdist

test_upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test_install:
	pip install --user --index-url https://test.pypi.org/simple/ pyhepmc-ng
