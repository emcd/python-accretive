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


''' Assert correct function of objects. '''

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
    name for name in MODULES_QNAMES if name.endswith( '.objects' ) )
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
THESE_CLASSES_NAMES = ( 'Object', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    obj = Object( )
    assert isinstance( obj, Object )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_accretion( module_qname, class_name ):
    ''' Object accretes attributes. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    obj = Object( )
    obj.attr = 42
    with pytest.raises( exceptions.IndelibleAttributeError ):
        obj.attr = -1
    assert 42 == obj.attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del obj.attr
    assert 42 == obj.attr


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_102_string_representation( module_qname, class_name ):
    ''' Object has expected string representations. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    obj = factory( )
    assert base.discover_fqname( obj ) in repr( obj )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_CONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_attribute_concealment( module_qname, class_name ):
    ''' Object conceals attributes. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )

    class Concealer( Object ):
        ''' test '''
        _attribute_visibility_includes_ = frozenset( ( '_private', ) )

    obj = Concealer( )
    assert not dir( obj )
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
def test_111_attribute_nonconcealment( module_qname, class_name ):
    ''' Object does not conceal attributes. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )

    class Concealer( Object ):
        ''' test '''
        _attribute_visibility_includes_ = frozenset( ( '_private', ) )

    obj = Concealer( )
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
