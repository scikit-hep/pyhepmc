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
    : buffer_(nullptr, size), iohandle_(iohandle) {
  // this ctor must not throw
  py::gil_scoped_acquire g;
  const bool has_readinto1 = py::hasattr(iohandle, "readinto1");
  if (has_readinto1 || py::hasattr(iohandle, "readinto"))
    readinto_ = iohandle.attr(has_readinto1 ? "readinto1" : "readinto");
  if (py::hasattr(iohandle, "write")) write_ = iohandle.attr("write");
  char* b = PyByteArray_AS_STRING(buffer_.ptr());
  setp(b, b + size);
}

pystreambuf::pystreambuf(const pystreambuf& other) { operator=(other); }

pystreambuf& pystreambuf::operator=(const pystreambuf& other) {
  throw std::runtime_error("copy not implemented");
  return *this;
}

// do nothing here, everything should be flushed beforehand
pystreambuf::~pystreambuf() {}

// reading from python
pystreambuf::int_type pystreambuf::underflow() {
  // HepMC3 code expects \n as linefeed character, even on Windows.
  // To improve performance, we let Python read the raw bytestream and
  // correct \r\n to \n here, by manipulating the view on the internal buffer.
  // - Read raw bytes from Python.
  // - If buffer contains \r at pos i, turn \r at i to \n and set buffer view
  //   from start to i + 1. Skip one character in buffer on next call to
  //   underflow.
  // - Skip this scan in the future if \r is not found, but \n is found in
  //   buffer, but only perform this check until the first \r is found.
  while (gptr() == egptr()) {
    // view is exhausted
    auto start = egptr();
    if (start == end_) {
      // buffer is exhausted, fill from Python
      auto size = pyreadinto_buffer();
      if (size == 0) return traits_type::eof();
      start = pbase();
      end_ = pbase() + size;
    }
    // buffer contains at least one character
    auto end = end_;
    assert(start < end);
    if (search_for_cr_ >= 0) {
      if (skip_next_ || *start == '\r') {
        search_for_cr_ = 1;
        ++start;
      }
      if (start < end) {
        end = std::find(start, end, '\r');
        if (end < end_)
          search_for_cr_ = 1;
        else if (search_for_cr_ == 0) {
          assert(end == end_);
          if (std::find(start, end, '\n') != end) search_for_cr_ = -1;
        }
        if (start < end) {
          if (*(end - 1) == '\r') {
            *(end - 1) = '\n';
            skip_next_ = true;
          }
        }
      }
    }
    // if start == end, do another loop
    setg(pbase(), start, end);
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
  if (pbase() != pptr()) {
    pywrite_buffer();
    setp(pbase(), epptr());
    assert(pbase() == pptr());
  }
  return 0;
}

void pystreambuf::pywrite_buffer() {
  assert(write_);
  const int s = std::distance(pbase(), pptr());
  py::gil_scoped_acquire g;
#if (PY_MAJOR_VERSION >= 3) && (PY_MINOR_VERSION >= 9)
  Py_SET_SIZE(buffer_.ptr(), s);
  PyByteArray_AS_STRING(buffer_.ptr())[s] = '\0'; /* Trailing null */
  write_(buffer_);
#else
  write_(buffer_[py::slice(0, s, 1)]);
#endif
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
