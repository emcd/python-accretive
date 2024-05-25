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


from . import __
from . import classes as _classes # pylint: disable=cyclic-import
from . import objects as _objects # pylint: disable=cyclic-import


class Omniexception(
    _objects.ConcealerObject, BaseException,
    metaclass = _classes.ConcealerClass,
):
    ''' Base for exceptions raised by package API. '''

    _attribute_visibility_includes_ = frozenset(
        ( '__cause__', '__context__', ) )


class AbsentAttributeError( Omniexception, AttributeError ):
    ''' Attempt to access absent attribute. '''

    def __init__( self, name ):
        super( ).__init__( f"Cannot access missing attribute {name!r}." )


class AbsentEntryError( Omniexception, KeyError ):
    ''' Attempt to access absent dictionary entry. '''

    def __init__( self, indicator ):
        super( ).__init__( f"Cannot access missing entry for {indicator!r}." )


class EntryIndicatorValidationFailure( Omniexception, KeyError, ValueError ):
    ''' Failure to validate dictionary entry indicator. '''

    def __init__( self, indicator ):
        super( ).__init__( f"Entry validation failed for key {indicator!r}." )


class IllegalAttributeNameError( Omniexception, AttributeError, TypeError ):
    ''' Attempt to assign attribute with illegal name. '''

    def __init__( self, name ):
        super( ).__init__( f"Cannot assign attribute with name {name!r}." )


class ImmutableAttributeError( Omniexception, AttributeError, TypeError ):
    ''' Attempt to reassign immutable attribute. '''

    def __init__( self, name ):
        super( ).__init__( f"Cannot alter existing attribute {name!r}." )


class ImmutableEntryError( Omniexception, TypeError ):
    ''' Attempt to update immutable dictionary entry. '''

    def __init__( self, indicator ):
        super( ).__init__( f"Cannot alter exsting entry for {indicator!r}." )


class IndelibleAttributeError( Omniexception, AttributeError, TypeError ):
    ''' Attempt to delete indelible attribute. '''

    def __init__( self, name ):
        super( ).__init__( f"Cannot remove existing attribute {name!r}." )


class IndelibleEntryError( Omniexception, TypeError ):
    ''' Attempt to remove indelible dictionary entry. '''

    def __init__( self, indicator ):
        super( ).__init__( f"Cannot remove existing entry for {indicator!r}." )


__all__ = __.discover_public_attributes( globals( ) )
