#ifndef PYHEPMC_PYSTREAM_HPP
#define PYHEPMC_PYSTREAM_HPP

#include "pybind.hpp"
#include <iostream>
#include <streambuf>

struct eol_normalizer {
  bool skip_ = false;
  void operator()(char* s, int& size) noexcept;
};

class pystreambuf : public std::streambuf {
  py::array_t<char_type> buffer_;
  py::object iohandle_;
  py::object readinto_;
  py::object write_;
  eol_normalizer eol_normalizer_;

public:
  bool initialization_error() const { return !readinto_ || !write_; }

  pystreambuf(py::object iohandle, int size);
  pystreambuf(const pystreambuf&);
  pystreambuf& operator=(const pystreambuf&);

  ~pystreambuf();

  int_type underflow() override;
  int_type overflow(int_type c) override;
  int sync() override { return sync_(); };

  // see pybind11/include/iostream.h for sync logic
  int sync_();
  int pyreadinto_buffer();
  void pywrite_buffer();
};

class pyiostream : public std::iostream {
public:
  pyiostream(py::object iohandle, int size);
  ~pyiostream();
};

#endif
