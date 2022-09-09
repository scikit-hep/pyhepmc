#include "pystream.hpp"
#include <algorithm>
#include <ios>
#include <pybind11/gil.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <stdexcept>

pystreambuf::pystreambuf(py::object iohandle, int size)
    : iohandle_(iohandle)
    , readinto_(
          iohandle.attr(py::hasattr(iohandle, "readinto1") ? "readinto1" : "readinto"))
    , write_(iohandle.attr("write"))
    , buffer_(size)
    , cbuffer_(buffer_.mutable_data()) {
  setp(cbuffer_, cbuffer_ + size);
}

// for some reason, buffer may be partially filled although all data
// has already been written to sink; must prevent calling sync
// here when file was already closed as workaround
pystreambuf::~pystreambuf() {
  if (py::cast<bool>(iohandle_.attr("closed"))) return;
  try {
    sync_();
  } catch (py::error_already_set& e) {
    // dtor must not throw
    e.discard_as_unraisable("~pystreambuf");
  };
}

pystreambuf::int_type pystreambuf::underflow() {
  // if buffer is exhausted (pos == end) ...
  if (gptr() == egptr()) {
    // ... refill buffer from Python source
    int size = pyreadinto_buffer();
    // return EOF if source is empty ...
    if (size == 0) return traits_type::eof();
    // .. or update view pointers to buffer area
    setg(cbuffer_, cbuffer_, cbuffer_ + size);
  }
  // return current char from refilled buffer
  return traits_type::to_int_type(*gptr());
}

pystreambuf::int_type pystreambuf::overflow(pystreambuf::int_type c) {
  const bool eof = traits_type::eq_int_type(c, traits_type::eof());
  // if buffer is full (pos == end) or c is EOF ...
  if (pptr() == epptr() || eof) {
    // ... write buffer to sink
    sync_();
    // pass-through EOF ...
    if (eof) return c;
  }
  // put current character into buffer
  *pptr() = traits_type::to_char_type(c);
  pbump(1);
  return c;
}

int pystreambuf::sync_() {
  // if buffer is not empty, write buffer to sink
  if (pbase() != pptr()) {
    pywrite_buffer();
    setp(pbase(), epptr());
  }
  return 0;
}

void pystreambuf::pywrite_buffer() {
  const int s = std::distance(pbase(), pptr());
  py::gil_scoped_acquire g;
  // TODO there is probably a more efficient way
  write_(buffer_[py::slice(0, s, 1)]);
}

int pystreambuf::pyreadinto_buffer() {
  py::gil_scoped_acquire g;
  return py::cast<int>(readinto_(buffer_));
}

// pystreambuf must be created before istream is constructed,
// we use new to achieve this
pyiostream::pyiostream(py::object iohandle, int size)
    : std::iostream(new pystreambuf(iohandle, size)) {}

pyiostream::~pyiostream() { delete rdbuf(nullptr); }
