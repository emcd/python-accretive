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

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name,magic-value-comparison,protected-access


import pytest

from itertools import product
from types import MappingProxyType as DictionaryProxy

from . import (
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

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


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
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert isinstance( dct, factory )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct[ 'a' ] = value
    with pytest.raises( exceptions.EntryValidationError ):
        dct[ 'b' ] = 'invalid value'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_attribute_accretion( module_qname, class_name ):
    ''' Dictionary accretes attributes. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    obj = factory( *posargs, **nomargs )
    obj.attr = 42
    with pytest.raises( exceptions.IndelibleAttributeError ):
        obj.attr = -1
    assert 42 == obj.attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del obj.attr
    assert 42 == obj.attr


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, INITARGS_NAMES )
)
def test_200_dictionary_entry_accretion( module_qname, class_name ):
    ''' Dictionary accretes entries. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *simple_posargs, **simple_nomargs )
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'foo' ] = 666
    dct[ 'baz' ] = 43
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'baz' ] = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, PRODUCER_NAMES )
)
def test_201_producer_dictionary_entry_accretion( module_qname, class_name ):
    ''' Producer dictionary accretes entries. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    if class_name not in VALIDATOR_NAMES:
        dct[ 'baz' ] = 43
    else: dct[ 'baz' ] = [ 43 ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        if class_name not in VALIDATOR_NAMES:
            dct[ 'baz' ] = 42
        else: dct[ 'baz' ] = [ 43 ]
    dct[ 'abc' ].append( 12 )
    assert 12 == dct[ 'abc' ][ 0 ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'abc' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
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
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct[ 'foo' ] = value
    with pytest.raises( exceptions.EntryValidationError ):
        dct[ 'bar' ] = 'invalid value'
    with pytest.raises( exceptions.IndelibleEntryError ):
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
    factory = getattr( module, class_name )
    # Producer that returns invalid values (not a list)
    dct = factory( lambda: 42, lambda k, v: isinstance( v, list ) )
    with pytest.raises( exceptions.EntryValidationError ):
        _ = dct[ 'foo' ]  # Production should fail validation


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_210_dictionary_entry_accretion_via_update( module_qname, class_name ):
    ''' Dictionary accretes entries via update. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        if class_name not in PRODUCER_VALIDATOR_NAMES: dct[ 'foo' ] = 666
        else: dct[ 'foo' ] = [ 666 ]
    if class_name not in PRODUCER_VALIDATOR_NAMES: dct[ 'baz' ] = 43
    else: dct[ 'baz' ] = [ 43 ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
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
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    value = [ ] if class_name in PRODUCER_NAMES else 42
    dct.update( foo = value )
    with pytest.raises( exceptions.EntryValidationError ):
        dct.update( bar = 'invalid value' )
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'foo' ] = value


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
def test_225_dictionary_equality( # pylint: disable=too-many-locals
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
    assert not ( dct1 == -1 ) # pylint: disable=superfluous-parens
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
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct.update( *simple_posargs, **simple_nomargs )
    cdct = dict( dct )
    assert str( cdct ) == str( dct )
    assert str( cdct ) in repr( dct )
    assert base.discover_fqname( dct ) in repr( dct )


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
def test_250_subclasses_abc_dictionary( module_qname, class_name ):
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


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_accretion( module_qname, class_name ):
    ''' Class docstring mentions accretion. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes accretion' )
    assert fragment in factory.__doc__
