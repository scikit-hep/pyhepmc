pyhepmc.so: src/main.cpp
	python setup.py build_ext -i

clean:
	rm -rf build *.so

test: pyhepmc.so
	@pytest tests -s