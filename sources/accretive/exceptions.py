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


# TODO: Immutable class attributes from class factory class.
class Omniexception( BaseException ):
    ''' Base for exceptions raised by package API. '''


class AbsentEntryError( Omniexception, KeyError ):
    ''' Attempt to access absent dictionary entry. '''

    def __init__( self, indicator ):
        super( ).__init__( f"Cannot access missing entry for {indicator!r}." )


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
