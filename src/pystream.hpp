#ifndef PYHEPMC_PYSTREAM_HPP
#define PYHEPMC_PYSTREAM_HPP

#include "pybind.hpp"
#include <iostream>
#include <streambuf>

class pystreambuf : public std::streambuf {
  py::array_t<char_type> buffer_;
  py::object iohandle_;
  py::object readinto_;
  py::object write_;

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

// need to call pystreambuf ctor before calling iostream ctor,
// so make pystreambuf a base of pyiostream
// struct pyiostream_base {
//   pystreambuf buf_;
//   pyiostream_base(py::object iohandle, int size) : buf_(iohandle, size) {}
// };

class pyiostream : public std::iostream {
public:
  pyiostream(py::object iohandle, int size);
  ~pyiostream();
};

#endif
