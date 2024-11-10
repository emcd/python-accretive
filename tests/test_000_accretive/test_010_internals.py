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


''' Assert correct function of internals. '''

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=magic-value-comparison
# pylint: disable=missing-class-docstring
# pylint: disable=protected-access
# ruff: noqa: E711,E712


import pytest

from platform import python_implementation
from types import MappingProxyType as DictionaryProxy

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__"
MODULE_ATTRIBUTE_NAMES = (
    'Absent',
    'ConcealerExtension',
    'CoreDictionary',
    'Docstring',
    'Falsifier',
    'InternalClass',
    'InternalObject',
    #'absent',
    'calculate_class_fqname',
    'calculate_fqname',
    'discover_public_attributes',
    'generate_docstring',
)

exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
module = cache_import_module( MODULE_QNAME )

dictionary_posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
dictionary_nomargs = DictionaryProxy( dict( orb = False ) )

pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently"
)


def test_102_concealer_extension_attribute_visibility( ):
    ''' Instance conceals attributes according to visibility rules. '''
    obj = module.ConcealerExtension( )
    obj.public = 42
    assert ( 'public', ) == tuple( dir( obj ) )
    obj._hidden = 24
    assert ( 'public', ) == tuple( dir( obj ) )
    obj._visible = 12
    obj._attribute_visibility_includes_ = frozenset( ( '_visible', ) )
    assert ( '_visible', 'public' ) == tuple( sorted( dir( obj ) ) )


def test_111_internal_class_immutability( ):
    ''' Class attributes become immutable after initialization. '''
    factory = module.InternalClass
    class Example( metaclass = factory ): value = 42
    with pytest.raises( AttributeError ): Example.value = 24
    with pytest.raises( AttributeError ): del Example.value


def test_112_internal_class_decorator_handling( ):
    ''' Class properly handles decorators during creation. '''
    factory = module.InternalClass
    def decorator1( cls ):
        cls.attr1 = 'one'
        return cls
    def decorator2( cls ):
        cls.attr2 = 'two'
        return cls

    class Example(
        metaclass = factory, decorators = ( decorator1, decorator2 )
    ): pass

    assert 'one' == Example.attr1
    assert 'two' == Example.attr2 # pylint: disable=no-member
    with pytest.raises( AttributeError ): Example.attr1 = 'changed'


def test_113_internal_class_attribute_visibility( ):
    ''' Class conceals attributes according to visibility rules. '''
    factory = module.InternalClass

    class Example( metaclass = factory ):
        _class_attribute_visibility_includes_ = frozenset( ( '_visible', ) )
        public = 42
        _hidden = 24
        _visible = 12

    assert ( '_visible', 'public' ) == tuple( sorted( dir( Example ) ) )


@pypy_skip_mark
def test_114_internal_class_decorator_replacement( ):
    ''' Class properly handles decorators that return new classes. '''
    from dataclasses import dataclass
    factory = module.InternalClass

    class Example(
        metaclass = factory, decorators = ( dataclass( slots = True ), )
    ):
        field1: str
        field2: int

    assert hasattr( Example, '__slots__' )
    with pytest.raises( AttributeError ): Example.field1 = 'changed'


def test_115_internal_class_behaviors_extension( ):
    ''' Class properly extends existing behaviors. '''
    factory = module.InternalClass

    class Base( metaclass = factory ):
        _class_behaviors_ = { 'existing' }

    assert 'existing' in Base._class_behaviors_
    assert module._immutability_label in Base._class_behaviors_


def test_150_internal_object_immutability( ):
    ''' Instance attributes cannot be modified or deleted. '''
    class Example( module.InternalObject ):
        def __init__( self ):
            # Need to bypass normal setattr to initialize
            super( module.InternalObject, self ).__setattr__( 'value', 42 )

    obj = Example( )
    with pytest.raises( AttributeError ): obj.value = 24
    with pytest.raises( AttributeError ): obj.new_attr = 'test'
    with pytest.raises( AttributeError ): del obj.value


def test_160_falsifier_behavior( ):
    ''' Falsifier objects are falsey and compare properly. '''
    class Example( module.Falsifier ): pass

    obj1 = Example( )
    obj2 = Example( )
    assert not obj1
    assert obj1 == obj1 # pylint: disable=comparison-with-itself
    assert obj1 != obj2
    assert obj1 is not True
    assert obj1 is not False
    assert obj1 is not None


def test_170_absent_singleton( ):
    ''' Absent class produces singleton instance. '''
    obj1 = module.Absent( )
    obj2 = module.Absent( )
    assert obj1 is obj2
    assert obj1 is module.absent
    assert not obj1
    assert obj1 == obj1 # pylint: disable=comparison-with-itself
    assert obj1 != None # pylint: disable=singleton-comparison
    assert obj1 != False # pylint: disable=singleton-comparison


def test_171_absent_type_guard( ):
    ''' Type guard correctly identifies absent values. '''
    def example( value: module.Optional[ str ] ) -> str:
        if not module.is_absent( value ): return value
        return 'default'

    assert 'test' == example( 'test' )
    assert 'default' == example( module.absent )


def test_200_core_dictionary_instantiation( ):
    ''' Class instantiates. '''
    factory = module.CoreDictionary
    dct1 = factory( )
    assert isinstance( dct1, factory )
    dct2 = factory( *dictionary_posargs, **dictionary_nomargs )
    assert isinstance( dct2, factory )
    assert 1 == dct2[ 'foo' ]
    assert 2 == dct2[ 'bar' ]
    assert dct2[ 'unicorn' ]
    assert not dct2[ 'orb' ]
    assert ( 'foo', 'bar', 'unicorn', 'orb' ) == tuple( dct2.keys( ) )
    assert ( 1, 2, True, False ) == tuple( dct2.values( ) )


def test_201_core_dictionary_duplication( ):
    ''' Dictionary is duplicable. '''
    factory = module.CoreDictionary
    odct = factory( *dictionary_posargs, **dictionary_nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    odct[ 'baz' ] = 42
    assert odct != ddct


def test_210_core_dictionary_entry_accretion( ):
    ''' Dictionary accretes entries. '''
    factory = module.CoreDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'foo' ] = 42
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'foo' ]
    dct[ 'baz' ] = 3.1415926535
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'baz' ] = -1
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]


def test_211_core_dictionary_entry_accretion_via_update( ):
    ''' Dictionary accretes entries via update. '''
    factory = module.CoreDictionary
    dct = factory( )
    dct.update( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'foo' ] = 42
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'foo' ]
    dct[ 'baz' ] = 3.1415926535
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'baz' ] = -1
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]


def test_212_core_dictionary_update_validation( ):
    ''' Dictionary update properly handles various input types. '''
    factory = module.CoreDictionary
    dct = factory( )
    dct.update( { 'a': 1, 'b': 2 } )
    assert 1 == dct[ 'a' ]
    dct.update( [ ( 'c', 3 ), ( 'd', 4 ) ] )
    assert 3 == dct[ 'c' ]
    dct.update( e = 5, f = 6 )
    assert 5 == dct[ 'e' ]
    dct.update( { 'g': 7 }, [ ( 'h', 8 ) ], i = 9 )
    assert 7 == dct[ 'g' ]
    assert 8 == dct[ 'h' ]
    assert 9 == dct[ 'i' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct.update( { 'a': 10 } )


def test_220_core_dictionary_operation_prevention( ):
    ''' Dictionary cannot perform entry deletions and mutations. '''
    factory = module.CoreDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.InvalidOperationError ):
        dct.clear( )
    with pytest.raises( exceptions.InvalidOperationError ):
        dct.pop( 'foo' )
    with pytest.raises( exceptions.InvalidOperationError ):
        dct.pop( 'foo', default = -1 )
    with pytest.raises( exceptions.InvalidOperationError ):
        dct.pop( 'baz' )
    with pytest.raises( exceptions.InvalidOperationError ):
        dct.popitem( )


def test_300_fqname_discovery( ):
    ''' Fully-qualified name of object is discovered. '''
    assert 'builtins.NoneType' == module.calculate_fqname( None )
    assert (
        'builtins.type'
        == module.calculate_fqname( module.ConcealerExtension ) )
    obj = module.ConcealerExtension( )
    assert (
        f"{MODULE_QNAME}.ConcealerExtension"
        == module.calculate_fqname( obj ) )


@pytest.mark.parametrize(
    'provided, expected',
    (
        ( { 'foo': 12 }, ( ) ),
        ( { '_foo': cache_import_module }, ( ) ),
        (
            { name: getattr( module, name )
              for name in MODULE_ATTRIBUTE_NAMES },
            MODULE_ATTRIBUTE_NAMES
        ),
    )
)
def test_400_public_attribute_discovery( provided, expected ):
    ''' Public attributes are discovered from dictionary. '''
    assert expected == module.discover_public_attributes( provided )


def test_500_docstring_generation_argument_acceptance( ):
    ''' Docstring generator errors on invalid arguments. '''
    class Foo: pass # pylint: disable=missing-class-docstring
    with pytest.raises( KeyError ):
        module.generate_docstring( 1 )
    with pytest.raises( KeyError ):
        module.generate_docstring( '8-bit theater' )
    assert not module.generate_docstring( Foo )
    assert module.generate_docstring( 'instance attributes accretion' )
    assert module.generate_docstring( module.Docstring( 'foo bar' ) )


def test_501_docstring_generation_validity( ):
    ''' Generated docstrings are correctly formatted. '''
    from inspect import getdoc

    class Foo:
        ''' headline

            additional information
        '''

    docstring_generated = module.generate_docstring(
        Foo,
        module.Docstring( 'foo bar' ),
        'class attributes accretion' )
    docstring_expected = '\n\n'.join( (
        getdoc( Foo ),
        'foo bar',
        module.generate_docstring( 'class attributes accretion' ) ) )
    assert docstring_expected == docstring_generated
