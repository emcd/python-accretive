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


import platform

from itertools import product

import pytest

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.objects' ) )
THESE_CLASSES_NAMES = ( 'Object', )


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
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
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
    ''' Object has expected string representations. '''
    module = cache_import_module( module_qname )
    base = cache_import_module( f"{PACKAGE_NAME}.__" )
    factory = getattr( module, class_name )
    obj = factory( )
    assert base.calculate_fqname( obj ) in repr( obj )


@pytest.mark.skipif(
    platform.python_implementation( ) != 'CPython',
    reason="Layout conflict specific to CPython implementation"
)
def test_150_slot_layout_conflict( ):
    ''' Object with slots cannot be used with built-in types. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    with pytest.raises( TypeError ) as excinfo:

        class ConflictingClass( BaseException, module.Object ):
            ''' This class will fail to create due to layout conflict. '''

    assert "instance lay-out conflict" in str( excinfo.value )


def test_200_accretive_decorator( ):
    ''' Accretive decorator applies accretive behavior to a class. '''
    objects_module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions_module = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    # Test with a simple class
    @objects_module.accretive
    class SimpleClass:
        def __init__( self, value = 42 ):
            self.value = value

    obj = SimpleClass( )
    assert 42 == obj.value
    obj.new_attribute = "test"  # Add new attribute
    assert "test" == obj.new_attribute

    # Test existing attribute immutability
    with pytest.raises( exceptions_module.AttributeImmutabilityError ):
        obj.value = 24
    assert 42 == obj.value

    # Test attribute deletion
    with pytest.raises( exceptions_module.AttributeImmutabilityError ):
        del obj.value


def test_201_accretive_decorator_with_dataclass( ):
    ''' Accretive decorator works with dataclass. '''
    from dataclasses import dataclass
    objects_module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions_module = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    @objects_module.accretive
    @dataclass
    class ConfigClass:
        name: str
        debug: bool = False

    config = ConfigClass( name = "test" )
    assert "test" == config.name
    assert not config.debug

    # Add new attribute
    config.verbose = True
    assert config.verbose

    # Test existing attribute immutability
    with pytest.raises( exceptions_module.AttributeImmutabilityError ):
        config.debug = True
    assert not config.debug


def test_210_accretive_decorator_compatibility_error():
    ''' Accretive decorator raises error for incompatible classes. '''
    module = cache_import_module(f"{PACKAGE_NAME}.objects")
    exceptions = cache_import_module(f"{PACKAGE_NAME}.exceptions")

    with pytest.raises(exceptions.DecoratorCompatibilityError) as excinfo:
        @module.accretive
        class TestSetattr:
            def __setattr__(self, name, value):
                pass
    assert "__setattr__" in str(excinfo.value)

    with pytest.raises(exceptions.DecoratorCompatibilityError) as excinfo:
        @module.accretive
        class TestDelattr:
            def __delattr__(self, name):
                pass
    assert "__delattr__" in str(excinfo.value)


def test_220_accretive_class_with_slots( ):
    ''' Accretive decorator works with slotted classes. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    @module.accretive
    class SlottedClass:
        __slots__ = ( '_behaviors_', 'value' )

        def __init__( self, value = 42 ):
            self.value = value

    obj = SlottedClass( 100 )
    assert 100 == obj.value
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.value = 200
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.value


def test_230_accretive_decorator_with_mutables( ):
    ''' Accretive decorator properly handles mutable attributes. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    @module.accretive( mutables = ( 'version', ) )
    class ConfigWithMutables:
        def __init__( self, name, version ):
            self.name = name
            self.version = version

    # Create instance
    config = ConfigWithMutables( 'TestApp', '1.0.0' )
    assert 'TestApp' == config.name
    assert '1.0.0' == config.version

    # Test mutable attribute
    config.version = '1.0.1'  # Should work - version is mutable
    assert '1.0.1' == config.version

    # Deleting mutable attribute should work
    del config.version
    with pytest.raises( AttributeError ):
        assert config.version

    # Test immutable attribute
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        config.name = 'NewName'


def test_231_accretive_decorator_with_docstring( ):
    ''' Accretive decorator sets custom docstring properly. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    custom_doc = 'Custom documentation for test class'

    @module.accretive( docstring = custom_doc )
    class TestDocstring:
        ''' Original docstring that should be replaced. '''

    assert custom_doc == TestDocstring.__doc__

    # Test with None docstring
    @module.accretive( docstring = None )
    class TestNoneDocstring:
        ''' Original docstring that should be replaced with None. '''

    assert TestNoneDocstring.__doc__ is None


def test_232_accretive_decorator_with_absent_docstring( ):
    ''' Accretive decorator preserves original docstring. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    base = cache_import_module( f"{PACKAGE_NAME}.__" )

    # Using the decorator with no docstring parameter should preserve original
    @module.accretive( )
    class TestPreserveDocstring:
        ''' Original docstring that should be preserved. '''

    assert (
        'Original docstring that should be preserved.'
        == TestPreserveDocstring.__doc__.strip( ) )

    # Test with explicit absent value
    @module.accretive( docstring = base.absent )
    class TestAbsentDocstring:
        ''' Original docstring should be preserved with explicit absent. '''

    assert (
        'Original docstring should be preserved with explicit absent.'
        == TestAbsentDocstring.__doc__.strip( ) )


def test_233_accretive_decorator_function_form( ):
    ''' Accretive decorator works when called with parameters but no class. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    # Create decorator with parameters
    decorator = module.accretive(
        mutables = ( 'version', ), docstring = 'Decorated class' )

    # Apply it to a class
    @decorator
    class LazyConfig:
        def __init__( self, name, version ):
            self.name = name
            self.version = version

    # Test the behavior
    config = LazyConfig( 'TestApp', '1.0.0' )

    # Mutable attribute
    config.version = '2.0.0'
    assert '2.0.0' == config.version

    # Immutable attribute
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        config.name = 'NewName'

    # Docstring set correctly
    assert 'Decorated class' == LazyConfig.__doc__


def test_234_accretive_with_multiple_parameters( ):
    ''' Accretive decorator handles multiple parameters correctly. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

    custom_doc = 'Class with multiple mutable attributes'

    @module.accretive(
        docstring = custom_doc,
        mutables = ( 'version', 'debug', 'config' )
    )
    class AdvancedConfig:
        def __init__( self, name, version, debug = False ):
            self.name = name
            self.version = version
            self.debug = debug

    # Check docstring
    assert custom_doc == AdvancedConfig.__doc__

    # Create instance
    config = AdvancedConfig( 'TestApp', '1.0.0', True )

    # Add a new mutable attribute
    config.config = { 'api_key': '12345' }

    # Modify mutable attributes
    config.version = '1.1.0'
    config.debug = False
    config.config = { 'api_key': 'updated' }

    assert '1.1.0' == config.version
    assert not config.debug
    assert { 'api_key': 'updated' } == config.config

    # Immutable attribute
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        config.name = 'NewName'


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
    base = cache_import_module( f"{PACKAGE_NAME}.__" )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes accretion' )
    assert fragment in Object.__doc__
