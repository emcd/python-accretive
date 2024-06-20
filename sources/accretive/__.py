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


from abc import ABCMeta as ABCFactory
from collections.abc import Mapping as AbstractDictionary
from functools import partial as partial_function
from inspect import cleandoc as clean_docstring
from sys import modules
from types import (
    MappingProxyType as DictionaryProxy,
    ModuleType as Module,
    SimpleNamespace,
)

from . import _annotations as _a


_no_value = object( )


class ClassConcealerExtension( type ):
    ''' Conceals class attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _class_attribute_visibility_includes_: _a.Collection[ str ] = frozenset( )

    def __dir__( class_ ) -> _a.Tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in class_._class_attribute_visibility_includes_ ) )


class ConcealerExtension:
    ''' Conceals instance attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: _a.Collection[ str ] = frozenset( )

    def __dir__( self ) -> _a.Tuple[ str, ... ]:
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
        *iterables: _a.DictionaryPositionalArgument,
        **entries: _a.DictionaryNominativeArgument
    ):
        super( ).__init__( )
        self.update( *iterables, **entries )

    def __delitem__( self, key: _a.Hashable ) -> None:
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __setitem__( self, key: _a.Hashable, value: _a.Any ) -> None:
        from .exceptions import IndelibleEntryError
        if key in self: raise IndelibleEntryError( key )
        super( ).__setitem__( key, value )

    def clear( self ) -> _a.Never:
        ''' Raises exception. Cannot clear indelible entries. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'clear' )

    def copy( self ) -> _a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def pop( # pylint: disable=unused-argument
        self, key: _a.Hashable, default: _a.Any = _no_value
    ) -> _a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'pop' )

    def popitem( self ) -> _a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'popitem' )

    def update( # type: ignore[override]
        self,
        *iterables: _a.DictionaryPositionalArgument,
        **entries: _a.DictionaryNominativeArgument
    ) -> _a.Self:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Add values in order received, enforcing no alteration.
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, AbstractDictionary )
                else element
            ),
            ( *iterables, entries )
        ) ): self[ indicator ] = value
        return self


class Docstring( str ):
    ''' Dedicated docstring container. '''


def discover_fqname( obj: _a.Any ) -> str:
    ''' Discovers fully-qualified name for class of instance. '''
    class_ = type( obj )
    return f"{class_.__module__}.{class_.__qualname__}"


def discover_public_attributes(
    attributes: _a.Mapping[ str, _a.Any ]
) -> _a.Tuple[ str, ... ]:
    ''' Discovers public attributes of certain types from dictionary.

        By default, callables, including classes, are discovered.
    '''
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if not name.startswith( '_' ) and callable( attribute ) ) )


def generate_docstring(
    *fragment_ids: _a.Union[ _a.Type, Docstring, str ]
) -> str:
    ''' Sews together docstring fragments into clean docstring. '''
    from inspect import cleandoc, getdoc, isclass
    from ._docstrings import TABLE
    fragments = [ ]
    for fragment_id in fragment_ids:
        if isclass( fragment_id ): fragment = getdoc( fragment_id ) or ''
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = TABLE[ fragment_id ]
        fragments.append( cleandoc( fragment ) )
    return '\n\n'.join( fragments )


def reclassify_modules(
    attributes: _a.Mapping[ str, _a.Any ],
    to_class: _a.Type[ Module ]
) -> None:
    ''' Reclassifies modules in dictionary with custom module type. '''
    for attribute in attributes.values( ):
        if not isinstance( attribute, Module ): continue
        if isinstance( attribute, to_class ): continue
        attribute.__class__ = to_class


__all__ = ( )
