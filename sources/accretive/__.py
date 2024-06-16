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
from collections.abc import (
    Collection as AbstractCollection,
    Mapping as AbstractDictionary,
)
from functools import partial as partial_function
from inspect import cleandoc as clean_docstring
from sys import modules
from types import (
    MappingProxyType as DictionaryProxy,
    ModuleType as Module,
)

from . import _annotations as a


_no_value = object( )


class ClassConcealerExtension( type ):
    ''' Conceals class attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _class_attribute_visibility_includes_: AbstractCollection = frozenset( )

    def __dir__( class_ ):
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in class_._class_attribute_visibility_includes_ ) )


class ConcealerExtension:
    ''' Conceals instance attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: AbstractCollection = frozenset( )

    def __dir__( self ):
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


class CoreDictionary( ConcealerExtension, dict ):
    ''' Accretive subclass of :py:class:`dict`.

        Can be used as an instance dictionary.

        Prevents attempts to mutate dictionary via inherited interface.
    '''

    def __init__( self, *iterables, **entries ):
        super( ).__init__( )
        self.update( *iterables, **entries )

    def __delitem__( self, key ):
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __setitem__( self, key, value ):
        from .exceptions import IndelibleEntryError
        if key in self: raise IndelibleEntryError( key )
        super( ).__setitem__( key, value )
        return self

    def clear( self ):
        ''' Raises exception. Cannot clear indelible entries. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'clear' )

    def copy( self ):
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def pop( # pylint: disable=unused-argument
        self, key, default = _no_value
    ):
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'pop' )

    def popitem( self ):
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'popitem' )

    def update( self, *iterables, **entries ):
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


def discover_fqname( obj ):
    ''' Discovers fully-qualified name for class of instance. '''
    class_ = type( obj )
    return f"{class_.__module__}.{class_.__qualname__}"


def discover_public_attributes( attributes ):
    ''' Discovers public attributes of certain types from dictionary.

        By default, classes and functions are discovered.
    '''
    from inspect import isclass, isfunction
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if  not name.startswith( '_' )
            and ( isclass( attribute ) or isfunction( attribute ) ) ) )


def generate_docstring( *fragment_ids ):
    ''' Sews together docstring fragments into clean docstring. '''
    from inspect import cleandoc, getdoc, isclass
    from ._docstrings import TABLE
    fragments = [ ]
    for fragment_id in fragment_ids:
        if isclass( fragment_id ): fragment = getdoc( fragment_id )
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = TABLE[ fragment_id ]
        fragments.append( cleandoc( fragment ) )
    return '\n\n'.join( fragments )


def reclassify_modules( attributes, to_class ):
    ''' Reclassifies modules in dictionary with custom module type. '''
    for attribute in attributes.values( ):
        if not isinstance( attribute, Module ): continue
        if isinstance( attribute, to_class ): continue
        attribute.__class__ = to_class


__all__ = ( )
