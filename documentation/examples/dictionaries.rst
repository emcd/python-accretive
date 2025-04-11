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


Dictionaries
===============================================================================


Simple Dictionary
-------------------------------------------------------------------------------

Simple accretive dictionaries have an interface nearly equivalent to
:py:class:`dict`. Because of their accretive nature, they can be useful as
registries for extensions, handlers, and plugins, such that something that is
registered is guaranteed to remain registered throughout the lifetime of the
registry.

.. doctest:: Dictionary

    >>> from accretive import Dictionary

Let us illustrate this use case by first defining some handlers to register.

.. doctest:: Dictionary

    >>> def csv_reader( stream ): pass
    ...
    >>> def env_reader( stream ): pass
    ...
    >>> def hcl_reader( stream ): pass
    ...
    >>> def ini_reader( stream ): pass
    ...
    >>> def json_reader( stream ): pass
    ...
    >>> def toml_reader( stream ): pass
    ...
    >>> def xml_reader( stream ): pass
    ...
    >>> def yaml_reader( stream ): pass
    ...

Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple dictionaries can be initialized from zero or more other dictionaries
or iterables over key-value pairs and zero or more keyword arguments.

.. doctest:: Dictionary

    >>> readers = Dictionary( { 'csv': csv_reader }, ( ( 'json', json_reader ), ( 'xml', xml_reader ) ), yaml = yaml_reader )
    >>> readers
    accretive.dictionaries.Dictionary( {'csv': <function csv_reader at 0x...>, 'json': <function json_reader at 0x...>, 'xml': <function xml_reader at 0x...>, 'yaml': <function yaml_reader at 0x...>} )

Immutability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Existing entries cannot be altered.

.. doctest:: Dictionary

    >>> readers[ 'xml' ] = toml_reader
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryImmutabilityError: Cannot alter or remove existing entry for 'xml'.

Or removed.

.. doctest:: Dictionary

    >>> del readers[ 'xml' ]
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryImmutabilityError: Cannot alter or remove existing entry for 'xml'.

(Seems like XML is here to stay.)

Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However, new entries can be added individually or in bulk. Bulk entry is via
the ``update`` method.

.. doctest:: Dictionary

    >>> readers.update( ( ( 'env', env_reader ), ( 'hcl', hcl_reader ) ), { 'ini': ini_reader }, toml = toml_reader )
    accretive.dictionaries.Dictionary( {'csv': <function csv_reader at 0x...>, 'json': <function json_reader at 0x...>, 'xml': <function xml_reader at 0x...>, 'yaml': <function yaml_reader at 0x...>, 'env': <function env_reader at 0x...>, 'hcl': <function hcl_reader at 0x...>, 'ini': <function ini_reader at 0x...>, 'toml': <function toml_reader at 0x...>} )

.. note::

    The ``update`` method returns the dictionary itself. This is different than
    the behavior of :py:class:`dict`, which returns ``None`` instead. Returning
    the dictionary is a more useful behavior, since it allows for call chaining
    as a fluent setter.

Copies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copies can be made which preserve behavior and data.

.. doctest:: Dictionary

    >>> dct1 = Dictionary( answer = 42 )
    >>> dct2 = dct1.copy( )

Copies can also be made which preserve behavior but replace data. These are
made using the ``with_data`` method, which creates a new dictionary of the same
type but with different data. This is particularly useful with producer and
validator dictionaries (see below) as it preserves their behavior:

.. doctest:: Dictionary

    >>> base = Dictionary( a = 1, b = 2 )
    >>> new = base.with_data( x = 3, y = 4 )
    >>> new
    accretive.dictionaries.Dictionary( {'x': 3, 'y': 4} )

Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The copies are equivalent to their originals.

.. doctest:: Dictionary

    >>> dct1 == dct2
    True

And to instances of other registered subclasses of
:py:class:`collections.abc.Mapping` which have equivalent data.

.. doctest:: Dictionary

    >>> dct2 == { 'answer': 42 }
    True

Modifying a copy causes it to become non-equivalent, as expected.

.. doctest:: Dictionary

    >>> dct2[ 'question' ] = 'is reality a quine of itself?'
    >>> dct1 == dct2
    False
    >>> dct2 != { 'answer': 42 }
    True

Access of Absent Entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with :py:class:`dict`, a missing entry will raise a :py:exc:`KeyError`.

.. doctest:: Dictionary

    >>> dct1[ 'question' ]
    Traceback (most recent call last):
    KeyError: 'question'

And, like :py:class:`dict`, the ``get`` method allows for "soft" accesses which
provide a default value if an entry is missing.

.. doctest:: Dictionary

    >>> dct1.get( 'question' )
    >>> dct1.get( 'question', 'what is the meaning of life?' )
    'what is the meaning of life?'

Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The usual methods for producing views on items, keys, and values exist.

.. doctest:: Dictionary

    >>> tuple( readers.keys( ) )
    ('csv', 'json', 'xml', 'yaml', 'env', 'hcl', 'ini', 'toml')
    >>> tuple( readers.items( ) ) == tuple( zip( readers.keys( ), readers.values( ) ) )
    True

Unions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The union operator (``|``) combines entries from two dictionaries or a
dictionary and a mapping, creating a new dictionary. The operation maintains
the accretive contract by preventing duplicate keys:

.. doctest:: Dictionary

    >>> formats = Dictionary( csv = csv_reader, json = json_reader )
    >>> more_formats = Dictionary( yaml = yaml_reader, toml = toml_reader )
    >>> all_formats = formats | more_formats
    >>> all_formats
    accretive.dictionaries.Dictionary( {'csv': <function csv_reader at 0x...>, 'json': <function json_reader at 0x...>, 'yaml': <function yaml_reader at 0x...>, 'toml': <function toml_reader at 0x...>} )

When operands have overlapping keys, an error is raised:

.. doctest:: Dictionary

    >>> conflicting = Dictionary( json = yaml_reader )
    >>> formats | conflicting
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryImmutabilityError: Cannot alter or remove existing entry for 'json'.

Intersections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The intersection operator (``&``) can be used in two ways:

1. With another mapping to keep entries with matching key-value pairs:

.. doctest:: Dictionary

    >>> d1 = Dictionary( a = 1, b = 2, c = 3 )
    >>> d2 = Dictionary( a = 1, b = 3, d = 4 )  # Note: b has different value
    >>> d1 & d2  # Only entries that match exactly
    accretive.dictionaries.Dictionary( {'a': 1} )

2. With a set or keys view to filter entries by keys:

.. doctest:: Dictionary

    >>> allowed = { 'a', 'b' }
    >>> d3 = d1 & allowed  # Keep only entries with allowed keys
    >>> 'c' in d3
    False


Producer Dictionary
-------------------------------------------------------------------------------

Producer dictionaries have an interface nearly equivalent to
:py:class:`collections.defaultdict`. The first argument to the initializer for
a producer dictionary must be a callable which can be invoked with no
arguments. This callable is used to create entries that are absent at lookup
time. Any additional arguments beyond the first one are treated the same as for
the simple dictionary. Most of their behaviors are the same as for the simple
dictionary, except as noted below.

.. doctest:: ProducerDictionary

    >>> from accretive import ProducerDictionary

Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A common use case is to automatically initialize a mutable data structure, such
as a :py:class:`list`, and add elements or entries to it by merely referencing
its corresponding key... without checking whether the entry exists or creating
the entry first.

.. doctest:: ProducerDictionary

    >>> watch_lists = ProducerDictionary( list )
    >>> watch_lists
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {} )

Production of Absent Entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. doctest:: ProducerDictionary

    >>> watch_lists[ 'FBI: Most Wanted' ]
    []
    >>> watch_lists
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'FBI: Most Wanted': []} )
    >>> watch_lists[ 'Santa Claus: Naughty' ].append( 'Calvin' )
    >>> watch_lists
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'FBI: Most Wanted': [], 'Santa Claus: Naughty': ['Calvin']} )

Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. doctest:: ProducerDictionary

    >>> watch_lists.update( { 'US Commerce: Do Not Call': [ 'me' ] }, Tasks = set( ) )
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'FBI: Most Wanted': [], 'Santa Claus: Naughty': ['Calvin'], 'US Commerce: Do Not Call': ['me'], 'Tasks': set()} )

Access of Absent Entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``get`` method behaves the same as it does on the simple dictionary. I.e.,
it does not implcitly create new entries in a producer dictionary. This is the
same behavior as :py:class:`collections.defaultdict`.

.. doctest:: ProducerDictionary

    >>> watch_lists.get( 'TSA: No Fly' )
    >>> watch_lists.get( 'TSA: No Fly', 'Richard Reid' )
    'Richard Reid'
    >>> watch_lists
    accretive.dictionaries.ProducerDictionary( <class 'list'>, {'FBI: Most Wanted': [], 'Santa Claus: Naughty': ['Calvin'], 'US Commerce: Do Not Call': ['me'], 'Tasks': set()} )

Copies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``copy`` method creates a new producer dictionary, which is initialized
with the same producer and data as the dictionary on which the method is
invoked.

.. doctest:: ProducerDictionary

    >>> ddct1 = ProducerDictionary( lambda: 42, { 'foo': 1, 'bar': 2 }, orb = True )
    >>> ddct1
    accretive.dictionaries.ProducerDictionary( <function <lambda> at 0x...>, {'foo': 1, 'bar': 2, 'orb': True} )
    >>> ddct2 = ddct1.copy( )
    >>> ddct2
    accretive.dictionaries.ProducerDictionary( <function <lambda> at 0x...>, {'foo': 1, 'bar': 2, 'orb': True} )

Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Equality comparisons may be made against any registered subclass of
:py:class:`collections.abc.Mapping`. Note that the producer is excluded from
the equality comparison; only data is compared; this is the same behavior as
:py:class:`collections.defaultdict`.

.. doctest:: ProducerDictionary

    >>> ddct2 == { 'foo': 1, 'bar': 2, 'orb': True }
    True

Validator Dictionary
-------------------------------------------------------------------------------

Validator dictionaries ensure that all entries satisfy specified criteria. The first
argument to the initializer must be a callable which accepts a key and value and
returns a boolean indicating whether the entry is valid. Any additional arguments
are treated the same as for the simple dictionary.

.. doctest:: ValidatorDictionary

    >>> from accretive import ValidatorDictionary

Let us illustrate this with a dictionary that only accepts integer values.

.. doctest:: ValidatorDictionary

    >>> numbers = ValidatorDictionary( lambda k, v: isinstance( v, int ) )
    >>> numbers[ 'answer' ] = 42
    >>> numbers[ 'pi' ] = 3
    >>> numbers
    accretive.dictionaries.ValidatorDictionary( <function <lambda> at 0x...>, {'answer': 42, 'pi': 3} )

Invalid entries are rejected.

.. doctest:: ValidatorDictionary

    >>> numbers[ 'e' ] = 2.718
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryValidityError: Cannot add invalid entry with key, 'e', and value, 2.718, to dictionary.

This includes attempts to add invalid entries via update.

.. doctest:: ValidatorDictionary

    >>> numbers.update( phi = 1.618 )
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryValidityError: Cannot add invalid entry with key, 'phi', and value, 1.618, to dictionary.

Producer-Validator Dictionary
-------------------------------------------------------------------------------

Producer-validator dictionaries combine the behaviors of producer and validator
dictionaries. The first argument must be a producer callable, and the second
must be a validator callable. Any additional arguments are treated the same as
for the simple dictionary.

.. doctest:: ProducerValidatorDictionary

    >>> from accretive import ProducerValidatorDictionary

A common use case is to automatically initialize data structures of a specific
type while ensuring that only those types can be stored.

.. doctest:: ProducerValidatorDictionary

    >>> registries = ProducerValidatorDictionary(
    ...     list,
    ...     lambda k, v: isinstance( v, list )
    ... )
    >>> registries
    accretive.dictionaries.ProducerValidatorDictionary( <class 'list'>, <function <lambda> at 0x...>, {} )

The producer must create values that satisfy the validator.

.. doctest:: ProducerValidatorDictionary

    >>> handlers = registries[ 'handlers' ]  # Produces new list
    >>> handlers.append( 'default_handler' )
    >>> registries[ 'plugins' ] = [ ]  # Valid manual assignment
    >>> registries
    accretive.dictionaries.ProducerValidatorDictionary( <class 'list'>, <function <lambda> at 0x...>, {'handlers': ['default_handler'], 'plugins': []} )

Invalid entries are rejected, whether assigned directly or via update.

.. doctest:: ProducerValidatorDictionary

    >>> registries[ 'modules' ] = { }  # Not a list
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryValidityError: Cannot add invalid entry with key, 'modules', and value, {}, to dictionary.
    >>> registries.update( callbacks = set( ) )  # Not a list
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryValidityError: Cannot add invalid entry with key, 'callbacks', and value, set(), to dictionary.

If the producer returns an invalid value, the entry is rejected.

.. doctest:: ProducerValidatorDictionary

    >>> bad_registries = ProducerValidatorDictionary(
    ...     dict,  # Produces dictionaries
    ...     lambda k, v: isinstance( v, list )  # Requires lists
    ... )
    >>> bad_registries[ 'anything' ]  # Production fails validation
    Traceback (most recent call last):
    ...
    accretive.exceptions.EntryValidityError: Cannot add invalid entry with key, 'anything', and value, {}, to dictionary.
