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

Classes
===============================================================================

Standard Classes
-------------------------------------------------------------------------------

Accretive classes are similar to standard Python classes, but with the added
property that once an attribute is set, it cannot be altered or removed. This
makes them useful for defining constants or configurations that should remain
immutable once defined.

.. doctest:: Classes

    >>> from accretive import Class

Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accretive classes can be defined using the `Class` metaclass. Attributes can be
added during class definition.

.. doctest:: Classes

    >>> class Config( metaclass = Class ):
    ...     host = 'localhost'
    ...     port = 8080
    >>> Config.host
    'localhost'

Immutability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Existing attributes cannot be reassigned.

.. doctest:: Classes

    >>> Config.host = '127.0.0.1'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute 'host'.

Or deleted.

.. doctest:: Classes

    >>> del Config.port
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute 'port'.

Attribute Assignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However, new attributes can be assigned.

.. doctest:: Classes

    >>> Config.new_feature = 'enabled'
    >>> Config.new_feature
    'enabled'

Decorator Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accretive classes can also use decorators to modify class behavior. Decorators
can add new attributes, but cannot modify existing ones.

.. doctest:: Classes

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
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute 'name'.

Mutable Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While accretive classes make attributes immutable by default after assignment,
you can designate specific attributes as mutable using the ``mutables``
parameter. This is useful for attributes that need to be updated or removed
throughout the class lifecycle.

.. doctest:: Classes

    >>> class Configuration( metaclass = Class, class_mutables = ( 'version', ) ):
    ...     name = 'MyApp'
    ...     version = '1.0.0'
    ...     release_date = '2025-01-01'

    >>> # Standard immutable attributes behave as expected
    >>> Configuration.name = 'NewApp'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'name'.

    >>> # Mutable attributes can be modified
    >>> Configuration.version = '1.0.1'
    >>> Configuration.version
    '1.0.1'

    >>> # Mutable attributes can also be deleted
    >>> del Configuration.version
    >>> hasattr( Configuration, 'version' )
    False

    >>> # New mutable attributes can be added later
    >>> Configuration.version = '1.1.0'
    >>> Configuration.version
    '1.1.0'

Abstract Base Classes
-------------------------------------------------------------------------------

The ``AbstractBaseClass`` metaclass creates accretive abstract base classes.
This is particularly useful for defining interfaces that can be extended but
not modified after definition. All of the behaviors mentioned for standard
classes also apply to these.

.. doctest:: Classes

    >>> from accretive import AbstractBaseClass
    >>> from abc import abstractmethod

    >>> class DataStore( metaclass = AbstractBaseClass ):
    ...     @abstractmethod
    ...     def get( self, key ): pass
    ...
    ...     @abstractmethod
    ...     def put( self, key, value ): pass
    ...
    ...     ENCODING = 'utf-8'

The abstract methods and class attributes are protected from modification:

.. doctest:: Classes

    >>> def new_method( self ): pass
    >>> DataStore.list_keys = new_method  # Attempt to replace
    >>> # Cannot modify class attributes
    >>> DataStore.ENCODING = 'ascii'  # Attempt to modify
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute 'ENCODING'.

However, new abstract methods and class attributes can be added:

.. doctest:: Classes

    >>> # Adding a new abstract method is permitted
    >>> @abstractmethod
    ... def delete( self, key ): pass
    >>> DataStore.delete = delete
    >>> # Adding a new class attribute is permitted
    >>> DataStore.TIMEOUT = 30

Protocol Classes
-------------------------------------------------------------------------------

The ``ProtocolClass`` metaclass creates accretive protocol classes, which is
useful for defining type interfaces that can be extended but not modified. All
of the behaviors mentioned for standard classes also apply to these.

.. doctest:: Classes

    >>> from accretive import ProtocolClass
    >>> from typing import Protocol

    >>> class Comparable( Protocol, metaclass = ProtocolClass ):
    ...     def __lt__( self, other ) -> bool: ...
    ...     def __gt__( self, other ) -> bool: ...
    ...
    ...     ORDERING = 'natural'

The existing protocol interface is protected from modification:

.. doctest:: Classes

    >>> # Cannot modify existing protocol method
    >>> def lt( self, other ) -> bool: ...
    >>> Comparable.__lt__ = lt  # Attempt to replace
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute '__lt__'.
    >>> # Cannot modify existing class attributes
    >>> Comparable.ORDERING = 'reverse'  # Attempt to modify
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete existing attribute 'ORDERING'.

However, new protocol methods and class attributes can be added:

.. doctest:: Classes

    >>> # Adding new class attributes is permitted
    >>> Comparable.COMPARISON_MODE = 'strict'
