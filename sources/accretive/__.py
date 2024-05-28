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


import typing as typ

from abc import ABCMeta as ABCFactory
from collections.abc import (
    Collection as AbstractCollection,
    Mapping as AbstractDictionary,
)
from functools import partial as partial_function
from sys import modules
from types import ModuleType as Module


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

    def __getattribute__( self, name ):
        from .exceptions import AbsentAttributeError
        # Mask off mutable methods from parent class.
        if name in ( 'clear', 'pop', 'popitem' ):
            raise AbsentAttributeError( name )
        return super( ).__getattribute__( name )

    def __delitem__( self, key ):
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __getitem__( self, key ):
        from .exceptions import AbsentEntryError
        if key not in self: raise AbsentEntryError( key )
        return super( ).__getitem__( key )

    def __setitem__( self, key, value ):
        from .exceptions import ImmutableEntryError
        if key in self: raise ImmutableEntryError( key )
        super( ).__setitem__( key, value )
        return self

    def copy( self ):
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

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
            iterables + ( entries, )
        ) ): self[ indicator ] = value
        return self


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


def is_python_identifier( obj ):
    ''' Is object a string which is a valid Python identifier? '''
    return isinstance( obj, str ) and obj.isidentifier( )


def reclassify_modules( attributes, to_class ):
    ''' Reclassifies modules in dictionary with custom module type. '''
    for attribute in attributes.values( ):
        if not isinstance( attribute, Module ): continue
        if isinstance( attribute, to_class ): continue
        attribute.__class__ = to_class


__all__ = ( )
