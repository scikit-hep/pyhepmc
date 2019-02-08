.py: ; # do nothing for python scripts as dependencies

build: pyhepmc_ng/cpp*.so

pyhepmc_ng/cpp*.so: src/*.cpp setup.py
	python3 setup.py build_ext -i

clean:
	rm -rf build pyhepmc_ng/*.so

distclean: clean
	rm -rf dist pyhepmc_ng.egg-info

test: build
	@python3 -m pytest tests -sv

dist: setup.py src/*.*
	rm -rf dist
	python3 setup.py sdist

install: build
	python3 setup.py install

test_upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test_install:
	pip3 install --user --index-url https://test.pypi.org/simple/ pyhepmc-ng

upload: dist
	twine upload --username hdembins dist/*

.PHONY: dist