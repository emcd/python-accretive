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


''' Family of exceptions for package API. '''


from . import __ # pylint: disable=cyclic-import
from . import _annotations as _a
from . import classes as _classes # pylint: disable=cyclic-import
from . import objects as _objects # pylint: disable=cyclic-import


class _Class( __.ClassConcealerExtension, _classes.Class ): pass


class Omniexception(
    __.ConcealerExtension, _objects.Object, BaseException,
    metaclass = _Class,
):
    ''' Base for exceptions raised by package API. '''

    _attribute_visibility_includes_: _a.Collection[ str ] = (
        frozenset( ( '__cause__', '__context__', ) ) )


class IndelibleAttributeError( Omniexception, AttributeError, TypeError ):
    ''' Attempt to reassign or delete indelible attribute. '''

    def __init__( self, name: str ) -> None:
        super( ).__init__(
            f"Cannot reassign or delete existing attribute {name!r}." )


class IndelibleEntryError( Omniexception, TypeError ):
    ''' Attempt to update or remove indelible dictionary entry. '''

    def __init__( self, indicator: _a.Any ) -> None:
        super( ).__init__(
            f"Cannot update or remove existing entry for {indicator!r}." )


class InvalidOperationError( Omniexception, RuntimeError, TypeError ):
    ''' Attempt to perform invalid operation. '''

    def __init__( self, name: str ) -> None:
        super( ).__init__( f"Cannot perform operation {name!r}." )


__all__ = __.discover_public_attributes( globals( ) )
