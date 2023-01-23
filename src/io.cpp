#include "UnparsedAttribute.hpp"
#include "pybind.hpp"
#include "pyiostream.hpp"
#include "repr.hpp"
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/Reader.h>
#include <HepMC3/ReaderAscii.h>
#include <HepMC3/ReaderAsciiHepMC2.h>
#include <HepMC3/ReaderHEPEVT.h>
#include <HepMC3/ReaderLHEF.h>
#include <HepMC3/WriterAscii.h>
#include <HepMC3/WriterAsciiHepMC2.h>
#include <HepMC3/WriterHEPEVT.h>
#include <iostream>
#include <map>
#include <memory>
#include <pybind11/attr.h>
#include <string>

using namespace HepMC3;

using GenRunInfoPtr = std::shared_ptr<GenRunInfo>;
using ReaderAsciiPtr = std::shared_ptr<ReaderAscii>;
using ReaderAsciiHepMC2Ptr = std::shared_ptr<ReaderAsciiHepMC2>;
using ReaderLHEFPtr = std::shared_ptr<ReaderLHEF>;
using ReaderHEPEVTPtr = std::shared_ptr<ReaderHEPEVT>;

#ifdef HEPMC3_ROOTIO
using ReaderRootTreePtr = std::shared_ptr<ReaderRootTree>;
using ReaderRootPtr = std::shared_ptr<ReaderRoot>;
#endif

void register_io(py::module& m) {

  py::module_ m_doc = py::module_::import("pyhepmc._doc");
  auto doc = py::cast<std::map<std::string, std::string>>(m_doc.attr("doc"));

  py::class_<std::iostream>(m, "iostream")
      .def("getline",
           [](std::iostream& self) {
             char buffer[1024];
             self.getline(buffer, 1024);
             return py::bytes(buffer);
           })
      .def("read",
           [](std::iostream& self, int size) {
             if (size > 1024) throw std::runtime_error("size must be <= 1024");
             char buffer[1024];
             self.read(buffer, size);
             return py::bytes(buffer);
           })
      .def("write",
           [](std::iostream& self, py::bytes s) {
             char* buffer = nullptr;
             py::ssize_t length = 0;
             if (PYBIND11_BYTES_AS_STRING_AND_SIZE(s.ptr(), &buffer, &length))
               py::pybind11_fail("Unable to extract bytes contents!");
             self.write(buffer, length);
           })
      // clang-format off
      METH(flush, pyiostream)
      // clang-format on
      ;

  py::class_<pyiostream, std::iostream>(m, "pyiostream")
      .def(py::init<py::object, int>(), "file_object"_a, "buffer_size"_a = 4096);

  // this class is here to simplify unit testing of Readers and Writers
  py::class_<std::stringstream, std::iostream>(m, "stringstream")
      .def(py::init<>())
      .def(py::init<std::string>())
      .def("__str__",
           (std::string(std::stringstream::*)() const) & std::stringstream::str);

  py::class_<Reader>(m, "Reader")
      // clang-format off
      METH(read_event, Reader, "event"_a)
      METH(failed, Reader)
      METH(close, Reader)
      PROP2(options, Reader)
      // clang-format on
      ;

  py::class_<ReaderAscii, Reader>(m, "ReaderAscii")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::iostream&>(), "istream"_a, py::keep_alive<1, 2>());

  py::class_<ReaderAsciiHepMC2, Reader>(m, "ReaderAsciiHepMC2")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::iostream&>(), "istream"_a, py::keep_alive<1, 2>());

  py::class_<ReaderLHEF, Reader>(m, "ReaderLHEF")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::iostream&>(), "istream"_a, py::keep_alive<1, 2>());

  py::class_<ReaderHEPEVT, Reader>(m, "ReaderHEPEVT")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::iostream&>(), "istream"_a, py::keep_alive<1, 2>());

  py::class_<Writer>(m, "Writer")
      // clang-format off
      METH(write_event, Writer, "event"_a)
      METH(failed, Writer)
      METH(close, Writer)
      PROP2(options, Writer)
      // clang-format on
      ;

  py::class_<WriterAscii, Writer>(m, "WriterAscii")
      .def(py::init<const std::string&, GenRunInfoPtr>(), "filename"_a,
           "run"_a = nullptr)
      .def(py::init<std::iostream&, GenRunInfoPtr>(), "ostream"_a, "run"_a = nullptr,
           py::keep_alive<1, 2>())
      // clang-format off
      // not needed: METH(write_run_info, WriterAscii)
      PROP(precision, WriterAscii)
      // clang-format on
      ;

  py::class_<WriterAsciiHepMC2, Writer>(m, "WriterAsciiHepMC2")
      .def(py::init<const std::string&, GenRunInfoPtr>(), "filename"_a,
           "run"_a = nullptr)
      .def(py::init<std::iostream&, GenRunInfoPtr>(), "ostream"_a, "run"_a = nullptr,
           py::keep_alive<1, 2>())
      // clang-format off
      // not needed: METH(write_run_info, WriterAscii)
      PROP(precision, WriterAsciiHepMC2)
      // clang-format on
      ;

  py::class_<WriterHEPEVT, Writer>(m, "WriterHEPEVT")
      .def(py::init<const std::string&>(), "filename"_a)
      .def(py::init<std::iostream&>(), "ostream"_a, py::keep_alive<1, 2>());

  py::class_<UnparsedAttribute>(m, "UnparsedAttribute", DOC(UnparsedAttribute))
      .def("__str__", [](UnparsedAttribute& a) { return a.parent_->unparsed_string(); })
      // clang-format off
      METH(astype, UnparsedAttribute, "pytype"_a)
      REPR(UnparsedAttribute)
      // clang-format on
      ;
}
