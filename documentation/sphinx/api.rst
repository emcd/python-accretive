.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

:tocdepth: 4


*******************************************************************************
API
*******************************************************************************


Package ``accretive``
===============================================================================

Data structures which can grow but never shrink - once values are set, they
become immutable. This behavior is useful for configuration registries, plugin
systems, and other scenarios requiring grow-only collections with immutability
guarantees.

* ``Dictionary``: A dict-like structure where entries can be added but not
  modified or removed once set. Variants include:

  - ``ProducerDictionary``: Auto-generates values for missing keys
  - ``ValidatorDictionary``: Validates entries before addition
  - ``ProducerValidatorDictionary``: Combines both behaviors

* ``Namespace``: Similar to :py:class:`types.SimpleNamespace` but with
  immutable attributes after assignment.

* ``Class``: Metaclass for creating classes with accretive class
  attributes.

* ``Module``: A module type that enforces attribute immutability after
  assignment.

* ``reclassify_modules``: Convenience function for making modules in a package
  accretive.

* ``Object``: Base class for objects with accretive attributes.

* ``accretive``: Decorator for causing classes to produce accretive instances.


Module ``accretive.dictionaries``
-------------------------------------------------------------------------------

.. automodule:: accretive.dictionaries


Module ``accretive.namespaces``
-------------------------------------------------------------------------------

.. automodule:: accretive.namespaces


Module ``accretive.modules``
-------------------------------------------------------------------------------

.. automodule:: accretive.modules


Module ``accretive.classes``
-------------------------------------------------------------------------------

.. automodule:: accretive.classes


Module ``accretive.objects``
-------------------------------------------------------------------------------

.. automodule:: accretive.objects


Module ``accretive.exceptions``
-------------------------------------------------------------------------------

.. automodule:: accretive.exceptions


Module ``accretive.qaliases``
-------------------------------------------------------------------------------

.. automodule:: accretive.qaliases
   :imported-members:
   :noindex:
