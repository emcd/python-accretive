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

Class
===============================================================================

Accretive classes are similar to standard Python classes, but with the added
property that once an attribute is set, it cannot be altered or removed. This
makes them useful for defining constants or configurations that should remain
immutable once defined.

.. doctest:: Class

    >>> from accretive import Class

Initialization
-------------------------------------------------------------------------------

Accretive classes can be defined using the `Class` metaclass. Attributes can be
added during class definition.

.. doctest:: Class

    >>> class Config( metaclass = Class ):
    ...     host = 'localhost'
    ...     port = 8080
    >>> Config.host
    'localhost'

Immutability
-------------------------------------------------------------------------------

Existing attributes cannot be reassigned.

.. doctest:: Class

    >>> Config.host = '127.0.0.1'
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'host'.

Or deleted.

.. doctest:: Class

    >>> del Config.port
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'port'.

Attribute Assignment
-------------------------------------------------------------------------------

However, new attributes can be assigned.

.. doctest:: Class

    >>> Config.new_feature = 'enabled'
    >>> Config.new_feature
    'enabled'

Decorator Usage
-------------------------------------------------------------------------------

Accretive classes can also use decorators to modify class behavior. Decorators
can add new attributes, but cannot modify existing ones.

.. doctest:: Class

    >>> def add_version( cls ):
    ...     cls.version = '1.0'
    ...     return cls
    >>> class AppConfig( metaclass = Class, decorators = ( add_version, ) ):
    ...     name = 'MyApp'
    >>> AppConfig.version
    '1.0'
    >>> AppConfig.name
    'MyApp'
    >>> AppConfig.name = 'NewApp'
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'name'.

Dynamic Docstring Assignment
-------------------------------------------------------------------------------

Accretive classes support dynamic docstring assignment, allowing for computed
docstrings to be set at class creation.

.. doctest:: Class

    >>> class DocumentedConfig( metaclass = Class, docstring = 'Dynamic docstring' ):
    ...     ''' Static docstring '''
    ...     host = 'localhost'
    >>> DocumentedConfig.__doc__
    'Dynamic docstring'
