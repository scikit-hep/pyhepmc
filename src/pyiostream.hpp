#ifndef PYHEPMC_PYSTREAM_HPP
#define PYHEPMC_PYSTREAM_HPP

#include "pybind.hpp"
#include <iostream>
#include <streambuf>

class pystreambuf : public std::streambuf {
  py::bytearray buffer_;
  py::object iohandle_;
  py::object readinto_;
  py::object write_;
  char search_for_cr_ = 0; // three-way 0 undecided, 1 yes, -1 no
  bool skip_next_ = false;
  char_type* end_ = nullptr;

public:
  bool has_readinto() const { return !readinto_.is_none(); }
  bool has_write() const { return !write_.is_none(); }

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
