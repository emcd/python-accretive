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


class Omniexception( __.InternalObject, BaseException ):
    ''' Base for all exceptions raised by package API. '''

    _attribute_visibility_includes_: __.cabc.Collection[ str ] = (
        frozenset( ( '__cause__', '__context__', ) ) )


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''


class AttributeImmutabilityError( Omnierror, AttributeError, TypeError ):
    ''' Attempt to reassign or delete immutable attribute. '''

    def __init__( self, name: str ) -> None:
        super( ).__init__( f"Cannot reassign or delete attribute {name!r}." )


class EntryImmutabilityError( Omnierror, TypeError ):
    ''' Attempt to update or remove immutable dictionary entry. '''

    def __init__( self, indicator: __.cabc.Hashable ) -> None:
        super( ).__init__(
            f"Cannot alter or remove existing entry for {indicator!r}." )


class EntryValidityError( Omnierror, ValueError ):
    ''' Attempt to add invalid entry to dictionary. '''

    def __init__( self, indicator: __.cabc.Hashable, value: __.a.Any ) -> None:
        super( ).__init__(
            f"Cannot add invalid entry with key, {indicator!r}, "
            f"and value, {value!r}, to dictionary." )


class OperationValidityError( Omnierror, RuntimeError, TypeError ):
    ''' Attempt to perform invalid operation. '''

    def __init__( self, name: str ) -> None:
        super( ).__init__( f"Operation {name!r} is not valid on this object." )


## BEGIN: Deprecated Exceptions
# TODO: release 3.0: Remove.


class EntryValidationError( EntryValidityError ):
    ''' Attempt to add invalid entry to dictionary.

        .. deprecated:: 2.1
           Please use :py:exc:`EntryValidityError` instead.
    '''


class IndelibleAttributeError( AttributeImmutabilityError ):
    ''' Attempt to reassign or delete indelible attribute.

        .. deprecated:: 2.1
           Please use :py:exc:`AttributeImmutabilityError` instead.
    '''


class IndelibleEntryError( EntryImmutabilityError ):
    ''' Attempt to update or remove indelible dictionary entry.

        .. deprecated:: 2.1
           Please use :py:exc:`EntryImmutabilityError` instead.
    '''

    def __init__( self, indicator: __.a.Any ) -> None:
        super( ).__init__( indicator )


class InvalidOperationError( OperationValidityError ):
    ''' Attempt to perform invalid operation.

        .. deprecated:: 2.1
           Please use :py:exc:`OperationValidityError` instead.
    '''
