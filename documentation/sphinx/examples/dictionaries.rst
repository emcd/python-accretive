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


Simple Dictionary
===============================================================================


Producer Dictionary
===============================================================================

.. doctest:: ProducerDictionary

    >>> from accretive import ProducerDictionary

Producer dictionaries are nearly equivalent to
:py:class:`collections.defaultdict`. The first argument to the initializer for
a producer dictionary must be a callable which can be invoked with no
arguments. This callable is used to create entries that are absent at lookup
time.

.. doctest:: ProducerDictionary

    >>> ddct = ProducerDictionary( list )
    >>> ddct
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {} )
    >>> ddct[ 'abc' ]
    []
    >>> ddct
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'abc': []} )

A common use case is to automatically initialize a mutable data structure, such
as a :py:class:`list`, and add elements or entries to it by merely referencing
its corresponding key... without checking whether the entry exists or creating
the entry first.

.. doctest:: ProducerDictionary

    >>> ddct[ 'def' ].append( 42 )
    >>> ddct
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'abc': [], 'def': [42]} )

Of course, entries can be explicitly added the same way as a simple dictionary.

.. doctest:: ProducerDictionary

    >>> ddct[ 'foo' ] = 'bar'
    >>> ddct
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'abc': [], 'def': [42], 'foo': 'bar'} )

A producer dictionary can also be initialized from multiple iterators, as well
as keyword arguments. The first argument must, of course, be the producer.

.. doctest:: ProducerDictionary

    >>> other_ddct = ProducerDictionary( set, { 'red': True }, ( ( 'size', '2XLT' ), ), cotton = True )
    >>> other_ddct
    accretive.dictionaries.ProducerDictionary( <class 'set'>, {'red': True, 'size': '2XLT', 'cotton': True} )
    >>> other_ddct[ 'inspectors' ].add( 42 )

As this is an accretive data structure, entries cannot be removed or altered,
once they have been added.

.. doctest:: ProducerDictionary

    >>> del ddct[ 'abc' ]
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'abc'.
    >>> ddct[ 'abc' ] = -1
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'abc'.
    >>> ddct
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'abc': [], 'def': [42], 'foo': 'bar'} )

The ``get`` method behaves the same as it does on the simple dictionary. I.e.,
it does not implcitly create new entries in a producer dictionary. This is the
same behavior as :py:class:`collections.defaultdict`.

.. doctest:: ProducerDictionary

    >>> ddct.get( 'fizz' )
    >>> 'fizz' in ddct
    False
    >>> ddct.get( 'fizz', 1 )
    1
    >>> 'fizz' in ddct
    False

The ``update`` method can take multiple iterables as positional arguments, as
well as keyword arguments. The iterables must either be sequences of key-value
pairs or else registered sublclasses of :py:class:`collections.abc.Mapping`.
The method returns the dictionary itself (rather than ``None``).

.. doctest:: ProducerDictionary

    >>> ddct.update( { 'ghi': 3 }, ( ( 'jkl', 3 ), ), mno = True )
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'abc': [], 'def': [42], 'foo': 'bar', 'ghi': 3, 'jkl': 3, 'mno': True} )

The ``copy`` method creates a new producer dictionary, which is initialized
with the same producer and data as the dictionary on which the method is
invoked.

.. doctest:: ProducerDictionary

    >>> type( ddct )
    <class 'accretive.dictionaries.ProducerDictionary'>
    >>> new_ddct = ddct.copy( )
    >>> type( new_ddct )
    <class 'accretive.dictionaries.ProducerDictionary'>
    >>> ddct == new_ddct
    True

Equality comparisons may be made against any registered subclass of
:py:class:`collections.abc.Mapping`. Note that the producer is excluded from
the equality comparison; only data is compared; this is the same behavior as
:py:class:`collections.defaultdict`.

.. doctest:: ProducerDictionary

    >>> other_ddct == { 'red': True, 'size': '2XLT', 'cotton': True, 'inspectors': { 42 } }
    True
