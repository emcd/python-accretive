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


Objects
===============================================================================

Accretive objects allow for the creation of instances, such that new attributes
can be assigned at any time, but cannot be reassigned or deleted after
assignment. Accretive objects can be created via decoration (by ``@accretive``)
or inheritance (from ``Object``).

.. doctest:: Objects

    >>> from accretive import Object, accretive

Decorator
-------------------------------------------------------------------------------

The ``@accretive`` decorator can apply accretive attribute behavior to any
class:

.. doctest:: Objects

    >>> @accretive
    ... class Config:
    ...     def __init__( self, debug = False ):
    ...         self.debug = debug
    ...
    >>> config = Config( debug = True )
    >>> config.debug
    True
    >>> config.verbose = True  # Add new attribute
    >>> config.verbose
    True

As with the ``Object`` class, attributes cannot be modified or deleted once
set:

.. doctest:: Objects

    >>> config.debug = False
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'debug'.


Mutable Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``mutables`` argument can allow some attributes to remain mutable after
assignment.

.. doctest:: Objects

    >>> @accretive( mutables = ( 'version', ) )
    ... class VersionedConfig:
    ...     def __init__( self, name, version ):
    ...         self.name = name
    ...         self.version = version
    ...
    >>> config = VersionedConfig( 'MyApp', '1.0.0' )

Reassignment of mutable attribute:

.. doctest:: Objects

    >>> config.version = '1.0.1'  # This works fine
    >>> config.version
    '1.0.1'

Deletion of mutable attribute:

.. doctest:: Objects

    >>> del config.version  # This works with mutable attributes
    >>> hasattr( config, 'version' )
    False


Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``docstring`` argument can set or override the docstring of the decorated
class. This is useful when docstrings need to be computed dynamically:

.. doctest:: Objects

    >>> @accretive( docstring = 'A configuration class with custom documentation.' )
    ... class DocumentedConfig:
    ...     '''Original docstring that will be replaced.'''
    ...     def __init__( self, name ):
    ...         self.name = name
    ...
    >>> print( DocumentedConfig.__doc__ )
    A configuration class with custom documentation.


Data Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``@accretive`` decorator works well with unfrozen Python data classes:

.. doctest:: Objects

    >>> from dataclasses import dataclass
    >>>
    >>> @accretive
    ... @dataclass
    ... class ServerConfig:
    ...     host: str
    ...     port: int = 8080
    ...
    >>> server = ServerConfig( host = 'localhost' )
    >>> server.host
    'localhost'
    >>> server.port
    8080
    >>> server.secure = True  # Add new attribute
    >>> server.host = '127.0.0.1'  # Attempt to modify
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'host'.


Slotted Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``@accretive`` decorator works with classes which use ``__slots__`` for
attribute storage. Remember to include the ``_behaviors_`` slot:

.. doctest:: Objects

    >>> @accretive
    ... class SlottedConfig:
    ...     __slots__ = ( 'debug', '_behaviors_' )
    ...
    ...     def __init__( self, debug = False ):
    ...         self.debug = debug
    ...
    >>> config = SlottedConfig( debug = True )
    >>> config.debug
    True
    >>> config.debug = False
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'debug'.


Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``@accretive`` decorator cannot be applied to classes that define their own
``__setattr__`` or ``__delattr__`` methods, as this would conflict with the
immutability enforcement:

.. doctest:: Objects

    >>> @accretive  # This will fail
    ... class Mutable:
    ...     def __setattr__( self, name, value ):
    ...         # Custom attribute setting logic
    ...         super( ).__setattr__( name, value )
    Traceback (most recent call last):
    ...
    accretive.exceptions.DecoratorCompatibilityError: Cannot decorate class 'Mutable' which defines '__setattr__'.


Base Class
-------------------------------------------------------------------------------

The ``Object`` base class provides accretive behavior when instantiated
directly:

.. doctest:: Objects

    >>> obj = Object( )
    >>> obj.name = 'example'
    >>> obj.name
    'example'

or through inheritance:

.. doctest:: Objects

    >>> class CustomConfig( Object ):
    ...     ''' A custom configuration with accretive attributes. '''
    ...     pass
    ...
    >>> custom = CustomConfig( )
    >>> custom.setting = 'enabled'

Once attributes are set, they cannot be modified or deleted:

.. doctest:: Objects

    >>> obj.name = 'modified'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'name'.

    >>> del custom.setting
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'setting'.

New attributes can be added at any time:

.. doctest:: Objects

    >>> obj.version = '1.0'
    >>> obj.version
    '1.0'

.. warning::

    When working with built-in types, such as exception types, in multiple
    inheritance hierarchies, avoid using the ``Object`` base class which uses
    ``__slots__``. Instead, apply the ``@accretive`` decorator directly to your
    class.


Multiple Inheritance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the ``Object`` class with multiple inheritance, be aware of
potential layout conflicts with built-in types that have their own memory
layout:

.. doctest:: Objects

    >>> # This would raise a TypeError due to memory layout conflict
    >>> # class InvalidCombination( BaseException, Object ):
    >>> #     pass

Instead, use the ``@accretive`` decorator directly:

.. doctest:: Objects

    >>> @accretive
    ... class ValidException( BaseException ):
    ...     ''' An exception with accretive behavior. '''
    ...     pass
    ...
    >>> ex = ValidException( 'Something went wrong' )
    >>> ex.context = 'Additional information'
    >>> ex.context
    'Additional information'
    >>> ex.context = 'Changed information'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'context'.
