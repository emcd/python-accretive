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

*******************************************************************************
                                  accretive
*******************************************************************************

A Python library package which provides *accretive data structures*.

Accretive data structures can grow at any time but can never shrink. An
accretive dictionary accepts new entires, but cannot have existing entries
altered or removed. Similarly, an accretive namespace accepts new attributes,
but cannot have existing attributes assigned to new values or deleted.

Accretive data structures are useful as registries, which may be incrementally
initialized, but should have immutable state, once initialized. In general,
they are a good compromise between the safety of immutability and the
convenience of incremental initialization.

In addition to accretive dictionaries and namespaces, this package also
provides accretive classes, modules, and objects. Subpackages provide variants
of all of these with some additional behaviors or constraints, such as the
concealment of non-public attributes and the accretion of class attributes.


Examples
===============================================================================


Accretive Namespace
-------------------------------------------------------------------------------

.. code-block:: python

  >>> from accretive import Namespace
  >>> ns = Namespace( apples = 12, bananas = 6, cherries = 42 )
  >>> ns
  accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42 )
  >>> ns.blueberries = 96
  >>> ns.strawberries = 24
  >>> ns
  accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )
  >>> del ns.apples
  Traceback (most recent call last):
  ...
  accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.
  >>> ns.apples = 14
  Traceback (most recent call last):
  ...
  accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.
  >>> ns
  accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )


Accretive Dictionary
-------------------------------------------------------------------------------

.. code-block:: python

  >>> from accretive import Dictionary
  >>> dct = Dictionary( apples = 12, bananas = 6, cherries = 42 )
  >>> dct
  accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42} )
  >>> dct.update( blueberries = 96, strawberries = 24 )
  accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )
  >>> del dct[ 'bananas' ]
  Traceback (most recent call last):
  ...
  accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.
  >>> dct[ 'bananas' ] = 11
  Traceback (most recent call last):
  ...
  accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.
  >>> dct
  accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )


Installation
===============================================================================

::

      pip install accretive
