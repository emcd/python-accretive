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


''' Assert correct function of class factory classes. '''


from itertools import product
from platform import python_implementation

import pytest

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )
THESE_CLASSES_NAMES = (
    'Class', 'AbstractBaseClass', 'ProtocolClass', )
    # 'Class', 'Dataclass', 'AbstractBaseClass',
    # 'ProtocolClass', 'ProtocolDataclass' )


pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently"
)


@pytest.mark.parametrize( 'module_qname', THESE_MODULE_QNAMES )
@pytest.mark.parametrize( 'class_name', THESE_CLASSES_NAMES )
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''
        x: int

    assert isinstance( Object, class_factory_class )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_accretion( module_qname, class_name ):
    ''' Class accretes attributes. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''
        attr = 42

    with pytest.raises( exceptions.AttributeImmutability ):
        Object.attr = -1
    assert 42 == Object.attr
    with pytest.raises( exceptions.AttributeImmutability ):
        del Object.attr
    assert 42 == Object.attr
    Object.accreted_attr = 'foo'
    assert 'foo' == Object.accreted_attr
    with pytest.raises( exceptions.AttributeImmutability ):
        Object.accreted_attr = 'bar'
    assert 'foo' == Object.accreted_attr
    with pytest.raises( exceptions.AttributeImmutability ):
        del Object.accreted_attr
    assert 'foo' == Object.accreted_attr


# @pytest.mark.parametrize(
#     'module_qname, class_name',
#     product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
# )
# def test_110_class_decorators( module_qname, class_name ):
#     ''' Class accepts and applies decorators correctly. '''
#     module = cache_import_module( module_qname )
#     exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
#     class_factory_class = getattr( module, class_name )
#     decorator_calls = [ ]
#
#     def test_decorator1( cls ):
#         decorator_calls.append( 'decorator1' )
#         cls.decorator1_attr = 'value1'
#         return cls
#
#     def test_decorator2( cls ):
#         decorator_calls.append( 'decorator2' )
#         cls.decorator2_attr = 'value2'
#         return cls
#
#     class Object(
#         metaclass = class_factory_class,
#         decorators = ( test_decorator1, test_decorator2 )
#     ):
#         ''' test '''
#         attr = 42
#
#         _class_behaviors_: typx.ClassVar[ set[ str ] ] = { 'foo' }
#
#     assert [ 'decorator1', 'decorator2' ] == decorator_calls
#     assert 'value1' == Object.decorator1_attr
#     assert 'value2' == Object.decorator2_attr
#     with pytest.raises( exceptions.AttributeImmutability ):
#         Object.decorator1_attr = 'new_value'
#     with pytest.raises( exceptions.AttributeImmutability ):
#         Object.decorator2_attr = 'new_value'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_114_decorator_error_handling( module_qname, class_name ):
    ''' Class handles decorator errors appropriately. '''
    module = cache_import_module( module_qname )
    class_factory_class = ( getattr( module, class_name ) )

    def failing_decorator( cls ):
        raise ValueError( "Decorator failure" )

    with pytest.raises( ValueError, match = "Decorator failure" ):
        class Object(
            metaclass = class_factory_class,
            decorators = ( failing_decorator, )
        ):
            ''' test '''


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_115_mutable_attributes( module_qname, class_name ):
    ''' Mutable attributes behavior via mutables parameter. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    class_factory_class = getattr( module, class_name )

    class MutableObject(
        metaclass = class_factory_class,
        class_mutables = ( 'mutable_attr', )
    ):
        ''' test '''
        immutable_attr = 42
        mutable_attr = 100

    with pytest.raises( exceptions.AttributeImmutability ):
        MutableObject.immutable_attr = 43
    assert 42 == MutableObject.immutable_attr
    with pytest.raises( exceptions.AttributeImmutability ):
        del MutableObject.immutable_attr
    assert 42 == MutableObject.immutable_attr
    MutableObject.mutable_attr = 200
    assert 200 == MutableObject.mutable_attr
    del MutableObject.mutable_attr
    assert 'mutable_attr' not in MutableObject.__dict__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product(
        ( qname for qname in MODULES_QNAMES if qname.endswith( '.classes' ) ),
        ( 'Object', 'ObjectMutable',
          'DataclassObject', 'DataclassObjectMutable',
          'Protocol', 'ProtocolMutable',
          'DataclassProtocol', 'DataclassProtocolMutable' )
    )
)
def test_130_object_instantiation( module_qname, class_name ):
    ''' Object class instantiates. '''
    module = cache_import_module( module_qname )
    object_class = getattr( module, class_name )
    assert isinstance( object_class, type )


@pytest.mark.parametrize(
    'module_qname, decorator_name',
    product(
        ( qname for qname in MODULES_QNAMES if qname.endswith( '.classes' ) ),
        ( 'dataclass_with_standard_behaviors', 'with_standard_behaviors' )
    )
)
def test_140_decorator_instantiation( module_qname, decorator_name ):
    ''' Decorator class instantiates. '''
    module = cache_import_module( module_qname )
    decorator_class = getattr( module, decorator_name )
    assert callable( decorator_class )


@pytest.mark.parametrize(
    'module_qname, decorator_name',
    product(
        ( qname for qname in MODULES_QNAMES if qname.endswith( '.classes' ) ),
        ( 'dataclass_with_standard_behaviors', ) # 'with_standard_behaviors' )
    )
)
def test_141_decorator_application( module_qname, decorator_name ):
    ''' Decorator class applies to class. '''
    module = cache_import_module( module_qname )
    decorator = getattr( module, decorator_name )
    @decorator
    class Foo:
        ''' Test. '''
        a: int = 1
        b: int
    foo = Foo( b = 2 )
    assert 1 == foo.a
    assert 2 == foo.b
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    with pytest.raises( exceptions.AttributeImmutability ):
        foo.a = 3


@pytest.mark.parametrize(
    'module_qname, decorator_name',
    product(
        ( qname for qname in MODULES_QNAMES if qname.endswith( '.classes' ) ),
        ( 'dataclass_with_standard_behaviors', ) # 'with_standard_behaviors' )
    )
)
def test_142_decorator_application_with_args( module_qname, decorator_name ):
    ''' Decorator class applies to class with arguments. '''
    module = cache_import_module( module_qname )
    decorator = getattr( module, decorator_name )
    @decorator( mutables = ( 'a', ) )
    class Foo:
        ''' Test. '''
        a: int = 1
        b: int
    foo = Foo( b = 2 )
    assert 1 == foo.a
    assert 2 == foo.b
    foo.a = 3
    assert 3 == foo.a
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    with pytest.raises( exceptions.AttributeImmutability ):
        foo.b = 4


@pytest.mark.parametrize(
    'module_qname, decorator_name',
    product(
        ( qname for qname in MODULES_QNAMES if qname.endswith( '.classes' ) ),
        ( 'dataclass_with_standard_behaviors', ) # 'with_standard_behaviors' )
    )
)
def test_143_decorator_application_with_no_args(
    module_qname, decorator_name
):
    ''' Decorator class applies to class with no arguments. '''
    module = cache_import_module( module_qname )
    decorator = getattr( module, decorator_name )
    @decorator( )
    class Foo:
        ''' Test. '''
        a: int = 1
        b: int
    foo = Foo( b = 2 )
    assert 1 == foo.a
    assert 2 == foo.b
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    with pytest.raises( exceptions.AttributeImmutability ):
        foo.a = 3


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    assert hasattr( class_factory_class, '__doc__' )
    assert isinstance( class_factory_class.__doc__, str )
    assert class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_910_dynadoc_sanity( module_qname, class_name ):
    ''' Class has valid dynamic documentation attributes. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    assert hasattr( class_factory_class, '_dynadoc_fragments_' )
    assert isinstance( class_factory_class._dynadoc_fragments_, tuple )
    assert class_factory_class._dynadoc_fragments_
    assert hasattr( class_factory_class, '__doc__' )
    assert isinstance( class_factory_class.__doc__, str )
    assert class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_920_new_sanity( module_qname, class_name ):
    ''' Class has valid __new__ method. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    assert hasattr( class_factory_class, '__new__' )
    assert callable( class_factory_class.__new__ )
