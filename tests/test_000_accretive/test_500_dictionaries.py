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


def _select_arguments( class_name ):
    if class_name in PRODUCER_NAMES: return ( list, ), { }
    return ( ), { }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, INITARGS_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    Dictionary = getattr( module, class_name )
    dct1 = Dictionary( )
    assert isinstance( dct1, Dictionary )
    dct2 = Dictionary(
        ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True }, orb = False )
    assert isinstance( dct2, Dictionary )
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
    Dictionary = getattr( module, class_name )
    dct = Dictionary( list )
    assert isinstance( dct, Dictionary )
    assert isinstance( dct[ 'a' ], list )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_accretion( module_qname, class_name ):
    ''' Dictionary accretes attributes. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    posargs, nomargs = _select_arguments( class_name )
    obj = Object( *posargs, **nomargs )
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
    Object = getattr( module, class_name )
    posargs, nomargs = _select_arguments( class_name )

    class Concealer( Object ):
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
    Object = getattr( module, class_name )
    posargs, nomargs = _select_arguments( class_name )

    class Concealer( Object ):
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
    Object = getattr( module, class_name )
    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.__setattr__ = None
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del Object.__setattr__
    Object.foo = 42
    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.foo = -1
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del Object.foo
    # Cleanup.
    type.__delattr__( Object, 'foo' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONPROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_151_class_attribute_nonprotection( module_qname, class_name ):
    ''' Class attributes are not protected. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    Object.foo = 42
    assert 42 == Object.foo
    Object.foo = -1
    assert -1 == Object.foo
    del Object.foo
    assert not hasattr( Object, 'foo' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    assert hasattr( Object, '__doc__' )
    assert isinstance( Object.__doc__, str )
    assert Object.__doc__


# TODO: Dictionary description.


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_accretion( module_qname, class_name ):
    ''' Class docstring mentions accretion. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes accretion' )
    assert fragment in Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_CONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_910_docstring_mentions_concealment( module_qname, class_name ):
    ''' Class docstring mentions concealment. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes concealment' )
    assert fragment in Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONCONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_911_docstring_not_mentions_concealment( module_qname, class_name ):
    ''' Class docstring does not mention concealment. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes concealment' )
    assert fragment not in Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_PROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_930_docstring_mentions_protection( module_qname, class_name ):
    ''' Class docstring mentions protection. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'protection of class' )
    assert fragment in Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_NONPROTECTION_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_931_docstring_not_mentions_protection( module_qname, class_name ):
    ''' Class docstring does not mention protection. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'protection of class' )
    assert fragment not in Object.__doc__
