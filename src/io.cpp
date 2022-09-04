#include "UnparsedAttribute.hpp"
#include "pybind.hpp"
#include "repr.hpp"
#include <HepMC3/GenRunInfo.h>
#include <HepMC3/ReaderAscii.h>
#include <HepMC3/ReaderAsciiHepMC2.h>
#include <HepMC3/ReaderHEPEVT.h>
#include <HepMC3/ReaderLHEF.h>
#include <HepMC3/WriterAscii.h>
#include <HepMC3/WriterAsciiHepMC2.h>
#include <HepMC3/WriterHEPEVT.h>
#ifdef HEPMC3_ROOTIO
#include "HepMC3/ReaderRoot.h"
#include "HepMC3/ReaderRootTree.h"
#endif
#include <map>
#include <memory>
#include <sstream>
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

  // this class is here to simplify unit testing of Readers and Writers
  py::class_<std::stringstream>(m, "stringstream")
      .def(py::init<>())
      .def(py::init<std::string>())
      .def("__str__", (std::string(std::stringstream::*)() const) &
                          std::stringstream::str) METH(flush, std::stringstream)
          METH(write, std::stringstream) METH(read, std::stringstream);

  py::class_<ReaderAscii, ReaderAsciiPtr>(m, "ReaderAscii")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::stringstream&>()) METH(read_event, ReaderAscii)
          METH(failed, ReaderAscii) METH(close, ReaderAscii);

  py::class_<ReaderAsciiHepMC2, ReaderAsciiHepMC2Ptr>(m, "ReaderAsciiHepMC2")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::stringstream&>()) METH(read_event, ReaderAsciiHepMC2)
          METH(failed, ReaderAsciiHepMC2) METH(close, ReaderAsciiHepMC2);

  py::class_<ReaderLHEF, ReaderLHEFPtr>(m, "ReaderLHEF")
      .def(py::init<const std::string>(), "filename"_a)
      // This will be enabled a bit later: .def(py::init<std::stringstream&>())
      METH(read_event, ReaderLHEF) METH(failed, ReaderLHEF) METH(close, ReaderLHEF);

  py::class_<ReaderHEPEVT, ReaderHEPEVTPtr>(m, "ReaderHEPEVT")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<std::stringstream&>())
      .def("read_event", (bool(ReaderHEPEVT::*)(GenEvent&)) & ReaderHEPEVT::read_event)
      .def("read_event",
           (bool(ReaderHEPEVT::*)(GenEvent&, bool)) & ReaderHEPEVT::read_event)
          METH(failed, ReaderHEPEVT) METH(close, ReaderHEPEVT);

  py::class_<WriterAscii>(m, "WriterAscii")
      .def(py::init<const std::string&, GenRunInfoPtr>(), "filename"_a,
           "run"_a = nullptr)
      .def(py::init<std::stringstream&, GenRunInfoPtr>(), "ostringstream"_a,
           "run"_a = nullptr, py::keep_alive<1, 2>()) METH(write_event, WriterAscii)
          METH(write_run_info, WriterAscii) METH(failed, WriterAscii)
              METH(close, WriterAscii) PROP(precision, WriterAscii);

  py::class_<WriterAsciiHepMC2>(m, "WriterAsciiHepMC2")
      .def(py::init<const std::string&, GenRunInfoPtr>(), "filename"_a,
           "run"_a = nullptr)
      .def(py::init<std::stringstream&, GenRunInfoPtr>(), "ostringstream"_a,
           "run"_a = nullptr, py::keep_alive<1, 2>())
          METH(write_event, WriterAsciiHepMC2) METH(write_run_info, WriterAsciiHepMC2)
              METH(failed, WriterAsciiHepMC2) METH(close, WriterAsciiHepMC2)
                  PROP(precision, WriterAsciiHepMC2);

  py::class_<WriterHEPEVT>(m, "WriterHEPEVT")
      .def(py::init<const std::string&>(), "filename"_a) METH(write_event, WriterHEPEVT)
          METH(failed, WriterHEPEVT) METH(close, WriterHEPEVT);

  py::class_<UnparsedAttribute>(m, "UnparsedAttribute", DOC(UnparsedAttribute))
      .def("__str__", [](UnparsedAttribute& a) { return a.parent_->unparsed_string(); })
      // clang-format off
      METH(astype, UnparsedAttribute, "pytype"_a)
      REPR(UnparsedAttribute)
      // clang-format on
      ;

#ifdef HEPMC3_ROOTIO

  py::class_<ReaderRootTree, ReaderRootTreePtr>(m, "ReaderRootTree")
      .def(py::init<const std::string>(), "filename"_a)
      .def(py::init<const std::string, const std::string, const std::string>(),
           "filename"_a, "treename"_a, "branchname"_a) METH(read_event, ReaderRootTree)
          METH(failed, ReaderRootTree) METH(close, ReaderRootTree);

  py::class_<ReaderRoot, ReaderRootPtr>(m, "ReaderRoot")
      .def(py::init<const std::string>(), "filename"_a) METH(read_event, ReaderRoot)
          METH(failed, ReaderRoot) METH(close, ReaderRoot);

#endif
}
