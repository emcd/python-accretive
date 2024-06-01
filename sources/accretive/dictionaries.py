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


''' Accretive dictionaries. '''


from . import __
from . import classes as _classes
from . import objects as _objects


class _Dictionary( # type: ignore
    __.CoreDictionary, metaclass = _classes.Class
): pass


class Dictionary( _objects.Object, __.AbstractDictionary ):
    ''' Accretive dictionary. '''

    __slots__ = ( '_data_', )

    def __init__( self, *iterables, **entries ):
        self._data_ = _Dictionary( *iterables, **entries )
        super( ).__init__( )

    def __iter__( self ): return iter( self._data_ )

    def __len__( self ): return len( self._data_ )

    def __repr__( self ):
        return "{fqname}( {contents} )".format(
            fqname = __.discover_fqname( self ),
            contents = str( self._data_ ) )

    def __str__( self ): return str( self._data_ )

    def __contains__( self, key ): return key in self._data_

    def __delitem__( self, key ):
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __getitem__( self, key ): return self._data_[ key ]

    def __setitem__( self, key, value ):
        self._data_[ key ] = value
        return self

    def copy( self ):
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def update( self, *iterables, **entries ):
        ''' Adds new entries as a batch. '''
        self._data_.update( *iterables, **entries )
        return self

    # TODO: Directly implement other methods for efficiency.

Dictionary.__doc__ = __.generate_docstring(
    Dictionary,
    'dictionary entries accretion',
    'instance attributes accretion',
)


class ProducerDictionary( Dictionary ):
    ''' Accretive dictionary with default value for missing entries. '''

    __slots__ = ( '_producer_', )

    def __init__( self, producer ):
        # TODO: Validate producer argument.
        self._producer_ = producer
        super( ).__init__( )

    def __getitem__( self, key ):
        if key not in self:
            value = self._producer_( )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

ProducerDictionary.__doc__ = __.generate_docstring(
    ProducerDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'instance attributes accretion',
)


__all__ = __.discover_public_attributes( globals( ) )
