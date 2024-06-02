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

# pylint: disable=magic-value-comparison,protected-access


import pytest

from itertools import product

from . import (
    CONCEALMENT_PACKAGES_NAMES,
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )
THESE_CONCEALMENT_MODULE_QNAMES = tuple(
    name for name in THESE_MODULE_QNAMES
    if name.startswith( CONCEALMENT_PACKAGES_NAMES ) )
ABC_FACTORIES_NAMES = ( 'ABCFactory', )
THESE_CLASSES_NAMES = ( 'Class', *ABC_FACTORIES_NAMES, )

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
    ''' Class accretes. '''
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
    product( THESE_CONCEALMENT_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_attribute_concealment( module_qname, class_name ):
    ''' Class conceals attributes. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''
        _class_attribute_visibility_includes_ = frozenset( ( '_private', ) )

    assert not dir( Object )
    Object.public = 42
    assert 'public' in dir( Object )
    Object._nonpublic = 3.1415926535
    assert '_nonpublic' not in dir( Object )
    assert '_private' not in dir( Object )
    Object._private = 'foo'
    assert '_private' in dir( Object )


# TODO: Test non-concealment.


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, ABC_FACTORIES_NAMES )
)
def test_200_abc_mutation_allowance( module_qname, class_name ):
    ''' Class allows mutation of ABC machinery. '''
    from abc import abstractmethod
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class AbstractObject( metaclass = class_factory_class ):
        ''' test '''
        @abstractmethod
        def method( self ):
            ''' test '''
            raise NotImplementedError

    class ConcereteObject( AbstractObject ): # pylint: disable=unused-variable
        ''' test '''
        def method( self ): return 42

    assert hasattr( AbstractObject, '__abstractmethods__' )
    assert hasattr( AbstractObject, '_abc_impl' )
