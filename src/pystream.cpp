#include "pystream.hpp"

pystreambuf::pystreambuf(py::object iohandle, int size)
    : iohandle_(iohandle)
    , readinto_(iohandle_.attr("readinto1"))
    , buffer_(size)
    , cbuffer_(buffer_.mutable_data()) {}

int pystreambuf::underflow() {
  if (this->gptr() == this->egptr()) {
    int size = py::cast<int>(readinto_(buffer_));
    this->setg(this->cbuffer_, this->cbuffer_, this->cbuffer_ + size);
  }
  return this->gptr() == this->egptr() ? traits_type::eof()
                                       : traits_type::to_int_type(*this->gptr());
}

// pystreambuf must be created before istream is constructed,
// we use placement new to achieve this AND store the object
// locally in pyistream
pyistream::pyistream(py::object iohandle, int size)
    : std::istream(new pystreambuf(iohandle, size)) {}

pyistream::~pyistream() { delete rdbuf(nullptr); }
