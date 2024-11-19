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


''' Assert correct function of namespaces. '''

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name,magic-value-comparison,protected-access


import pytest

from itertools import product

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.namespaces' ) )
THESE_CLASSES_NAMES = ( 'Namespace', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    Namespace = getattr( module, class_name )
    ns1 = Namespace( )
    assert isinstance( ns1, Namespace )
    ns2 = Namespace(
        ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True }, orb = False )
    assert isinstance( ns2, Namespace )
    assert 1 == ns2.foo
    assert 2 == ns2.bar
    assert ns2.unicorn
    assert not ns2.orb
    assert ( 'foo', 'bar', 'unicorn', 'orb' ) == tuple( ns2.__dict__.keys( ) )
    assert ( 1, 2, True, False ) == tuple( ns2.__dict__.values( ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_accretion( module_qname, class_name ):
    ''' Namespace accretes attributes. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    obj = Object( )
    obj.attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.attr = -1
    assert 42 == obj.attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.attr
    assert 42 == obj.attr


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_102_string_representation( module_qname, class_name ):
    ''' Namespace has expected string representations. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    obj = factory( )
    assert base.calculate_fqname( obj ) in repr( obj )
    obj.a = 1
    obj.b = 2
    assert 'a = 1, b = 2' in repr( obj )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_105_dictionary_equality( module_qname, class_name ):
    ''' Dictionary is equivalent to another dictionary with same values. '''
    from types import SimpleNamespace
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    ns1 = factory( foo = 1, bar = 2 )
    ns2 = factory( ns1.__dict__ )
    ns3 = SimpleNamespace( **ns1.__dict__ )
    assert ns1 == ns2
    assert ns2 == ns1
    assert ns1 == ns3
    assert ns3 == ns1
    assert not ( ns1 == -1 ) # pylint: disable=superfluous-parens
    assert ns1 != -1
    assert ns1 != ( )
    ns2.baz = 43
    assert ns1 != ns2
    assert ns2 != ns1


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
def test_901_docstring_describes_namespace( module_qname, class_name ):
    ''' Class docstring describes namespace. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'description of namespace' )
    assert fragment in Object.__doc__


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
