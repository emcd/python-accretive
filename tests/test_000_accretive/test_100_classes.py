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

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )
ABC_FACTORIES_NAMES = ( 'ABCFactory', )
THESE_CLASSES_NAMES = ( 'Class', *ABC_FACTORIES_NAMES, )
NONABC_FACTORIES_NAMES = tuple(
    name for name in THESE_CLASSES_NAMES
    if name not in ABC_FACTORIES_NAMES )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


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
def test_102_docstring_assignment( module_qname, class_name ):
    ''' Class has dynamically-assigned docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class, docstring = 'dynamic' ):
        ''' test '''
        attr = 42

    assert 'test' != Object.__doc__
    assert 'dynamic' == Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ABC_FACTORIES_NAMES )
)
def test_200_abc_mutation_allowance( module_qname, class_name ):
    ''' Class allows mutation of ABC machinery. '''
    from collections.abc import Mapping
    from platform import python_implementation
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''

    class Dict( # pylint: disable=abstract-method,unused-variable
        Object, Mapping
    ):
        ''' test '''

    python_kind = python_implementation( )
    assert hasattr( Object, '__abstractmethods__' )
    if python_kind in ( 'CPython', ):
        assert hasattr( Object, '_abc_impl' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, NONABC_FACTORIES_NAMES )
)
def test_201_abc_mutation_prevention( module_qname, class_name ):
    ''' Class prevents mutation of ABC machinery. '''
    from abc import ABCMeta
    from collections.abc import Mapping
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Class( class_factory_class, ABCMeta ):
        ''' test '''

    class Object( metaclass = Class ):
        ''' test '''

    with pytest.raises( exceptions.IndelibleAttributeError ):

        class Dict( # pylint: disable=abstract-method,unused-variable
            Object, Mapping
        ):
            ''' test '''


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


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ABC_FACTORIES_NAMES )
)
def test_950_docstring_mentions_abc_exemption( module_qname, class_name ):
    ''' Class docstring mentions ABC attributes exemption. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'abc attributes exemption' )
    assert fragment in class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, NONABC_FACTORIES_NAMES )
)
def test_951_docstring_not_mentions_abc_exemption( module_qname, class_name ):
    ''' Class docstring does not mention ABC attributes exemption. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'abc attributes exemption' )
    assert fragment not in class_factory_class.__doc__
