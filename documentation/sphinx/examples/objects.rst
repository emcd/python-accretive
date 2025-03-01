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

Accretive objects allow for the creation of instances where attributes can be
added but not modified or deleted after assignment. This behavior is valuable
for configuration objects, immutable data containers, and scenarios where
attribute stability is required.

.. doctest:: Objects

    >>> from accretive import Object, accretive

Object Class
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

Accretive Decorator
-------------------------------------------------------------------------------

The ``accretive`` decorator can apply accretive attribute behavior to any
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


Accretive Decorator with Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``accretive`` decorator accepts optional parameters to customize behavior:

.. doctest:: Objects

    >>> # With mutable attributes
    >>> @accretive( mutables = ( 'version', ) )
    ... class VersionedConfig:
    ...     def __init__( self, name, version ):
    ...         self.name = name
    ...         self.version = version
    ...
    >>> config = VersionedConfig( 'MyApp', '1.0.0' )
    >>> config.name
    'MyApp'
    >>> config.version
    '1.0.0'

Attributes specified in the ``mutables`` parameter can be modified even after
initial assignment:

.. doctest:: Objects

    >>> # Modify mutable attribute
    >>> config.version = '1.0.1'  # This works fine
    >>> config.version
    '1.0.1'
    >>>
    >>> # Attempt to modify immutable attribute
    >>> config.name = 'YourApp'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'name'.

Mutable attributes can also be deleted:

.. doctest:: Objects

    >>> del config.version  # This works with mutable attributes
    >>> hasattr( config, 'version' )
    False


Custom Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``accretive`` decorator can set or override the docstring of the
decorated class:

.. doctest:: Objects

    >>> @accretive( docstring = 'A configuration class with custom documentation.' )
    ... class DocumentedConfig:
    ...     '''Original docstring that will be replaced.'''
    ...     def __init__( self, name ):
    ...         self.name = name
    ...
    >>> print( DocumentedConfig.__doc__ )
    A configuration class with custom documentation.


Combining Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple parameters can be combined for more flexibility:

.. doctest:: Objects

    >>> @accretive(
    ...     docstring = 'Advanced configuration with mutable settings.',
    ...     mutables = ( 'debug', 'log_level' )
    ... )
    ... class AdvancedConfig:
    ...     def __init__( self, name, debug = False, log_level = 'INFO' ):
    ...         self.name = name
    ...         self.debug = debug
    ...         self.log_level = log_level
    ...
    >>> advanced = AdvancedConfig( 'ServiceApp' )
    >>>
    >>> # Modify mutable attributes
    >>> advanced.debug = True
    >>> advanced.log_level = 'DEBUG'
    >>>
    >>> # Add new attribute
    >>> advanced.timeout = 30
    >>>
    >>> # All attributes are accessible
    >>> advanced.name, advanced.debug, advanced.log_level, advanced.timeout
    ('ServiceApp', True, 'DEBUG', 30)
    >>>
    >>> # Only immutable attributes raise errors on modification
    >>> advanced.name = 'NewName'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'name'.


Working with Data Classes
-------------------------------------------------------------------------------

The ``accretive`` decorator works well with Python's data classes:

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

Working with Slotted Classes
-------------------------------------------------------------------------------

The ``accretive`` decorator also works with classes that use ``__slots__``:

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

Exception Classes
-------------------------------------------------------------------------------

The ``accretive`` decorator is particularly useful for creating exception
hierarchies with accretive properties:

.. doctest:: Objects

    >>> @accretive
    ... class CustomException( Exception ):
    ...     ''' Base exception with accretive attributes. '''
    ...     pass
    ...
    >>> try:
    ...     raise CustomException( 'Operation failed' )
    ... except CustomException as e:
    ...     e.error_code = 500
    ...     print( f"Error {e.error_code}: {e}" )
    ...     try:
    ...         e.error_code = 404  # Try to modify
    ...     except Exception as modify_error:
    ...         print( f"Modification failed: {type(modify_error).__name__}" )
    Error 500: Operation failed
    Modification failed: AttributeImmutabilityError

Multiple Inheritance Considerations
-------------------------------------------------------------------------------

When using the ``Object`` class with multiple inheritance, be aware of
potential layout conflicts with built-in types that have their own memory
layout:

.. doctest:: Objects

    >>> # This would raise a TypeError due to memory layout conflict
    >>> # class InvalidCombination( BaseException, Object ):
    >>> #     pass

    >>> # Instead, use the accretive decorator directly
    >>> @accretive
    ... class ValidException( BaseException ):
    ...     ''' An exception with accretive behavior. '''
    ...     pass
    ...
    >>> ex = ValidException( 'Something went wrong' )
    >>> ex.context = 'Additional information'
    >>> ex.context
    'Additional information'
    >>> # Cannot modify after setting
    >>> ex.context = 'Changed information'
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'context'.

.. warning::

    When working with built-in types (especially exception types) in multiple
    inheritance hierarchies, avoid using the ``Object`` base class which
    uses ``__slots__``. Instead, apply the ``accretive`` decorator directly to
    your class.
