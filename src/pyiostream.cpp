#include "pyiostream.hpp"
#include <algorithm>
#include <ios>
#include <pybind11/detail/common.h>
#include <pybind11/gil.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <stdexcept>
#include <streambuf>

pystreambuf::pystreambuf(py::object iohandle, int size)
    : buffer_(size), iohandle_(iohandle) {
  // this ctor must not throw
  const bool has_readinto1 = py::hasattr(iohandle, "readinto1");
  if (has_readinto1 || py::hasattr(iohandle, "readinto"))
    readinto_ = iohandle.attr(has_readinto1 ? "readinto1" : "readinto");
  if (py::hasattr(iohandle, "write")) write_ = iohandle.attr("write");
  char* b = buffer_.mutable_data();
  setp(b, b + size);
}

pystreambuf::pystreambuf(const pystreambuf& other) { operator=(other); }

pystreambuf& pystreambuf::operator=(const pystreambuf& other) {
  if (this != &other) {
    buffer_ = py::array_t<char_type>(py::len(other.buffer_));
    iohandle_ = other.iohandle_;
    readinto_ = other.readinto_;
    write_ = other.write_;
    char* b = buffer_.mutable_data();
    const int size = py::len(buffer_);
    setp(b, b + size);
  }
  return *this;
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

// reading from python
pystreambuf::int_type pystreambuf::underflow() {
  // if buffer is exhausted (pos == end) ...
  if (gptr() == egptr()) {
    // ... refill buffer from Python source
    int size = pyreadinto_buffer();
    // return EOF if source is empty ...
    if (size == 0) return traits_type::eof();
    // .. or update view pointers to buffer area
    setg(pbase(), pbase(), pbase() + size);
  }
  // return current char from refilled buffer
  return traits_type::to_int_type(*gptr());
}

// writing to python
pystreambuf::int_type pystreambuf::overflow(pystreambuf::int_type c) {
  // if c is EOF write buffer to sink and return
  if (traits_type::eq_int_type(c, traits_type::eof())) {
    sync_();
    return c;
  }
  // if buffer is full (pos == end) write buffer to sink
  if (pptr() == epptr()) sync_();
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
  py::gil_scoped_acquire g;
  assert(write_);
  const int s = std::distance(pbase(), pptr());
  // TODO there is probably a more efficient way
  write_(buffer_[py::slice(0, s, 1)]);
}

int pystreambuf::pyreadinto_buffer() {
  if (readinto_) {
    py::gil_scoped_acquire g;
    return py::cast<int>(readinto_(buffer_));
  }
  return 0;
}

// pystreambuf must be initialized before std::iostream
pyiostream::pyiostream(py::object iohandle, int size)
    : std::iostream(new pystreambuf(iohandle, size)) {
  if (!static_cast<pystreambuf*>(rdbuf())->has_readinto())
    throw std::runtime_error("file object lacks readinto");
  if (!static_cast<pystreambuf*>(rdbuf())->has_write())
    throw std::runtime_error("file object lacks write");
}

pyiostream::~pyiostream() { delete rdbuf(nullptr); }
