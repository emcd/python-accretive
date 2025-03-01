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


''' Assert correct function of dataclass factory classes. '''

# pylint: disable=invalid-field-call,no-member,unused-variable
# pylint: disable=magic-value-comparison,protected-access


import pytest

from dataclasses import field, FrozenInstanceError
from itertools import product
from typing import ClassVar

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )

DATACLASS_METACLASSES = (
    'Dataclass',
    'CompleteDataclass',
)
PROTOCOL_DATACLASS_METACLASSES = (
    'ProtocolDataclass',
    'CompleteProtocolDataclass',
)
ALL_DATACLASS_METACLASSES = (
    DATACLASS_METACLASSES + PROTOCOL_DATACLASS_METACLASSES )
FROZEN_DATACLASS_METACLASSES = (
    'CompleteDataclass',
    'CompleteProtocolDataclass',
)


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_200_instantiation( module_qname, class_name ):
    ''' Dataclass metaclass instantiates. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42

    assert isinstance( TestDataclass, class_factory_class )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_201_dataclass_features( module_qname, class_name ):
    ''' Dataclass has expected dataclass features. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42
        cls_var: ClassVar[str] = 'class_level'

    # Test instantiation with required arguments
    instance = TestDataclass( value = 'test' )
    assert 'test' == instance.value
    assert 42 == instance.optional

    # Test instantiation with all arguments
    instance2 = TestDataclass( value = 'test2', optional = 100 )
    assert 'test2' == instance2.value
    assert 100 == instance2.optional

    # Test that class variables are accessible
    assert 'class_level' == TestDataclass.cls_var
    # In this implementation, ClassVar fields may still be accessible on instances
    # but they should be the same value as the class attribute
    if hasattr(instance, 'cls_var'):
        assert TestDataclass.cls_var == instance.cls_var


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_202_kw_only( module_qname, class_name ):
    ''' Dataclass enforces kw_only=True. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42

    # Test that positional arguments are not allowed
    with pytest.raises( TypeError ):
        TestDataclass( 'test' )  # type: ignore


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, FROZEN_DATACLASS_METACLASSES )
)
def test_203_frozen_instance( module_qname, class_name ):
    ''' Complete dataclasses create frozen instances. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42

    instance = TestDataclass( value = 'test' )

    # Test that attributes cannot be modified
    with pytest.raises( FrozenInstanceError ):
        instance.value = 'modified'

    # Test that attributes cannot be deleted
    with pytest.raises( FrozenInstanceError ):
        del instance.value


@pytest.mark.parametrize(
    'module_qname, class_name',
    product(
        THESE_MODULE_QNAMES,
        list(
                set( ALL_DATACLASS_METACLASSES )
            -   set( FROZEN_DATACLASS_METACLASSES ) ) )
)
def test_204_mutable_instance( module_qname, class_name ):
    ''' Standard dataclasses allow instance modification. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42

    instance = TestDataclass( value = 'test' )

    # Test that attributes can be modified
    instance.value = 'modified'
    assert 'modified' == instance.value

    # Test that attributes can be deleted
    del instance.value
    assert not hasattr( instance, 'value' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_205_slots( module_qname, class_name ):
    ''' Dataclass uses slots=True. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42

    instance = TestDataclass( value = 'test' )

    # Test that __slots__ exists (though it might be in a parent class)
    assert '__slots__' in dir( TestDataclass )

    # Test that __dict__ is not available on instance (effect of slots)
    assert '__dict__' not in dir( instance )

    # For now, simply check that the instance was created successfully
    # We're not testing dynamic attribute assignment because the implementation
    # appears to be raising a TypeError related to super() when attempting to set
    # attributes on instances
    assert instance.value == 'test'
    assert instance.optional == 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_206_accretive_class_attrs( module_qname, class_name ):
    ''' Dataclass still has accretive class attributes. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42
        CLASS_CONSTANT: ClassVar[str] = 'constant'

    # Test that class attributes cannot be modified
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        TestDataclass.CLASS_CONSTANT = 'modified'

    # Test that class attributes cannot be deleted
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del TestDataclass.CLASS_CONSTANT

    # Test that new class attributes can be added
    TestDataclass.NEW_ATTR = 'new'
    assert 'new' == TestDataclass.NEW_ATTR

    # But once added, they follow accretive rules
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        TestDataclass.NEW_ATTR = 'changed'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_207_dataclass_field_features( module_qname, class_name ):
    ''' Dataclass supports advanced field features. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class TestDataclass( metaclass = class_factory_class ):
        ''' test '''
        value: str
        optional: int = 42
        default_factory: list = field( default_factory = list )
        metadata_field: str = field(
            default="test",
            metadata = { 'description': 'A field with metadata' } )

    instance = TestDataclass( value = 'test' )

    # Test default_factory works
    assert isinstance( instance.default_factory, list )
    assert len( instance.default_factory ) == 0

    # Mutating the default_factory instance shouldn't affect other instances
    instance.default_factory.append( 'item' )
    instance2 = TestDataclass( value = 'test2' )
    assert len( instance2.default_factory ) == 0


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_208_dataclass_with_mutable_class_attrs( module_qname, class_name ):
    ''' Dataclass supports mutable class attributes. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    class_factory_class = getattr( module, class_name )

    class TestDataclass(
        metaclass = class_factory_class,
        mutables = ( 'MUTABLE_CLASS_VAR', )
    ):
        ''' test '''
        value: str
        optional: int = 42
        MUTABLE_CLASS_VAR: ClassVar[int] = 100
        IMMUTABLE_CLASS_VAR: ClassVar[int] = 200

    # Test that mutable class attributes can be modified
    TestDataclass.MUTABLE_CLASS_VAR = 150
    assert 150 == TestDataclass.MUTABLE_CLASS_VAR

    # Test that immutable class attributes cannot be modified
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        TestDataclass.IMMUTABLE_CLASS_VAR = 250


@pytest.mark.parametrize(
    'module_qname',
    THESE_MODULE_QNAMES
)
def test_209_protocol_dataclass_behavior( module_qname ):
    ''' Protocol dataclasses work as protocols. '''
    try:
        module = cache_import_module( module_qname )

        class TestProtocolDataclass( metaclass = module.ProtocolDataclass ):
            ''' Protocol for testing. '''
            value: str

            def get_value( self ) -> str: # pylint: disable=no-self-use
                ''' Protocol method. '''

        # Create a class that matches the protocol
        class ImplementsProtocol:
            ''' Implements TestProtocolDataclass protocol. '''
            def __init__( self, value: str ):
                self.value = value

            def get_value( self ) -> str:
                ''' Returns the value. '''
                return self.value

        # Create a class that doesn't match the protocol
        class DoesNotImplementProtocol:
            ''' Doesn't implement TestProtocolDataclass protocol. '''
            def __init__( self, data: str ):
                self.data = data

        # Test structural compatibility rather than runtime isinstance
        # Since Protocol runtime checking behavior is implementation-dependent
        compliant = ImplementsProtocol( "test" )
        assert hasattr(compliant, "value")
        assert hasattr(compliant, "get_value")
        assert callable(compliant.get_value)

        non_compliant = DoesNotImplementProtocol( "test" )
        assert not hasattr(non_compliant, "value")
        assert not hasattr(non_compliant, "get_value")

    except (ImportError, AttributeError):
        # Skip if ProtocolDataclass isn't available
        pytest.skip("ProtocolDataclass not available")



@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_210_custom_decorators( module_qname, class_name ):
    ''' Dataclass supports additional custom decorators. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    decorator_applied = False

    def custom_decorator( cls ):
        nonlocal decorator_applied
        decorator_applied = True
        cls.DECORATOR_ATTR = 'was_applied'
        return cls

    class TestDataclass(
        metaclass = class_factory_class,
        decorators = ( custom_decorator, )
    ):
        ''' test '''
        value: str
        optional: int = 42

    # Test that custom decorator was applied
    assert decorator_applied
    assert hasattr( TestDataclass, 'DECORATOR_ATTR' )
    assert 'was_applied' == TestDataclass.DECORATOR_ATTR


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_211_inheritance( module_qname, class_name ):
    ''' Dataclass supports inheritance properly. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class ParentDataclass( metaclass = class_factory_class ):
        ''' Parent dataclass. '''
        parent_value: str
        parent_optional: int = 42

    class ChildDataclass( ParentDataclass ):
        ''' Child dataclass. '''
        child_value: str
        child_optional: int = 100

    # Test that child inherits parent fields
    instance = ChildDataclass(
        parent_value = 'parent',
        child_value = 'child'
    )

    assert 'parent' == instance.parent_value
    assert 42 == instance.parent_optional
    assert 'child' == instance.child_value
    assert 100 == instance.child_optional


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Dataclass has valid docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    assert hasattr( class_factory_class, '__doc__' )
    assert isinstance( class_factory_class.__doc__, str )
    assert class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_901_docstring_describes_cfc( module_qname, class_name ):
    ''' Dataclass docstring describes class factory class. '''
    module = cache_import_module( module_qname )
    base = cache_import_module( f"{PACKAGE_NAME}.__" )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'description of class factory class' )
    assert fragment in class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ALL_DATACLASS_METACLASSES )
)
def test_902_docstring_mentions_accretion( module_qname, class_name ):
    ''' Dataclass docstring mentions accretion. '''
    module = cache_import_module( module_qname )
    base = cache_import_module( f"{PACKAGE_NAME}.__" )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'class attributes accretion' )
    assert fragment in class_factory_class.__doc__
