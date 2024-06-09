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

# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name,magic-value-comparison,protected-access


import pytest

from itertools import product
from types import MappingProxyType as DictionaryProxy

from . import (
    CONCEALMENT_PACKAGES_NAMES,
    MODULES_QNAMES,
    PACKAGE_NAME,
    PROTECTION_PACKAGES_NAMES,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.dictionaries' ) )
THESE_CONCEALMENT_MODULE_QNAMES = tuple(
    name for name in THESE_MODULE_QNAMES
    if name.startswith( CONCEALMENT_PACKAGES_NAMES ) )
THESE_NONCONCEALMENT_MODULE_QNAMES = tuple(
    name for name in THESE_MODULE_QNAMES
    if not name.startswith( CONCEALMENT_PACKAGES_NAMES ) )
THESE_PROTECTION_MODULE_QNAMES = tuple(
    name for name in THESE_MODULE_QNAMES
    if name.startswith( PROTECTION_PACKAGES_NAMES ) )
THESE_NONPROTECTION_MODULE_QNAMES = tuple(
    name for name in THESE_MODULE_QNAMES
    if not name.startswith( PROTECTION_PACKAGES_NAMES ) )
INITARGS_NAMES = ( 'Dictionary', )
PRODUCER_NAMES = ( 'ProducerDictionary', )
THESE_CLASSES_NAMES = ( *INITARGS_NAMES, *PRODUCER_NAMES, )
NONPRODUCER_NAMES = tuple(
    name for name in THESE_CLASSES_NAMES
    if name not in PRODUCER_NAMES )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

simple_posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
simple_nomargs = DictionaryProxy( dict( orb = False ) )


def select_arguments( class_name ):
    ''' Choose initializer arguments depending on class. '''
    if class_name in PRODUCER_NAMES: return ( list, ), { }
    return ( ), { }


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
    dct = factory( list )
    assert isinstance( dct, factory )
    assert isinstance( dct[ 'a' ], list )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_201_duplication( module_qname, class_name ):
    ''' Dictionary is duplicable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    odct = factory( *posargs, **nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    odct[ 'baz' ] = 42
    assert odct != ddct


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
    product( THESE_CONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_120_attribute_concealment( module_qname, class_name ):
    ''' Object conceals attributes. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )

    class Concealer( factory ):
        ''' test '''
        _attribute_visibility_includes_ = frozenset( ( '_private', ) )

    obj = Concealer( *posargs, **nomargs )
    assert dir( obj )
    obj.public = 42
    assert 'public' in dir( obj )
    obj._nonpublic = 3.1415926535
    assert '_nonpublic' not in dir( obj )
    assert '_private' not in dir( obj )
    obj._private = 'foo'
    assert '_private' in dir( obj )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONCONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_121_attribute_nonconcealment( module_qname, class_name ):
    ''' Object does not conceal attributes. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )

    class Concealer( factory ):
        ''' test '''
        _attribute_visibility_includes_ = frozenset( ( '_private', ) )

    obj = Concealer( *posargs, **nomargs )
    assert '_attribute_visibility_includes_' in dir( obj )
    obj.public = 42
    assert 'public' in dir( obj )
    obj._nonpublic = 3.1415926535
    assert '_nonpublic' in dir( obj )
    assert '_private' not in dir( obj )
    obj._private = 'foo'
    assert '_private' in dir( obj )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_PROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_150_class_attribute_protection( module_qname, class_name ):
    ''' Class attributes are protected. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    with pytest.raises( exceptions.IndelibleAttributeError ):
        factory.__setattr__ = None
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del factory.__setattr__
    factory.foo = 42
    with pytest.raises( exceptions.IndelibleAttributeError ):
        factory.foo = -1
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del factory.foo
    # Cleanup.
    type.__delattr__( factory, 'foo' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONPROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_151_class_attribute_nonprotection( module_qname, class_name ):
    ''' Class attributes are not protected. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    factory.foo = 42
    assert 42 == factory.foo
    factory.foo = -1
    assert -1 == factory.foo
    del factory.foo
    assert not hasattr( factory, 'foo' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, INITARGS_NAMES )
)
def test_200_dictionary_entry_accretion( module_qname, class_name ):
    ''' Dictionary accretes entries. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
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
    dct = factory( list )
    dct[ 'baz' ] = 43
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'baz' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'baz' ] = 42
    dct[ 'abc' ].append( 12 )
    assert 12 == dct[ 'abc' ][ 0 ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        del dct[ 'abc' ]
    with pytest.raises( exceptions.IndelibleEntryError ):
        dct[ 'abc' ] = 666


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
    dct.update( *simple_posargs, **simple_nomargs )
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
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_220_dictionary_iterability( module_qname, class_name ):
    ''' Dictionary is iterable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    dct.update( *simple_posargs, **simple_nomargs )
    assert frozenset( dct.keys( ) ) == frozenset( iter( dct ) )
    assert tuple( dct.items( ) ) == tuple( zip( dct.keys( ), dct.values( ) ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_221_dictionary_measurability( module_qname, class_name ):
    ''' Dictionary is measurable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    dct.update( *simple_posargs, **simple_nomargs )
    assert len( dct.keys( ) ) == len( dct )
    assert len( dct.items( ) ) == len( dct )
    assert len( dct.values( ) ) == len( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_225_dictionary_equality( module_qname, class_name ):
    ''' Dictionary is equivalent to another dictionary with same values. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct1 = factory( *posargs, **nomargs )
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
    dct2[ 'baz' ] = 43
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
    dct.update( *simple_posargs, **simple_nomargs )
    cdct = dict( dct )
    assert str( cdct ) == str( dct )
    assert str( cdct ) in repr( dct )
    assert base.discover_fqname( dct ) in repr( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_230_dictionary_entry_optional_retrieval( module_qname, class_name ):
    ''' Default value on optional access of dictionary entry. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    dct.update( *simple_posargs, **simple_nomargs )
    assert None is dct.get( 'baz' )
    assert -1 == dct.get( 'baz', -1 )
    assert -1 == dct.get( 'baz', default = -1 )
    assert 1 == dct.get( 'foo' )
    assert 1 == dct.get( 'foo', -1 )


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


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_CONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_910_docstring_mentions_concealment( module_qname, class_name ):
    ''' Class docstring mentions concealment. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes concealment' )
    assert fragment in factory.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONCONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_911_docstring_not_mentions_concealment( module_qname, class_name ):
    ''' Class docstring does not mention concealment. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes concealment' )
    assert fragment not in factory.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_PROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_930_docstring_mentions_protection( module_qname, class_name ):
    ''' Class docstring mentions protection. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    fragment = base.generate_docstring( 'protection of class' )
    assert fragment in factory.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONPROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_931_docstring_not_mentions_protection( module_qname, class_name ):
    ''' Class docstring does not mention protection. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    fragment = base.generate_docstring( 'protection of class' )
    assert fragment not in factory.__doc__
