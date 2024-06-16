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


_no_default = object( )


class Dictionary( _objects.Object ): # pylint: disable=eq-without-hash
    ''' Accretive dictionary. '''

    __slots__ = ( '_data_', )

    _data_: _Dictionary

    def __init__(
        self,
        *iterables: __.a.Annotation[
            __.a.DictionaryArgument,
            __.a.Doc(
                'Zero or more dictionaries or iterables, over key-value '
                'pairs, from which to initialize the dictionary data. '
                'Duplicate keys will result in an error.' )
        ],
        **entries: __.a.Annotation[
            __.a.Any,
            __.a.Doc(
                'Zero or more keyword arguments from which to initialize '
                'the dictionary data.' )
        ]
    ) -> None:
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

    def __eq__( self, other ):
        if isinstance( other, __.AbstractDictionary ):
            return self._data_ == other
        return NotImplemented

    def __ne__( self, other ):
        if isinstance( other, __.AbstractDictionary ):
            return self._data_ != other
        return NotImplemented

    def copy( self ):
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def get( self, key, default = _no_default ):
        ''' Retrieves entry associated with key, if it exists.

            Return default value if the entry does not exist.
            If no default value is supplied, then ``None`` is returned.
        '''
        if _no_default is default: return self._data_.get( key )
        return self._data_.get( key, default )

    def update( self, *iterables, **entries ):
        ''' Adds new entries as a batch. '''
        self._data_.update( *iterables, **entries )
        return self

    def keys( self ):
        ''' Provides iterable view over dictionary keys. '''
        return self._data_.keys( )

    def items( self ):
        ''' Provides iterable view over dictionary items. '''
        return self._data_.items( )

    def values( self ):
        ''' Provides iterable view over dictionary values. '''
        return self._data_.values( )

Dictionary.__doc__ = __.generate_docstring(
    Dictionary,
    'dictionary entries accretion',
    'instance attributes accretion',
)
# Register as subclass of AbstractDictionary rather than use it as mixin.
# We directly implement, for the sake of efficiency, the methods which the
# mixin would provide.
__.AbstractDictionary.register( Dictionary )


class ProducerDictionary( Dictionary ):
    ''' Accretive dictionary with default value for missing entries. '''

    __slots__ = ( '_producer_', )

    def __init__( self, producer, /, *iterables, **entries ):
        # TODO: Validate producer argument.
        self._producer_ = producer
        super( ).__init__( *iterables, **entries )

    def __repr__( self ):
        return "{fqname}( {producer}, {contents} )".format(
            fqname = __.discover_fqname( self ),
            producer = self._producer_,
            contents = str( self._data_ ) )

    def __getitem__( self, key ):
        if key not in self:
            value = self._producer_( )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

    def copy( self ):
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._producer_ )
        return dictionary.update( self )

ProducerDictionary.__doc__ = __.generate_docstring(
    ProducerDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'instance attributes accretion',
)


__all__ = __.discover_public_attributes( globals( ) )
