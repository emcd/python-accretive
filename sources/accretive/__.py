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

# pylint: disable=unused-import


import typing as typ

from abc import ABCMeta as ABCFactory
from collections.abc import (
    Mapping as AbstractDictionary,
)
from sys import modules
from types import ModuleType as Module


class ConcealerExtension:
    ''' Conceals attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_ = frozenset( )

    def __dir__( self ):
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


def discover_fqname( obj, module_name = __package__ ):
    ''' Discovers fully-qualified name of class.

        If given an instance, then the fully-qualified name of the class, to
        which the instance belongs, is returned.
    '''
    from inspect import isclass
    return "{module_name}.{qname}".format(
        module_name = module_name,
        qname = (
            obj.__qualname__ if isclass( obj )
            else type( obj ).__qualname__ ) )


def discover_public_attributes( attributes ):
    ''' Discovers public attributes of certain types from dictionary.

        By default, classes and functions are discovered.
    '''
    from inspect import isclass, isfunction
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if  not name.startswith( '_' )
            and ( isclass( attribute ) or isfunction( attribute ) ) ) )
