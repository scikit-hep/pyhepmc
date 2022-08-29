Reference
=========

Differences between C++ and Python
----------------------------------

- The Python API uses properties where the C++ API uses setters/getters (where possible).
- Sequences with matching types and lengths are implicitly convertible to FourVector und ToolInfo.
- In addition to the C++ Reader/Writer classes, we offer an easy to use :func:`pyhepmc.open`. It can read any supported format and writes in HepMC3 format.
- The Print class is missing, but its functions :func:`listing` and :func:`content` are present.
- The member functions ``delta_X`` of FourVector are free functions with two arguments.

Missing functionality
---------------------
- The classes GenParticleData and GenVertexData are not yet implemented.
- Generic attributes for events, particles, and vertices are not yet implemented.

.. currentmodule:: pyhepmc

.. include:: generated_reference.rst.in
