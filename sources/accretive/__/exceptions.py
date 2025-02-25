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


''' Family of exceptions for package internals.

    * ``Omniexception``: Base for all internal exceptions
    * ``Omnierror``: Base for all internals errors
'''


from __future__ import annotations

from . import imports as __
from . import immutables as _immutables


class Omniexception( _immutables.ImmutableObject, BaseException ):
    ''' Base for all exceptions raised internally. '''

    _attribute_visibility_includes_: __.cabc.Collection[ str ] = (
        frozenset( ( '__cause__', '__context__', ) ) )


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised internally. '''


class EntryImmutabilityError( Omnierror, TypeError ):
    ''' Attempt to update or remove immutable dictionary entry. '''

    def __init__( self, indicator: __.cabc.Hashable ) -> None:
        super( ).__init__(
            f"Cannot alter or remove existing entry for {indicator!r}." )


class OperationInvalidity( Omnierror, RuntimeError, TypeError ):
    ''' Attempt to perform invalid operation. '''

    def __init__( self, name: str ) -> None:
        super( ).__init__( f"Operation {name!r} is not valid on this object." )
