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


_accretion_function_names = (
    '_delitem_', '_getitem_', '_iter_', '_len_', '_setitem_', '_str_' )


class Dictionary(
    _objects.ConcealerObject, __.AbstractDictionary,
    metaclass = _classes.ConcealerABCFactory,
):
    ''' Simple accretive dictionary.

        An accretive dictionary only accepts new entries; attempts to alter or
        delete existing entries result in errors. '''

    __slots__ = _accretion_function_names

    def __init__( self, *iterables, **entries ):
        from itertools import chain
        _inject_accretion_functions( self )
        # Add values in order received, enforcing no alteration.
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, __.AbstractDictionary )
                else element
            ),
            iterables + ( entries, )
        ) ): self[ indicator ] = value
        super( ).__init__( )

    # pylint: disable=no-member

    def __repr__( self ):
        return "{fqname}( {contents} )".format(
            fqname = __.discover_fqname( self ),
            contents = self._str_( ) )

    def __str__( self ): return self._str_( )

    def __iter__( self ): return self._iter_( )

    def __len__( self ): return self._len_( )

    def __delitem__( self, key ):
        self._delitem_( key )
        return self

    def __getitem__( self, key ): return self._getitem_( key )

    def __setitem__( self, key, value ):
        self._setitem_( key, value )
        return self

    # pylint: enable=no-member


class ProducerDictionary( Dictionary ):
    ''' Accretive dictionary which produces values for missing entries.

        Accretive equivalent to 'collections.defaultdict'. '''

    __slots__ = ( '_producer', )

    def __init__( self, producer ):
        # TODO: Validate producer argument.
        self._producer = producer
        super( ).__init__( )

    def __getitem__( self, key ):
        from .exceptions import AbsentEntryError
        try: return super( ).__getitem__( key )
        except AbsentEntryError:
            self[ key ] = value = self._producer( )
            return value


def _inject_accretion_functions( owner ): # pylint: disable=too-complex,too-many-locals
    from .exceptions import (
        AbsentEntryError, ImmutableEntryError, IndelibleEntryError
    )
    dictionary = { }

    # pylint: disable=possibly-unused-variable

    def _str_( ): return str( dictionary )

    def _iter_( ): return iter( dictionary )

    def _len_( ): return len( dictionary )

    def _delitem_( indicator ):
        if indicator not in dictionary:
            raise AbsentEntryError( indicator )
        raise IndelibleEntryError( indicator )

    def _getitem_( indicator ):
        if indicator not in dictionary:
            raise AbsentEntryError( indicator )
        return dictionary[ indicator ]

    def _setitem_( indicator, value ):
        if indicator in dictionary:
            raise ImmutableEntryError( indicator )
        dictionary[ indicator ] = value

    # pylint: enable=possibly-unused-variable

    for name in _accretion_function_names:
        setattr( owner, name, locals( )[ name ] )
    return owner


__all__ = __.discover_public_attributes( globals( ) )
