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


Namespace
===============================================================================

Accretive namespaces are similar to :py:class:`types.SimpleNamespace`, but with
the added property that once an attribute is set, it cannot be altered or
removed. This makes them useful for configurations and settings that should
remain immutable once defined.

.. doctest:: Namespace

    >>> from accretive import Namespace

Let us illustrate this use case by defining a configuration namespace for a web
application.

Initialization
-------------------------------------------------------------------------------

Accretive namespaces can be initialized from zero or more dictionaries or
iterables over key-value pairs and zero or more keyword arguments.

.. doctest:: Namespace

    >>> config = Namespace(
    ...     ( ( 'host', 'localhost' ), ( 'port', 8080 ) ),
    ...     { 'debug': True, 'database': 'sqlite:///app.db' },
    ...     api_key = '12345-ABCDE' )
    >>> config
    accretive.namespaces.Namespace( host = 'localhost', port = 8080, debug = True, database = 'sqlite:///app.db', api_key = '12345-ABCDE' )

Immutability
-------------------------------------------------------------------------------

Existing attributes cannot be reassigned.

.. doctest:: Namespace

    >>> config.host = '127.0.0.1'
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'host'.

Or deleted.

.. doctest:: Namespace

    >>> del config.port
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'port'.

(Seems like the configuration is locked in.)

New Attributes
-------------------------------------------------------------------------------

However, new attributes can be added.

.. doctest:: Namespace

    >>> config.new_feature = 'enabled'
    >>> config
    accretive.namespaces.Namespace( host = 'localhost', port = 8080, debug = True, database = 'sqlite:///app.db', api_key = '12345-ABCDE', new_feature = 'enabled' )

Copies
-------------------------------------------------------------------------------

To copy an accretive namespace, access its underlying `__dict__` and feed that
as keyword arguments to a new namespace. This is the same way as how it would
be done with :py:class:`types.SimpleNamespace`.

.. doctest:: Namespace

    >>> from types import SimpleNamespace
    >>> config_copy = Namespace( **config.__dict__ ) #**
    >>> config_copy
    accretive.namespaces.Namespace( host = 'localhost', port = 8080, debug = True, database = 'sqlite:///app.db', api_key = '12345-ABCDE', new_feature = 'enabled' )
    >>> ns = SimpleNamespace( **config.__dict__ ) #**

Comparison
-------------------------------------------------------------------------------

The copies are equivalent to their originals.

.. doctest:: Namespace

    >>> config == config_copy
    True
    >>> config_copy == ns
    True

Modifying a copy causes it to become non-equivalent, as expected.

.. doctest:: Namespace

    >>> config_copy.another_feature = 'disabled'
    >>> config == config_copy
    False
    >>> config_copy != ns
    True
