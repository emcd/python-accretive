# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Common constants, imports, and utilities. '''

# ruff: noqa: F401
# pylint: disable=unused-import


import collections.abc as cabc

from abc import ABCMeta as ABCFactory
from functools import partial as partial_function
from inspect import cleandoc as clean_docstring
from sys import modules
from types import (
    MappingProxyType as DictionaryProxy,
    ModuleType as Module,
    NotImplementedType as TypeofNotImplemented,
    SimpleNamespace,
)

from . import _annotations as a


H = a.TypeVar( 'H', bound = cabc.Hashable )
V = a.TypeVar( 'V' )


ComparisonResult: a.TypeAlias = bool | TypeofNotImplemented
DictionaryNominativeArgument: a.TypeAlias = a.Annotation[
    a.Any,
    a.Doc(
        'Zero or more keyword arguments from which to initialize '
        'dictionary data.' )
]
# TODO: Support taking our dictionaries, themselves, as arguments.
#       Supposed to work via structural typing, but must match protocol.
#       https://github.com/python/mypy/issues/2922
#       https://github.com/python/mypy/issues/2922#issuecomment-1186587232
#       https://github.com/python/typing/discussions/1127#discussioncomment-2538837
#       https://mypy.readthedocs.io/en/latest/protocols.html
DictionaryPositionalArgument: a.TypeAlias = a.Annotation[
        cabc.Mapping[ cabc.Hashable, a.Any ]
    |   cabc.Iterable[ tuple[ cabc.Hashable, a.Any] ],
    a.Doc(
        'Zero or more iterables from which to initialize dictionary data. '
        'Each iterable must be dictionary or sequence of key-value pairs. '
        'Duplicate keys will result in an error.' )
]
DictionaryProducer: a.TypeAlias = a.Annotation[
    cabc.Callable[ [ ], a.Any ],
    a.Doc( 'Callable which produces values for absent dictionary entries.' )
]
ModuleReclassifier: a.TypeAlias = cabc.Callable[
    [ cabc.Mapping[ str, a.Any ] ], None ]


_no_value = object( )


class ClassConcealerExtension( type ):
    ''' Conceals class attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _class_attribute_visibility_includes_: cabc.Collection[ str ] = (
        frozenset( ) )

    def __dir__( selfclass ) -> tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in selfclass._class_attribute_visibility_includes_ ) )


class ConcealerExtension:
    ''' Conceals instance attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: cabc.Collection[ str ] = frozenset( )

    def __dir__( self ) -> tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


class CoreDictionary( ConcealerExtension, dict ): # type: ignore[type-arg]
    ''' Accretive subclass of :py:class:`dict`.

        Can be used as an instance dictionary.

        Prevents attempts to mutate dictionary via inherited interface.
    '''

    def __init__(
        self,
        *iterables: DictionaryPositionalArgument,
        **entries: DictionaryNominativeArgument
    ):
        super( ).__init__( )
        self.update( *iterables, **entries )

    def __delitem__( self, key: cabc.Hashable ) -> None:
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __setitem__( self, key: cabc.Hashable, value: a.Any ) -> None:
        from .exceptions import IndelibleEntryError
        if key in self: raise IndelibleEntryError( key )
        super( ).__setitem__( key, value )

    def clear( self ) -> a.Never:
        ''' Raises exception. Cannot clear indelible entries. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'clear' )

    def copy( self ) -> a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def pop( # pylint: disable=unused-argument
        self, key: cabc.Hashable, default: a.Any = _no_value
    ) -> a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'pop' )

    def popitem( self ) -> a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'popitem' )

    def update(
        self,
        *iterables: DictionaryPositionalArgument,
        **entries: DictionaryNominativeArgument
    ) -> a.Self:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Add values in order received, enforcing no alteration.
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ): self[ indicator ] = value
        return self


class Docstring( str ):
    ''' Dedicated docstring container. '''


def discover_fqname( obj: a.Any ) -> str:
    ''' Discovers fully-qualified name for class of instance. '''
    class_ = type( obj )
    return f"{class_.__module__}.{class_.__qualname__}"


def discover_public_attributes(
    attributes: cabc.Mapping[ str, a.Any ]
) -> tuple[ str, ... ]:
    ''' Discovers public attributes of certain types from dictionary.

        By default, callables, including classes, are discovered.
    '''
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if not name.startswith( '_' ) and callable( attribute ) ) )


def generate_docstring(
    *fragment_ids: type | Docstring | str
) -> str:
    ''' Sews together docstring fragments into clean docstring. '''
    from inspect import cleandoc, getdoc, isclass
    from ._docstrings import TABLE
    fragments = [ ]
    for fragment_id in fragment_ids:
        if isclass( fragment_id ): fragment = getdoc( fragment_id ) or ''
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = TABLE[ fragment_id ] # type: ignore
        fragments.append( cleandoc( fragment ) )
    return '\n\n'.join( fragments )
