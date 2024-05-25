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
from sys import modules
from types import ModuleType as Module


class ConcealerExtension:
    ''' Conceals attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: AbstractCollection = frozenset( )

    def __dir__( self ):
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


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


__all__ = ( )
