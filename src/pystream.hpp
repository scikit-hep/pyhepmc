#ifndef PYHEPMC_PYSTREAM_HPP
#define PYHEPMC_PYSTREAM_HPP

#include "pybind.hpp"
#include <iostream>
#include <streambuf>

class pystreambuf : public std::streambuf {
  py::object iohandle_;
  py::object readinto_;
  py::array_t<char> buffer_;
  char* cbuffer_;
  // context for the compression
public:
  pystreambuf(py::object iohandle, int size);
  int underflow() override;
};

class pyiostream : public std::iostream {
public:
  pyiostream(py::object iohandle, int size);
  virtual ~pyiostream();
};

#endif
