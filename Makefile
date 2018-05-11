pyhepmc3.so: src/main.cpp setup.py
	python setup.py build_ext -i

clean:
	rm -rf build dist *.so

test: pyhepmc3.so
	@pytest tests -s

dist:
	python setup.py sdist