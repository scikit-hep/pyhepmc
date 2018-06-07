.py: ; # do nothing for python scripts as dependencies

build: pyhepmc_ng/cpp.so

pyhepmc_ng/cpp.so: src/*.cpp setup.py
	python setup.py build_ext -i

clean:
	rm -rf build/*/src/*.o pyhepmc_ng/*.so

distclean:
	rm -rf build dist *.so

test: build
	@pytest tests -sv

dist: setup.py src/*.*
	rm -rf dist
	python setup.py sdist

install: build
	python setup.py install

test_upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test_install:
	pip install --user --index-url https://test.pypi.org/simple/ pyhepmc-ng

upload: dist
	twine upload dist/*
