Reference
=========

.. currentmodule:: pyhepmc

pyhepmc offers a more pythonic Python API than the auto-generated HepMC3 Python bindings.

Differences between HepMC3 C++ and pyhepmc
------------------------------------------

- The pyhepmc API uses properties where the C++ API uses setters/getters (where possible).
- Sequences with matching types and lengths are implicitly convertible to :class:`FourVector` und :class:`ToolInfo`.
- In addition to the C++ Reader/Writer classes, we offer an easy to use :func:`open`. It can read any supported format and writes in HepMC3 format.
- The ``Print`` class is missing, but :func:`listing` and :func:`content` are present as free functions.
- The member functions ``delta_X`` of :class:`FourVector` are free functions with two arguments.
- ``HEPEVT_Wrapper`` and friends are missing, use :meth:`GenEvent.from_hepevt` instead
- API marked as deprecated in HepMC3 is not available in Python.

Missing functionality
---------------------

- Not yet implemented: ``GenParticleData``, ``GenVertexData``, ``ReaderMT``, ``ReaderGZ``, ``Setup``, ``WriterGZ``. These will be added in the future.
- Generic ``Attribute`` s for :class:`GenEvent`, :class:`GenParticle`, :class:`GenVertex`, :class:`GenRunInfo` are not yet implemented.

.. include:: generated_reference.rst.in
