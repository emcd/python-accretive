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


class AbstractDictionary( __.cabc.Mapping[ __.H, __.V ] ):
    ''' Abstract base class for dictionaries that can grow but not shrink.

        An accretive dictionary allows new entries to be added but prevents
        modification or removal of existing entries. This provides a middle
        ground between immutable and fully mutable mappings.

        Implementations must provide:
        - __getitem__, __iter__, __len__
        - _pre_setitem_ for entry validation/preparation
        - _store_item_ for storage implementation
    '''

    @__.abstract_member_function
    def __iter__( self ) -> __.cabc.Iterator[ __.H ]:
        raise NotImplementedError # pragma: no coverage

    @__.abstract_member_function
    def __len__( self ) -> int:
        raise NotImplementedError # pragma: no coverage

    @__.abstract_member_function
    def __getitem__( self, key: __.H ) -> __.V:
        raise NotImplementedError # pragma: no coverage

    def _pre_setitem_( # pylint: disable=no-self-use
        self, key: __.H, value: __.V
    ) -> tuple[ __.H, __.V ]:
        ''' Validates and/or prepares entry before addition.

            Should raise appropriate exception if entry is invalid.
        '''
        return key, value

    @__.abstract_member_function
    def _store_item_( self, key: __.H, value: __.V ) -> None:
        ''' Stores entry in underlying storage. '''
        raise NotImplementedError # pragma: no coverage

    def __setitem__( self, key: __.H, value: __.V ) -> None:
        key, value = self._pre_setitem_( key, value )
        if key in self:
            from .exceptions import EntryImmutabilityError
            raise EntryImmutabilityError( key )
        self._store_item_( key, value )

    def __delitem__( self, key: __.H ) -> None:
        from .exceptions import EntryImmutabilityError
        raise EntryImmutabilityError( key )

    def setdefault( self, key: __.H, default: __.V ) -> __.V:
        ''' Returns value for key, setting it to default if missing. '''
        try: return self[ key ]
        except KeyError:
            self[ key ] = default
            return default

    def update(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        ''' Adds new entries as a batch. Returns self. '''
        from itertools import chain
        updates = [ ]
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, __.cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ):
            indicator_, value_ = self._pre_setitem_( indicator, value )
            if indicator_ in self:
                from .exceptions import EntryImmutabilityError
                raise EntryImmutabilityError( indicator_ )
            updates.append( ( indicator_, value_ ) )
        for indicator, value in updates: self._store_item_( indicator, value )
        return self


class _DictionaryOperations( AbstractDictionary[ __.H, __.V ] ):
    ''' Mix-in providing additional dictionary operations. '''

    def __init__( self, *posargs: __.a.Any, **nomargs: __.a.Any ) -> None:
        super( ).__init__( *posargs, **nomargs )

    def __or__( self, other: __.cabc.Mapping[ __.H, __.V ] ) -> __.a.Self:
        if not isinstance( other, __.cabc.Mapping ): return NotImplemented
        result = self.copy( )
        result.update( other )
        return result

    def __ror__( self, other: __.cabc.Mapping[ __.H, __.V ] ) -> __.a.Self:
        if not isinstance( other, __.cabc.Mapping ): return NotImplemented
        return self | other

    def __and__(
        self,
        other: __.cabc.Set[ __.H ] | __.cabc.Mapping[ __.H, __.V ]
    ) -> __.a.Self:
        if isinstance( other, __.cabc.Mapping ):
            return self.with_data(
                ( key, value ) for key, value in self.items( )
                if key in other and other[ key ] == value )
        if isinstance( other, ( __.cabc.Set, __.cabc.KeysView ) ):
            return self.with_data(
                ( key, self[ key ] ) for key in self.keys( ) & other )
        return NotImplemented

    def __rand__(
        self,
        other: __.cabc.Set[ __.H ] | __.cabc.Mapping[ __.H, __.V ]
    ) -> __.a.Self:
        if not isinstance(
            other, ( __.cabc.Mapping, __.cabc.Set, __.cabc.KeysView )
        ): return NotImplemented
        return self & other

    @__.abstract_member_function
    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        raise NotImplementedError # pragma: no coverage

    @__.abstract_member_function
    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        ''' Creates new dictionary with same behavior but different data. '''
        raise NotImplementedError # pragma: no coverage



class _Dictionary(
    __.CoreDictionary[ __.H, __.V ], metaclass = _classes.Class
): pass


class Dictionary( # pylint: disable=eq-without-hash
    _objects.Object, _DictionaryOperations[ __.H, __.V ]
):
    ''' Accretive dictionary. '''

    __slots__ = ( '_data_', )

    _data_: _Dictionary

    def __init__(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._data_ = _Dictionary( *iterables, **entries )
        super( ).__init__( )

    def __iter__( self ) -> __.cabc.Iterator[ __.H ]:
        return iter( self._data_ )

    def __len__( self ) -> int:
        return len( self._data_ )

    def __repr__( self ) -> str:
        return "{fqname}( {contents} )".format(
            fqname = __.calculate_fqname( self ),
            contents = str( self._data_ ) )

    def __str__( self ) -> str:
        return str( self._data_ )

    def __contains__( self, key: __.a.Any ) -> bool:
        return key in self._data_

    def __getitem__( self, key: __.H ) -> __.V:
        return self._data_[ key ]

    def __eq__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ == other
        return NotImplemented

    def __ne__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ != other
        return NotImplemented

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def get(
        self, key: __.H, default: __.Optional[ __.V ] = __.absent
    ) -> __.a.Annotation[
        __.V,
        __.a.Doc(
            'Value of entry, if it exists. '
            'Else, supplied default value or ``None``.' )
    ]:
        ''' Retrieves entry associated with key, if it exists. '''
        if __.is_absent( default ): return self._data_.get( key )
        return self._data_.get( key, default )

    def keys( self ) -> __.cabc.KeysView[ __.H ]:
        ''' Provides iterable view over dictionary keys. '''
        return self._data_.keys( )

    def items( self ) -> __.cabc.ItemsView[ __.H, __.V ]:
        ''' Provides iterable view over dictionary items. '''
        return self._data_.items( )

    def values( self ) -> __.cabc.ValuesView[ __.V ]:
        ''' Provides iterable view over dictionary values. '''
        return self._data_.values( )

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        return type( self )( *iterables, **entries )

    def _store_item_( self, key: __.H, value: __.V ) -> None:
        self._data_[ key ] = value

Dictionary.__doc__ = __.generate_docstring(
    Dictionary,
    'dictionary entries accretion',
    'instance attributes accretion',
)
# Register as subclass of Mapping rather than use it as mixin.
# We directly implement, for the sake of efficiency, the methods which the
# mixin would provide.
__.cabc.Mapping.register( Dictionary )


class ProducerDictionary( Dictionary[ __.H, __.V ] ):
    ''' Accretive dictionary with default value for missing entries. '''

    __slots__ = ( '_producer_', )

    _producer_: __.DictionaryProducer

    def __init__(
        self,
        producer: __.DictionaryProducer,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument
    ):
        # TODO: Validate producer argument.
        self._producer_ = producer
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {producer}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            producer = self._producer_,
            contents = str( self._data_ ) )

    def __getitem__( self, key: __.H ) -> __.V:
        if key not in self:
            value = self._producer_( )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._producer_ )
        return dictionary.update( self )

    def setdefault( self, key: __.H, default: __.V ) -> __.V:
        ''' Returns value for key, setting it to default if missing. '''
        if key not in self:
            self[ key ] = default
            return default
        return self[ key ]

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        return type( self )( self._producer_, *iterables, **entries )

ProducerDictionary.__doc__ = __.generate_docstring(
    ProducerDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'instance attributes accretion',
)


class ValidatorDictionary( Dictionary[ __.H, __.V ] ):
    ''' Accretive dictionary with validation of new entries. '''

    __slots__ = ( '_validator_', )

    _validator_: __.DictionaryValidator

    def __init__(
        self,
        validator: __.DictionaryValidator,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._validator_ = validator
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {validator}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            validator = self._validator_,
            contents = str( self._data_ ) )

    def _pre_setitem_( self, key: __.H, value: __.V ) -> tuple[ __.H, __.V ]:
        if not self._validator_( key, value ):
            from .exceptions import EntryValidityError
            raise EntryValidityError( key, value )
        return key, value

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._validator_ )
        return dictionary.update( self )

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        return type( self )( self._validator_, *iterables, **entries )

ValidatorDictionary.__doc__ = __.generate_docstring(
    ValidatorDictionary,
    'dictionary entries accretion',
    'dictionary entries validation',
    'instance attributes accretion',
)


class ProducerValidatorDictionary( Dictionary[ __.H, __.V ] ):
    ''' Accretive dictionary with defaults and validation. '''

    __slots__ = ( '_producer_', '_validator_' )

    _producer_: __.DictionaryProducer
    _validator_: __.DictionaryValidator

    def __init__(
        self,
        producer: __.DictionaryProducer,
        validator: __.DictionaryValidator,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._producer_ = producer
        self._validator_ = validator
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {producer}, {validator}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            producer = self._producer_,
            validator = self._validator_,
            contents = str( self._data_ ) )

    def __getitem__( self, key: __.H ) -> __.V:
        if key not in self:
            value = self._producer_( )
            if not self._validator_( key, value ):
                from .exceptions import EntryValidityError
                raise EntryValidityError( key, value )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

    def _pre_setitem_( self, key: __.H, value: __.V ) -> tuple[ __.H, __.V ]:
        if not self._validator_( key, value ):
            from .exceptions import EntryValidityError
            raise EntryValidityError( key, value )
        return key, value

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._producer_, self._validator_ )
        return dictionary.update( self )

    def setdefault( self, key: __.H, default: __.V ) -> __.V:
        ''' Returns value for key, setting it to default if missing. '''
        if key not in self:
            self[ key ] = default
            return default
        return self[ key ]

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        return type( self )(
            self._producer_, self._validator_, *iterables, **entries )

ProducerValidatorDictionary.__doc__ = __.generate_docstring(
    ProducerValidatorDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'dictionary entries validation',
    'instance attributes accretion',
)
