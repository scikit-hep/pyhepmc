pyhepmc_ng.so: src/main.cpp setup.py
	python setup.py build_ext -i

clean:
	rm -rf build dist *.so

test:
	@pytest tests -s

dist:
	python setup.py sdist

test_upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test_install:
	pip install --user --index-url https://test.pypi.org/simple/ pyhepmc-ng

upload:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
