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
Classes
*******************************************************************************


Introduction
===============================================================================

The package provides base classes, decorators, and class factory classes
(metaclasses) to imbue classes, and the instances which they produce, with
attributes concealment and accretion. Base classes, decorators, and class
factories each provide different sets of behaviors.

.. doctest:: Classes

    >>> import accretive

Class Factory Classes
===============================================================================

Class factory classes produce classes which accrete attributes. Instances of
the produced classes have immutable attributes. Both the classes and their
instances conceal attributes.

.. doctest:: Classes

    >>> class Point2d( metaclass = accretive.Class ):
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         self.x = x
    ...         self.y = y
    ...
    >>> point = Point2d( 5, 12 )

Class Attributes Accretion
-------------------------------------------------------------------------------

We can assign new attributes on such classes:

.. doctest:: Classes

    >>> Point2d.foo = 42

However, we cannot reassign or delete attributes on them:

.. doctest:: Classes

    >>> Point2d.foo = 216
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on class ...
    >>> del Point2d.foo
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on class ...
    >>> del Point2d.__init__
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute '__init__' on class ...

Instance Attributes Immutability
-------------------------------------------------------------------------------

We cannot assign or delete attributes on instances of these classes.

.. doctest:: Classes

    >>> point.x = 42
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...
    >>> del point.x
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...

Attributes Concealment
-------------------------------------------------------------------------------

Non-public attributes are concealed on both the classes and their instances.

.. doctest:: Classes

    >>> dir( Point2d )
    ['foo']
    >>> dir( point )
    ['foo', 'x', 'y']


Base Classes
===============================================================================

Base classes and their descendants have immutable attributes. Instances of
these classes accrete attributes.

.. doctest:: Classes

    >>> class Point2d( accretive.Object ):
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         self.x = x
    ...         self.y = y
    ...
    >>> point = Point2d( 3, 4 )

Class Attributes Immutability
-------------------------------------------------------------------------------

We cannot assign or delete attributes on these classes:

.. doctest:: Classes

    >>> Point2d.foo = 42
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on class ...
    >>> del Point2d.foo
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on class ...
    >>> del Point2d.__init__
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute '__init__' on class ...

Instance Attributes Accretion
-------------------------------------------------------------------------------

We can assign new attributes on their instances:

.. doctest:: Classes

    >>> point.foo = 42

However, we cannot reassign or delete attributes on them:

.. doctest:: Classes

    >>> point.foo = 216
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on instance of class ...
    >>> point.x = 3
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...
    >>> del point.x
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...

Attributes Concealment
-------------------------------------------------------------------------------

Non-public attributes are concealed on both the classes and their instances.

.. doctest:: Classes

    >>> dir( Point2d )
    []
    >>> dir( point )
    ['foo', 'x', 'y']


Decorators
===============================================================================

Decorators cause classes to produce instances which accrete attributes.
However, the classes, themselves, retain default Python behaviors (full
mutability and visibility) with respect to their own attributes.

.. doctest:: Classes

    >>> @accretive.with_standard_behaviors
    ... class Point2d:
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         self.x = x
    ...         self.y = y
    ...
    >>> point = Point2d( 8, 15 )
    >>> type( Point2d )
    <class 'type'>

Class Attributes Mutability
-------------------------------------------------------------------------------

Per Python default behavior, class attributes are mutable:

.. doctest:: Classes

    >>> del Point2d.__init__

Instance Attributes Accretion
-------------------------------------------------------------------------------

We can assign new attributes on instances:

.. doctest:: Classes

    >>> point.foo = 42

However, we cannot reassign or delete attributes on them:

.. doctest:: Classes

    >>> point.foo = 216
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'foo' on instance of class ...
    >>> point.x = 5
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...
    >>> del point.x
    Traceback (most recent call last):
    ...
    accretive.exceptions.AttributeImmutability: Could not assign or delete attribute 'x' on instance of class ...

Class Attributes Publicity
-------------------------------------------------------------------------------

Per Python default behavior, all class attributes are visible:

.. doctest:: Classes

    >>> '__init__' in dir( Point2d )
    True

Instance Attributes Concealment
-------------------------------------------------------------------------------

Non-public instance attributes are concealed:

.. doctest:: Classes

    >>> dir( point )
    ['foo', 'x', 'y']


Dataclasses
===============================================================================

The package also provides base classes, decorators, and class factories
(metaclasses) to imbue :py:mod:`dataclasses` with the same standard behaviors
as seen above.

.. doctest:: Classes

    >>> import accretive
    >>> import dataclasses

New dataclasses with accretive class attributes can be produced via metaclass.

.. doctest:: Classes

    >>> class Point2d( metaclass = accretive.Dataclass ):
    ...     x: float
    ...     y: float
    ...
    >>> point = Point2d( x = 5, y = 12 )
    >>> dataclasses.is_dataclass( Point2d )
    True

New dataclasses with accretive instance attributes can inherit from a base.

.. doctest:: Classes

    >>> class Point2d( accretive.DataclassObject ):
    ...     x: float
    ...     y: float
    ...
    >>> point = Point2d( x = 3, y = 4 )
    >>> dataclasses.is_dataclass( Point2d )
    True

As can be seen above, dataclasses are produced without the need to explicitly
decorate with the :py:func:`dataclasses.dataclass` decorator. And, speaking of
decorators, one is provided which transforms a class into a dataclass with the
standard behaviors (instance attributes concealment and accretion) of the
package:

.. doctest:: Classes

    >>> @accretive.dataclass_with_standard_behaviors
    ... class Point2d:
    ...     x: float
    ...     y: float
    ...
    >>> point = Point2d( x = 8, y = 15 )
    >>> dataclasses.is_dataclass( Point2d )
    True
    >>> type( Point2d )
    <class 'type'>


Mutable Instances
===============================================================================

To produce classes with immutable attributes but instances with mutable
attributes, there is a convenience class, ``ObjectMutable``.

.. doctest:: Classes

    >>> class Point2d( accretive.ObjectMutable ):
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         self.x = x
    ...         self.y = y
    ...
    >>> point = Point2d( 7, 24 )
    >>> point.x, point.y = 20, 21
    >>> point.x, point.y
    (20, 21)

Similarly, there is a convenience dataclass, ``DataclassObjectMutable``.

.. doctest:: Classes

    >>> class Point2d( accretive.DataclassObjectMutable ):
    ...     x: float
    ...     y: float
    ...
    >>> dataclasses.is_dataclass( Point2d )
    True
    >>> point = Point2d( x = 7, y = 24 )
    >>> point.x, point.y = 20, 21
    >>> point.x, point.y
    (20, 21)

The ``with_standard_behaviors`` decorator can also provide mutability by
supplying the ``mutables`` argument as a wildcard:

.. doctest:: Classes

    >>> @accretive.with_standard_behaviors( mutables = '*' )
    ... class Point2d:
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         self.x = x
    ...         self.y = y
    ...
    >>> point = Point2d( 7, 24 )
    >>> point.x, point.y = 20, 21
    >>> point.x, point.y
    (20, 21)

Likewise for the ``dataclass_with_standard_behaviors`` decorator:

.. doctest:: Classes

    >>> @accretive.dataclass_with_standard_behaviors( mutables = '*' )
    ... class Point2d:
    ...     x: float
    ...     y: float
    ...
    >>> point = Point2d( x = 7, y = 24 )
    >>> point.x, point.y = 20, 21
    >>> point.x, point.y
    (20, 21)


Attribute Preallocations
===============================================================================

You can preallocate attributes using the standard Python ``__slots__``
mechanism. In addition to potential performance gains for attribute lookups,
this can be useful if you are making a namespace class and want to keep the
namespace dictionary free of record-keeping attributes. You cannot inherit a
standard base class, such as ``Object``, for this purpose, as it is
``__dict__``-based. However, you can create the namespace class via metaclass.

.. doctest:: Classes

    >>> class Namespace( metaclass = accretive.Class ):
    ...     __slots__ = ( '__dict__', )
    ...     def __init__( self, **arguments: float ) -> None:
    ...         self.__dict__.update( arguments )
    ...
    >>> ns = Namespace( x = 20, y = 21 )
    >>> ns.__slots__
    ('__dict__', '_accretive_instance_behaviors_')
    >>> 'x' in ns.__dict__
    True
    >>> '_accretive_instance_behaviors_' in ns.__dict__
    False
    >>> ns.x, ns.y
    (20, 21)

The mapping form of ``__slots__`` is also supported.

.. doctest:: Classes

    >>> class Namespace( metaclass = accretive.Class ):
    ...     __slots__ = { '__dict__': 'Namespace attributes.' }
    ...     def __init__( self, **arguments: float ):
    ...         self.__dict__.update( arguments )
    ...
    >>> ns = Namespace( x = 20, y = 21 )
    >>> ns.__slots__[ '__dict__' ]
    'Namespace attributes.'


Integrations with Custom Behaviors
===============================================================================

You can define dunder methods, like ``__delattr__``, ``__setattr__``, and
``__dir__``, and they will be automatically wrapped by the decorators which
setup attributes concealment and accretion enforcement on classes.

.. doctest:: Classes

    >>> class Point2d( accretive.ObjectMutable ):
    ...     def __init__( self, x: float, y: float ) -> None:
    ...         super( ).__init__( )
    ...         self.x = x
    ...         self.y = y
    ...     def __delattr__( self, name: str ) -> None:
    ...         if not name.startswith( '_' ): print( name )
    ...         super( ).__delattr__( name )
    ...     def __setattr__( self, name: str, value ) -> None:
    ...         if not name.startswith( '_' ): print( f"{name} = {value!r}" )
    ...         super( ).__setattr__( name, value )
    ...     def __dir__( self ):
    ...         print( 'called dir' )
    ...         return super( ).__dir__( )
    ...
    >>> point = Point2d( 3, 4 )
    x = 3
    y = 4
    >>> point.x, point.y = 5, 12
    x = 5
    y = 12
    >>> del point.y
    y
    >>> 'x' in dir( point )
    called dir
    True

The integration points work correctly with inheritance. Furthermore, the
standard behaviors (concealment and accretion) are idempotent, which
improves their performance in class hierarchies.

.. doctest:: Classes

    >>> class Point3d( Point2d ):
    ...     def __init__( self, x: float, y: float, z: float ) -> None:
    ...         super( ).__init__( x, y )
    ...         self.z = z
    ...     def __delattr__( self, name: str ) -> None:
    ...         if name == 'z': print( 'Z!' )
    ...         super( ).__delattr__( name )
    ...     def __setattr__( self, name: str, value ) -> None:
    ...         if name == 'z': print( 'Z!' )
    ...         super( ).__setattr__( name, value )
    ...     def __dir__( self ):
    ...         print( 'called dir in 3D' )
    ...         return super( ).__dir__( )
    ...
    >>> point3 = Point3d( 5, 12, 17 )
    x = 5
    y = 12
    Z!
    z = 17
    >>> point3.z = 60
    Z!
    z = 60
    >>> del point3.z
    Z!
    z
    >>> 'z' not in dir( point3 )
    called dir in 3D
    called dir
    True
