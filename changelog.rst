

.. towncrier release notes start

Accretive 2.0 (2024-11-10)
==========================

Bugfixes
--------

- Add missing alias for ``reclassify_modules`` to the qualified aliases module
  (``qaliases``) as ``reclassify_modules_as_accretive``. (#12)


Features
--------

- Add ``ValidatorDictionary`` and ``ProducerValidatorDictionary`` classes.
  Validator dictionaries allow a validation function to be supplied, which can
  inspect the key and value of a proposed dictionary entry to determine if it
  should be accepted or not. Producer dictionaries are like ``defaultdict`` from
  the standard Python ``collections`` module. (#10)
- Add ``py.typed`` file to package to let typecheckers know that it has a full
  set of type annotations. (#11)
- Dictionary classes now accept type annonations for key and value. (#14)
- Accept a ``decorators`` argument with all of the metaclasses to produce classes
  which have a sequence of class decorators applied before class attribute
  accretion is enforced. Some class decorators are compatible with accretion but
  some are not; this gives a way to ensure that they are applied without
  attribute enforcement. Advanced cases, such as ``dataclasses.dataclass( slots
  = True )``, which produces a replacement class, are correctly supported by this
  machinery on CPython.
- Add ``ProtocolClass`` metaclass to produce accretive protocol classes.


Supported Platforms
-------------------

- Add support for CPython 3.13.
- Drop support for CPython 3.8 (past end-of-life).
- Drop support for CPython 3.9 (skipping to 3.10, which is the next baseline LTS
  version for major OS distributions).
- Drop support for PyPy 3.9, which is no longer maintained upstream.


Deprecations and Removals
-------------------------

- Remove ``complete``, ``concealment``, and ``protection`` subpackages to focus
  on core value of package: accretive data structures. Users can easily make
  their own syntheses as necessary. (#13)


Accretive 1.0.1 (2024-07-07)
============================

Improved Documentation
----------------------

- Grammar fixes to documentation and update of trove classifier to 'Stable'.


Accretive 1.0rc0 (2024-07-04)
=============================

Features
--------

- Initial release. Includes accretive **dictionaries**, **namespaces**,
  **modules**, **objects**, and **classes**.
