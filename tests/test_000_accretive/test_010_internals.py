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

# pylint: disable=magic-value-comparison,protected-access


import pytest

from types import MappingProxyType as DictionaryProxy

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__"
CONCEALER_EXTENSIONS_NAMES = (
    'ClassConcealerExtension',
    'ConcealerExtension',
)
MODULE_ATTRIBUTE_NAMES = (
    *CONCEALER_EXTENSIONS_NAMES,
    'CoreDictionary',
    'discover_fqname',
    'discover_public_attributes',
    'generate_docstring',
    'reclassify_modules',
)

_core_dictionary_posargs = (
    ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
_core_dictionary_nomargs = DictionaryProxy( dict( orb = False ) )

exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
module = cache_import_module( MODULE_QNAME )


@pytest.mark.parametrize( 'class_name', CONCEALER_EXTENSIONS_NAMES )
def test_100_concealer_extension_instantiation( class_name ):
    ''' Class instantiantes. '''
    factory = getattr( module, class_name )
    posargs = ( 'Object', ( ), { } ) if issubclass( factory, type ) else ( )
    obj = factory( *posargs )
    assert isinstance( obj, factory )


@pytest.mark.parametrize( 'class_name', CONCEALER_EXTENSIONS_NAMES )
def test_102_concealer_extension_attribute_concealment( class_name ):
    ''' Class conceals attributes. '''
    factory = getattr( module, class_name )
    posargs = ( 'Object', ( ), { } ) if issubclass( factory, type ) else ( )
    concealer_name = (
        '_class_attribute_visibility_includes_'
        if issubclass( factory, type )
        else '_attribute_visibility_includes_' )
    obj = factory( *posargs )
    assert not dir( obj )
    obj.public = 42
    assert 'public' in dir( obj )
    obj._nonpublic = 3.1415926535
    assert '_nonpublic' not in dir( obj )
    setattr( obj, concealer_name, frozenset( ( '_nonpublic', ) ) )
    assert '_nonpublic' in dir( obj )
    assert concealer_name not in dir( obj )


def test_103_class_concealer_extension_creates_classes( ):
    ''' Class factory class instances are classes. '''
    from inspect import isclass
    factory = module.ClassConcealerExtension
    assert issubclass( factory, type )
    obj = factory( 'Object', ( ), { } )
    assert isclass( obj )


def test_200_core_dictionary_instantiation( ):
    ''' Class instantiates. '''
    factory = module.CoreDictionary
    dct1 = factory( )
    assert isinstance( dct1, factory )
    dct2 = factory( *_core_dictionary_posargs, **_core_dictionary_nomargs )
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
    odct = factory( *_core_dictionary_posargs, **_core_dictionary_nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    odct[ 'baz' ] = 42
    assert odct != ddct


def test_210_core_dictionary_entry_accretion( ):
    ''' Dictionary accretes entries. '''
    factory = module.CoreDictionary
    dct = factory( *_core_dictionary_posargs, **_core_dictionary_nomargs )
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
    dct.update( *_core_dictionary_posargs, **_core_dictionary_nomargs )
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'foo' ] = 42
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'foo' ]
    dct[ 'baz' ] = 3.1415926535
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'baz' ] = -1
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]


def test_220_core_dictionary_operation_prevention( ):
    ''' Dictionary cannot perform entry deletions and mutations. '''
    factory = module.CoreDictionary
    dct = factory( *_core_dictionary_posargs, **_core_dictionary_nomargs )
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
    assert 'builtins.NoneType' == module.discover_fqname( None )
    assert (
        'builtins.type'
        == module.discover_fqname( module.ConcealerExtension ) )
    obj = module.ConcealerExtension( )
    assert (
        f"{MODULE_QNAME}.ConcealerExtension" == module.discover_fqname( obj ) )


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
    with pytest.raises( TypeError ):
        module.generate_docstring( Foo )
    assert module.generate_docstring( 'instance attributes accretion' )


def test_501_docstring_generation_validity( ):
    ''' Generated docstrings are correctly formatted. '''
    from inspect import getdoc

    class Foo:
        ''' headline

            additional information
        '''

    docstring_generated = (
        module.generate_docstring( Foo, 'class attributes accretion' ) )
    docstring_expected = '\n\n'.join( (
        getdoc( Foo ),
        module.generate_docstring( 'class attributes accretion' ) ) )
    assert docstring_expected == docstring_generated


def test_600_module_reclassification( ):
    ''' Modules are correctly reclassified. '''
    from types import ModuleType as Module
    m1 = Module( 'm1' )
    m2 = Module( 'm2' )

    class FooModule( Module ):
        ''' test '''

    m3 = FooModule( 'm3' )
    attrs = { 'bar': 42, 'orb': True, 'm1': m1, 'm2': m2, 'm3': m3 }
    assert not isinstance( m1, FooModule )
    assert not isinstance( m2, FooModule )
    assert isinstance( m3, FooModule )
    module.reclassify_modules( attrs, FooModule )
    assert isinstance( m1, FooModule )
    assert isinstance( m2, FooModule )
    assert isinstance( m3, FooModule )
