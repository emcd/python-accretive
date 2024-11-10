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

# mypy: ignore-errors
# pylint: disable=magic-value-comparison,protected-access


import pytest

from itertools import product
from platform import python_implementation

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )
THESE_CLASSES_NAMES = ( 'Class', 'ABCFactory', 'ProtocolClass' )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently"
)


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''

    assert isinstance( Object, class_factory_class )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_accretion( module_qname, class_name ):
    ''' Class accretes attributes. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''
        attr = 42

    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.attr = -1
    assert 42 == Object.attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del Object.attr
    assert 42 == Object.attr
    Object.accreted_attr = 'foo'
    assert 'foo' == Object.accreted_attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.accreted_attr = 'bar'
    assert 'foo' == Object.accreted_attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        del Object.accreted_attr
    assert 'foo' == Object.accreted_attr


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_class_decorators( module_qname, class_name ):
    ''' Class accepts and applies decorators correctly. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    decorator_calls = [ ]

    def test_decorator1( cls ):
        decorator_calls.append( 'decorator1' )
        cls.decorator1_attr = 'value1'
        return cls

    def test_decorator2( cls ):
        decorator_calls.append( 'decorator2' )
        cls.decorator2_attr = 'value2'
        return cls

    class Object(
        metaclass = class_factory_class,
        decorators = ( test_decorator1, test_decorator2 )
    ):
        ''' test '''
        attr = 42

        _class_behaviors_ = { 'foo' }

    assert [ 'decorator1', 'decorator2' ] == decorator_calls
    assert 'value1' == Object.decorator1_attr
    assert 'value2' == Object.decorator2_attr
    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.decorator1_attr = 'new_value'
    with pytest.raises( exceptions.IndelibleAttributeError ):
        Object.decorator2_attr = 'new_value'


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_111_class_decorator_reproduction_method( module_qname, class_name ):
    ''' Class handles decorator reproduction with super() method. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        def method_with_super( self ):
            ''' References class cell on CPython. '''
            super( ).__init__( )
            return self.__class__.__name__

        def other_method_with_super( self ):
            ''' References class cell on CPython. '''
            super( ).__init__( )
            return 'other'

    # Verify class was properly reproduced and both methods work
    obj = Object( )
    assert 'Object' == obj.method_with_super( )
    assert 'other' == obj.other_method_with_super( )


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_112_class_decorator_reproduction_property( module_qname, class_name ):
    ''' Class handles decorator reproduction with dotted access property. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        @property
        def prop_with_class( self ):
            ''' References class cell on CPython. '''
            return self.__class__.__name__

        @property
        def other_prop_with_class( self ):
            ''' References class cell on CPython. '''
            return f"other_{self.__class__.__name__}"

    # Verify class was properly reproduced and both properties work
    obj = Object( )
    assert 'Object' == obj.prop_with_class
    assert 'other_Object' == obj.other_prop_with_class


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_113_class_decorator_reproduction_no_cell( module_qname, class_name ):
    ''' Class handles decorator reproduction with no class cell. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        def method_without_cell( self ): # pylint: disable=no-self-use
            ''' Operates without class cell on CPython. '''
            return 'no_cell'

    # Verify class was properly reproduced
    obj = Object()
    assert 'no_cell' == obj.method_without_cell( )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_114_decorator_error_handling( module_qname, class_name ):
    ''' Class handles decorator errors appropriately. '''
    module = cache_import_module( module_qname )
    class_factory_class = ( # pylint: disable=unused-variable
        getattr( module, class_name ) )

    def failing_decorator( cls ):
        raise ValueError( "Decorator failure" ) # noqa

    with pytest.raises( ValueError, match = "Decorator failure" ):
        class Object( # pylint: disable=unused-variable
            metaclass = class_factory_class,
            decorators = ( failing_decorator, )
        ):
            ''' test '''


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_120_docstring_assignment( module_qname, class_name ):
    ''' Class has dynamically-assigned docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class, docstring = 'dynamic' ):
        ''' test '''
        attr = 42

    assert 'test' != Object.__doc__
    assert 'dynamic' == Object.__doc__


# TODO? String representations.


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
def test_901_docstring_describes_cfc( module_qname, class_name ):
    ''' Class docstring describes class factory class. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'description of class factory class' )
    assert fragment in class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_accretion( module_qname, class_name ):
    ''' Class docstring mentions accretion. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'class attributes accretion' )
    assert fragment in class_factory_class.__doc__
