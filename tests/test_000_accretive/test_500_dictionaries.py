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


''' Assert correct function of dictionaries. '''


from itertools import product
from types import MappingProxyType as DictionaryProxy

import pytest

from .__ import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)

THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.dictionaries' ) )
INITARGS_NAMES = ( 'Dictionary', )
VALIDATOR_NAMES = ( 'ValidatorDictionary', 'ProducerValidatorDictionary' )
PRODUCER_NAMES = ( 'ProducerDictionary', 'ProducerValidatorDictionary' )
THESE_CLASSES_NAMES = ( *INITARGS_NAMES, *PRODUCER_NAMES, *VALIDATOR_NAMES )
PRODUCER_VALIDATOR_NAMES = tuple(
    name for name in THESE_CLASSES_NAMES
    if name in PRODUCER_NAMES and name in VALIDATOR_NAMES )



def select_arguments( class_name ):
    ''' Chooses initializer arguments depending on class. '''
    if class_name in PRODUCER_NAMES:
        if class_name in VALIDATOR_NAMES:
            return ( list, lambda k, v: isinstance( v, list ), ), { }
        return ( list, ), { }
    if class_name in VALIDATOR_NAMES:
        return ( lambda k, v: isinstance( v, int ), ), { }
    return ( ), { }


def select_simple_arguments( class_name ):
    ''' Choose simple test arguments depending on class. '''
    posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
    nomargs = DictionaryProxy( dict( orb = False ) )
    if class_name in PRODUCER_NAMES:
        if class_name in VALIDATOR_NAMES:
            posargs = (
                ( ( 'foo', [ 1 ] ), ( 'bar', [ 2 ] ) ), { 'unicorn': [ ] } )
            nomargs = DictionaryProxy( dict( orb = [ ] ) )
            return posargs, nomargs
        return posargs, nomargs
    if class_name in VALIDATOR_NAMES:
        posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': 42 } )
        nomargs = DictionaryProxy( dict( orb = 84 ) )
        return posargs, nomargs
    return posargs, nomargs


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, INITARGS_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    dct1 = factory( )
    assert isinstance( dct1, factory )
    dct2 = factory(
        ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True }, orb = False )
    assert isinstance( dct2, factory )
    assert 1 == dct2[ 'foo' ]
    assert 2 == dct2[ 'bar' ]
    assert dct2[ 'unicorn' ]
    assert not dct2[ 'orb' ]
    assert ( 'foo', 'bar', 'unicorn', 'orb' ) == tuple( dct2.keys( ) )
    assert ( 1, 2, True, False ) == tuple( dct2.values( ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, PRODUCER_NAMES )
)
def test_101_instantiation( module_qname, class_name ):
    ''' Producer class instantiates. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert isinstance( dct, factory )
    assert isinstance( dct[ 'a' ], list )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, VALIDATOR_NAMES )
)
def test_102_instantiation( module_qname, class_name ):
    ''' Validator class instantiates. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert isinstance( dct, factory )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct[ 'a' ] = value
    with pytest.raises( exceptions.EntryInvalidity ):
        dct[ 'b' ] = 'invalid value'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, INITARGS_NAMES )
)
def test_200_dictionary_entry_accretion( module_qname, class_name ):
    ''' Dictionary accretes entries. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *simple_posargs, **simple_nomargs )
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'foo' ] = 666
    dct[ 'baz' ] = 43
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'baz' ] = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_150_setdefault_preserves_existing_entry( module_qname, class_name ):
    ''' Setdefault returns existing value without modification. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    # Add initial value
    if class_name in PRODUCER_NAMES:
        dct[ 'a' ] = [ 1 ]
        assert [ 1 ] == dct.setdefault( 'a', [ 42 ] )
        assert [ 1 ] == dct[ 'a' ]
    else:
        dct[ 'a' ] = 1
        assert 1 == dct.setdefault( 'a', 42 )
        assert 1 == dct[ 'a' ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_151_setdefault_adds_missing_entry( module_qname, class_name ):
    ''' Setdefault adds new entry for missing key. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    if class_name in PRODUCER_NAMES:
        assert [ 42 ] == dct.setdefault( 'b', [ 42 ] )
        assert [ 42 ] == dct[ 'b' ]
    else:
        assert 42 == dct.setdefault( 'b', 42 )
        assert 42 == dct[ 'b' ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_160_or_combines_dictionaries( module_qname, class_name ):
    ''' Dictionary union produces new dictionary with combined entries. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, **nomargs )
    d2 = factory( *posargs, **nomargs )
    d3 = { }
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d1[ 'a' ] = [ 1 ]
        d2[ 'c' ] = [ 4 ]
        d3.update( d = [ 5 ], e = [ 6 ] )
    else:
        d1[ 'a' ] = 1
        d2[ 'c' ] = 4
        d3.update( d = 5, e = 6 )
    d4 = d1 | d2
    assert isinstance( d4, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d4 == { 'a': [ 1 ], 'c': [ 4 ] }
    else: assert d4 == { 'a': 1, 'c': 4 }
    d5 = d1 | d3
    assert isinstance( d5, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d5 == { 'a': [ 1 ], 'd': [ 5 ], 'e': [ 6 ] }
    else: assert d5 == { 'a': 1, 'd': 5, 'e': 6 }
    d6 = d3 | d1
    assert isinstance( d6, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d6 == { 'a': [ 1 ], 'd': [ 5 ], 'e': [ 6 ] }
    else: assert d6 == { 'a': 1, 'd': 5, 'e': 6 }
    d7 = factory( *posargs, **nomargs )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d7[ 'a' ] = [ 2 ]
    else: d7[ 'a' ] = 2
    with pytest.raises( exceptions.EntryImmutability ):
        _ = d1 | d7


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_161_or_rejects_invalid_operands( module_qname, class_name ):
    ''' Dictionary union rejects non-mapping operands. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert NotImplemented == dct.__or__( [ ] )
    assert NotImplemented == dct.__ror__( [ ] )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_170_and_intersects_mappings( module_qname, class_name ):
    ''' Dictionary intersection with mapping matches key-value pairs. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, **nomargs )
    d2 = factory( *posargs, **nomargs )
    d3 = { }
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d1.update( a = [ 1 ], b = [ 2 ], c = [ 3 ] )
        d2.update( a = [ 1 ], b = [ 3 ], d = [ 4 ] )
        d3.update( a = [ 1 ], c = [ 3 ], e = [ 5 ] )
    else:
        d1.update( a = 1, b = 2, c = 3 )
        d2.update( a = 1, b = 3, d = 4 )
        d3.update( a = 1, c = 3, e = 5 )
    d4 = d1 & d2
    assert isinstance( d4, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d4 == { 'a': [ 1 ] }
    else: assert d4 == { 'a': 1 }
    d5 = d1 & d3
    assert isinstance( d5, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d5 == { 'a': [ 1 ], 'c': [ 3 ] }
    else: assert d5 == { 'a': 1, 'c': 3 }
    d6 = d3 & d1
    assert isinstance( d6, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d6 == { 'a': [ 1 ], 'c': [ 3 ] }
    else: assert d6 == { 'a': 1, 'c': 3 }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_171_and_filters_by_keys( module_qname, class_name ):
    ''' Dictionary intersection with set filters by keys. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, **nomargs )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d1.update( a = [ 1 ], b = [ 2 ], c = [ 3 ] )
    else: d1.update( a = 1, b = 2, c = 3 )
    s1 = { 'a', 'b' }
    d2 = d1 & s1
    assert isinstance( d2, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d2 == { 'a': [ 1 ], 'b': [ 2 ] }
    else: assert d2 == { 'a': 1, 'b': 2 }
    d3 = d1 & factory( *posargs, x = [ 0 ], a = [ 9 ], b = [ 8 ] ).keys( )
    assert isinstance( d3, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d3 == { 'a': [ 1 ], 'b': [ 2 ] }
    else: assert d3 == { 'a': 1, 'b': 2 }
    d4 = s1 & d1
    assert isinstance( d4, factory )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d4 == { 'a': [ 1 ], 'b': [ 2 ] }
    else: assert d4 == { 'a': 1, 'b': 2 }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_172_and_rejects_invalid_operands( module_qname, class_name ):
    ''' Dictionary intersection rejects invalid operands. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert NotImplemented == dct.__and__( [ ] )
    assert NotImplemented == dct.__rand__( [ ] )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_180_operations_preserve_accretion( module_qname, class_name ):
    ''' Dictionary operations maintain accretive contract. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, **nomargs )
    d2 = factory( *posargs, **nomargs )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d1[ 'a' ] = [ 1 ]
        d2[ 'a' ] = [ 2 ]
    else:
        d1[ 'a' ] = 1
        d2[ 'a' ] = 2
    with pytest.raises( exceptions.EntryImmutability ): d1 | d2
    d4 = d1 & { 'a' }
    with pytest.raises( exceptions.EntryImmutability ):
        if class_name in PRODUCER_VALIDATOR_NAMES:
            d4[ 'a' ] = [ 3 ]
        else: d4[ 'a' ] = 3


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, PRODUCER_NAMES )
)
def test_201_producer_dictionary_entry_accretion( module_qname, class_name ):
    ''' Producer dictionary accretes entries. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    if class_name not in VALIDATOR_NAMES:
        dct[ 'baz' ] = 43
    else: dct[ 'baz' ] = [ 43 ]
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.EntryImmutability ):
        if class_name not in VALIDATOR_NAMES:
            dct[ 'baz' ] = 42
        else: dct[ 'baz' ] = [ 43 ]
    dct[ 'abc' ].append( 12 )
    assert 12 == dct[ 'abc' ][ 0 ]
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'abc' ]
    with pytest.raises( exceptions.EntryImmutability ):
        if class_name not in VALIDATOR_NAMES:
            dct[ 'abc' ] = 666
        else: dct[ 'abc' ] = [ 666 ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, VALIDATOR_NAMES )
)
def test_202_validator_dictionary_entry_accretion( module_qname, class_name ):
    ''' Validator dictionary accretes valid entries only. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct[ 'foo' ] = value
    with pytest.raises( exceptions.EntryInvalidity ):
        dct[ 'bar' ] = 'invalid value'
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'foo' ] = value
    if class_name in PRODUCER_NAMES:
        lst = dct[ 'baz' ]
        assert isinstance( lst, list )
        lst.append( 42 )
        assert 42 == dct[ 'baz' ][ 0 ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, PRODUCER_VALIDATOR_NAMES )
)
def test_205_producer_validator_invalid_production( module_qname, class_name ):
    ''' Producer-validator dictionary rejects invalid produced values. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    # Producer that returns invalid values (not a list)
    dct = factory( lambda: 42, lambda k, v: isinstance( v, list ) )
    with pytest.raises( exceptions.EntryInvalidity ):
        _ = dct[ 'foo' ]  # Production should fail validation


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_210_dictionary_entry_accretion_via_update( module_qname, class_name ):
    ''' Dictionary accretes entries via update. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.EntryImmutability ):
        if class_name not in PRODUCER_VALIDATOR_NAMES: dct[ 'foo' ] = 666
        else: dct[ 'foo' ] = [ 666 ]
    if class_name not in PRODUCER_VALIDATOR_NAMES: dct[ 'baz' ] = 43
    else: dct[ 'baz' ] = [ 43 ]
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.EntryImmutability ):
        if class_name not in PRODUCER_VALIDATOR_NAMES: dct[ 'baz' ] = 42
        else: dct[ 'baz' ] = [ 42 ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, VALIDATOR_NAMES )
)
def test_211_validator_dictionary_entry_accretion_via_update(
    module_qname, class_name
):
    ''' Validator dictionary accretes valid entries via update. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct.update( foo = value )
    with pytest.raises( exceptions.EntryInvalidity ):
        dct.update( bar = 'invalid value' )
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'foo' ] = value


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_212_update_with_existing_key_raises_immutability_error(
    module_qname, class_name
):
    ''' Update raises EntryImmutability for existing keys. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dictionary = factory( *posargs, **nomargs )
    if class_name in PRODUCER_NAMES:
        dictionary[ 'existing_key' ] = [ 1 ]
        new_value = [ 999 ]
        new_key_value = [ 100 ]
    else:
        dictionary[ 'existing_key' ] = 42
        new_value = 999
        new_key_value = 100
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary.update( [ ( 'existing_key', new_value ) ] )
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary.update( existing_key = new_value )
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary.update(
            [ ( 'new_key', new_key_value ), ( 'existing_key', new_value ) ] )
    assert dictionary[ 'existing_key' ] == (
        [ 1 ] if class_name in PRODUCER_NAMES else 42 )

@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_213_update_with_empty_inputs( module_qname, class_name ):
    ''' Update behavior with empty or no inputs. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dictionary = factory( *posargs, **nomargs )
    initial_length = len( dictionary )
    dictionary.update( )
    assert len( dictionary ) == initial_length
    dictionary.update( [ ], **{ } )
    assert len( dictionary ) == initial_length


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_214_update_with_invalid_inputs( module_qname, class_name ):
    ''' Update behavior with invalid (non-iterable/non-mapping) inputs. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dictionary = factory( *posargs, **nomargs )
    with pytest.raises( TypeError ):
        dictionary.update( 42 )  # Non-iterable input
    with pytest.raises( TypeError ):
        dictionary.update( None )  # Non-iterable input (None is not iterable)
    with pytest.raises( TypeError ):
        dictionary.update( [ 1, 2, 3 ] )  # List without key-value pairs


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_216_update_with_pre_setitem_modification( module_qname, class_name ):
    ''' Update behavior with _pre_setitem_ modifying indicator or value. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )

    class ModifiedDictionary( factory ):
        def _pre_setitem_( self, key, value ):
            return str( key ) if isinstance( key, int ) else key, value + 1

    dictionary = ModifiedDictionary( *posargs, **nomargs )
    dictionary.update( [ ( 'test_key', 10 ) ] )
    assert dictionary[ 'test_key' ] == 11


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_220_duplication( module_qname, class_name ):
    ''' Dictionary is duplicable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    odct = factory( *posargs, **nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    if class_name in PRODUCER_NAMES:
        odct[ 'baz' ] = [ 42 ]
    else: odct[ 'baz' ] = 42
    assert odct != ddct


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_221_dictionary_iterability( module_qname, class_name ):
    ''' Dictionary is iterable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    assert frozenset( dct.keys( ) ) == frozenset( iter( dct ) )
    assert tuple( dct.items( ) ) == tuple( zip( dct.keys( ), dct.values( ) ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_222_dictionary_measurability( module_qname, class_name ):
    ''' Dictionary is measurable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    assert len( dct.keys( ) ) == len( dct )
    assert len( dct.items( ) ) == len( dct )
    assert len( dct.values( ) ) == len( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_225_dictionary_equality(
    module_qname, class_name
):
    ''' Dictionary is equivalent to another dictionary with same values. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct1 = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct1.update( *simple_posargs, **simple_nomargs )
    dct2 = dct1.copy( )
    dct3 = dict( dct1 )
    assert dct1 == dct2
    assert dct2 == dct1
    assert dct1 == dct3
    assert dct3 == dct1
    assert not ( dct1 == -1 ) # noqa: SIM201
    assert dct1 != -1
    assert dct1 != ( )
    if class_name not in PRODUCER_VALIDATOR_NAMES: dct2[ 'baz' ] = 43
    else: dct2[ 'baz' ] = [ 43 ]
    assert dct1 != dct2
    assert dct2 != dct1


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_230_string_representation( module_qname, class_name ):
    ''' Dictionary has expected string representations. '''
    module = cache_import_module( module_qname )
    base = cache_import_module( f"{PACKAGE_NAME}.__" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    cdct = dict( dct )
    assert str( cdct ) == str( dct )
    assert str( cdct ) in repr( dct )
    assert base.ccutils.qualify_class_name( type( dct ) ) in repr( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_240_dictionary_entry_optional_retrieval( module_qname, class_name ):
    ''' Default value on optional access of dictionary entry. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    assert None is dct.get( 'baz' )
    assert -1 == dct.get( 'baz', -1 )
    assert -1 == dct.get( 'baz', default = -1 )
    if class_name not in PRODUCER_VALIDATOR_NAMES:
        assert 1 == dct.get( 'foo' )
        assert 1 == dct.get( 'foo', -1 )
    else:
        assert [ 1 ] == dct.get( 'foo' )
        assert [ 1 ] == dct.get( 'foo', -1 )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_250_with_data( module_qname, class_name ):
    ''' Dictionary creates new instance with different data. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, **nomargs )
    if class_name in PRODUCER_VALIDATOR_NAMES:
        d1[ 'a' ] = [ 1 ]
        d1[ 'b' ] = [ 2 ]
        new_data = { 'c': [ 3 ], 'd': [ 4 ] }
    else:
        d1[ 'a' ] = 1
        d1[ 'b' ] = 2
        new_data = { 'c': 3, 'd': 4 }
    d2 = d1.with_data( new_data )
    assert isinstance( d2, factory )
    assert type( d1 ) is type( d2 )
    assert d1 != d2
    if class_name in PRODUCER_VALIDATOR_NAMES:
        assert d2 == { 'c': [ 3 ], 'd': [ 4 ] }
    else: assert d2 == { 'c': 3, 'd': 4 }
    if class_name in PRODUCER_NAMES:
        assert isinstance( d2[ 'x' ], list )
    if class_name in VALIDATOR_NAMES:
        with pytest.raises( exceptions.EntryInvalidity ):
            d2[ 'y' ] = 'invalid'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_260_subclasses_abc_dictionary( module_qname, class_name ):
    ''' Subclasses 'collections.abc.Mapping'. '''
    from collections.abc import Mapping as AbstractDictionary
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    issubclass( factory, AbstractDictionary )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    assert hasattr( factory, '__doc__' )
    assert isinstance( factory.__doc__, str )
    assert factory.__doc__


# TODO: Dictionary description.
