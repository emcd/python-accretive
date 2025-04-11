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


''' Assert correct function of modules. '''


import sys
import types
import uuid

from itertools import product

import pytest

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.modules' ) )
THESE_CLASSES_NAMES = ( 'Module', )


def generate_unique_name( prefix: str ) -> str:
    ''' Generate a unique module name to avoid test interference. '''
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_temp_module_hierarchy( package_prefix: str ):
    ''' Create a temporary module hierarchy for testing.

        Returns a tuple of (parent_name, parent_module, child_modules_dict)
        where child_modules_dict maps name -> module.

        Caller is responsible for cleanup.
    '''
    parent_name = generate_unique_name( f"{package_prefix}.parent" )
    child1_name = f"{parent_name}.child1"
    child2_name = f"{parent_name}.child2"
    parent_module = types.ModuleType( parent_name )
    child1_module = types.ModuleType( child1_name )
    child2_module = types.ModuleType( child2_name )
    parent_module.__package__ = package_prefix
    child1_module.__package__ = parent_name
    child2_module.__package__ = parent_name
    sys.modules[ parent_name ] = parent_module
    sys.modules[ child1_name ] = child1_module
    sys.modules[ child2_name ] = child2_module
    parent_module.child1 = child1_module
    parent_module.child2 = child2_module
    child_modules = {
        'child1': child1_module,
        'child2': child2_module }
    return parent_name, parent_module, child_modules


def cleanup_temp_modules( *module_names ):
    ''' Remove temporary modules from sys.modules. '''
    for name in module_names:
        if name in sys.modules:
            del sys.modules[ name ]


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    obj = Module( 'foo' )
    assert isinstance( obj, Module )
    assert 'foo' == obj.__name__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_accretion( module_qname, class_name ):
    ''' Module accretes attributes. '''
    module = cache_import_module( module_qname )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    Module = getattr( module, class_name )
    obj = Module( 'foo' )
    obj.attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.attr = -1
    assert 42 == obj.attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.attr
    assert 42 == obj.attr


def test_500_module_reclassification( ):
    ''' Modules are correctly reclassified when passed directly. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    Module = module.Module
    module_name = generate_unique_name( f"{PACKAGE_NAME}.test_module" )
    test_module = types.ModuleType( module_name )
    test_module.__name__ = module_name
    test_module.__package__ = PACKAGE_NAME
    sys.modules[module_name] = test_module
    try:
        assert not isinstance( test_module, Module )
        module.reclassify_modules( test_module )
        assert isinstance( test_module, Module )
    finally: cleanup_temp_modules( module_name )


def test_501_module_reclassification_dictionary( ):
    ''' Modules are correctly reclassified from dictionary. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    Module = module.Module
    package_dict = {
        '__name__': PACKAGE_NAME,
        '__package__': PACKAGE_NAME
    }
    module_name = generate_unique_name( f"{PACKAGE_NAME}.test_module" )
    test_module = types.ModuleType( module_name )
    test_module.__name__ = module_name
    test_module.__package__ = PACKAGE_NAME
    package_dict['test_module'] = test_module
    sys.modules[module_name] = test_module
    try:
        assert not isinstance( test_module, Module )
        module.reclassify_modules( package_dict )
        assert isinstance( test_module, Module )
    finally: cleanup_temp_modules( module_name )


def test_502_module_reclassification_package_dict( ):
    ''' Modules correctly reclassified from dictionary with package info. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    Module = module.Module
    module_name = generate_unique_name( f"{PACKAGE_NAME}.test_module" )
    test_module = types.ModuleType( module_name )
    test_module.__name__ = module_name
    test_module.__package__ = PACKAGE_NAME
    other_name = generate_unique_name( "other_package.module" )
    other_module = types.ModuleType( other_name )
    other_module.__name__ = other_name
    other_module.__package__ = "other_package"
    sys.modules[module_name] = test_module
    sys.modules[other_name] = other_module
    ns_dict = {
        '__name__': PACKAGE_NAME,
        '__package__': PACKAGE_NAME,
        'test': test_module,
        'other': other_module,
    }
    try:
        assert not isinstance( test_module, Module )
        assert not isinstance( other_module, Module )
        module.reclassify_modules( ns_dict )
        assert isinstance( test_module, Module )
        assert not isinstance( other_module, Module )
    finally: cleanup_temp_modules( module_name, other_name )


def test_510_module_reclassification_by_name( ):
    ''' Modules are correctly reclassified when passed by name. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    Module = module.Module
    test_module_name = generate_unique_name( f"{PACKAGE_NAME}.test_module" )
    test_module = types.ModuleType( test_module_name )
    test_module.__package__ = PACKAGE_NAME
    sys.modules[ test_module_name ] = test_module
    try:
        assert not isinstance( test_module, Module )
        module.reclassify_modules( test_module_name )
        assert isinstance( test_module, Module )
        test_module.test_attr = "value"
        with pytest.raises( exceptions.AttributeImmutabilityError ):
            test_module.test_attr = "new value"
    finally: cleanup_temp_modules( test_module_name )


def test_520_module_reclassification_recursive( ):
    ''' Module reclassification correctly operates recursively. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    Module = module.Module
    parent_name, parent_module, children = (
        create_temp_module_hierarchy( PACKAGE_NAME ) )
    child1_module = children[ 'child1' ]
    child2_module = children[ 'child2' ]
    all_modules = [ parent_name ]
    all_modules.extend( ( f"{parent_name}.child1", f"{parent_name}.child2" ) )
    try:
        assert not isinstance( parent_module, Module )
        assert not isinstance( child1_module, Module )
        assert not isinstance( child2_module, Module )
        module.reclassify_modules( parent_module, recursive=True )
        assert isinstance( parent_module, Module )
        assert isinstance( child1_module, Module )
        assert isinstance( child2_module, Module )
        parent_module.test_attr = "parent"
        child1_module.test_attr = "child1"
        child2_module.test_attr = "child2"
        with pytest.raises( exceptions.AttributeImmutabilityError ):
            parent_module.test_attr = "new parent"
        with pytest.raises( exceptions.AttributeImmutabilityError ):
            child1_module.test_attr = "new child1"
        with pytest.raises( exceptions.AttributeImmutabilityError ):
            child2_module.test_attr = "new child2"
    finally: cleanup_temp_modules( *all_modules )


def test_530_module_reclassification_non_recursive( ):
    ''' Module reclassification respects non-recursive mode. '''
    module = cache_import_module(f"{PACKAGE_NAME}.modules")
    Module = module.Module
    test_package = f"test_pkg_{uuid.uuid4().hex[:8]}"
    pkg_module = types.ModuleType(test_package)
    pkg_module.__name__ = test_package
    pkg_module.__package__ = ''  # Root level package
    parent_name = f"{test_package}.parent"
    parent_module = types.ModuleType(parent_name)
    parent_module.__name__ = parent_name
    parent_module.__package__ = test_package
    child1_name = f"{parent_name}.child1"
    child2_name = f"{parent_name}.child2"
    child1_module = types.ModuleType(child1_name)
    child2_module = types.ModuleType(child2_name)
    child1_module.__name__ = child1_name
    child2_module.__name__ = child2_name
    child1_module.__package__ = parent_name
    child2_module.__package__ = parent_name
    sys.modules[test_package] = pkg_module
    sys.modules[parent_name] = parent_module
    sys.modules[child1_name] = child1_module
    sys.modules[child2_name] = child2_module
    all_modules = [test_package, parent_name, child1_name, child2_name]
    try:
        assert not isinstance(parent_module, Module)
        assert not isinstance(child1_module, Module)
        assert not isinstance(child2_module, Module)
        module.reclassify_modules(parent_module)
        assert isinstance(parent_module, Module)
        assert not isinstance(child1_module, Module)
        assert not isinstance(child2_module, Module)
    finally: cleanup_temp_modules(*all_modules)


def test_540_module_reclassification_safety():
    ''' Module reclassification only affects modules in the same package. '''
    module = cache_import_module(f"{PACKAGE_NAME}.modules")
    Module = module.Module
    package_name = f"{PACKAGE_NAME}"
    pkg_module = types.ModuleType(package_name)
    pkg_module.__name__ = package_name
    pkg_module.__package__ = ''
    same_pkg_name = f"{package_name}.test_module_{uuid.uuid4().hex[:8]}"
    diff_pkg_name = f"other_package.test_module_{uuid.uuid4().hex[:8]}"
    same_pkg_module = types.ModuleType(same_pkg_name)
    diff_pkg_module = types.ModuleType(diff_pkg_name)
    same_pkg_module.__name__ = same_pkg_name
    diff_pkg_module.__name__ = diff_pkg_name
    same_pkg_module.__package__ = package_name
    diff_pkg_module.__package__ = "other_package"
    sys.modules[same_pkg_name] = same_pkg_module
    sys.modules[diff_pkg_name] = diff_pkg_module
    pkg_module.same_pkg = same_pkg_module
    pkg_module.diff_pkg = diff_pkg_module
    try:
        assert not isinstance(same_pkg_module, Module)
        assert not isinstance(diff_pkg_module, Module)
        module.reclassify_modules(pkg_module)
        assert isinstance(same_pkg_module, Module)
        assert not isinstance(diff_pkg_module, Module)
    finally: cleanup_temp_modules(same_pkg_name, diff_pkg_name)


def test_550_module_with_self_reference( ):
    ''' Module reclassification works when module contains self-reference. '''
    module = cache_import_module( f"{PACKAGE_NAME}.modules" )
    Module = module.Module
    test_module_name = generate_unique_name( f"{PACKAGE_NAME}.test_module" )
    test_module = types.ModuleType( test_module_name )
    test_module.__package__ = PACKAGE_NAME
    test_module.self = test_module
    sys.modules[ test_module_name ] = test_module
    try:
        assert not isinstance( test_module, Module )
        module.reclassify_modules( test_module )
        assert isinstance( test_module, Module )
        assert test_module.self is test_module
    finally: cleanup_temp_modules( test_module_name )


def test_560_module_reclassification_no_package():
    ''' Module reclassification returns early when no package name found. '''
    module = cache_import_module(f"{PACKAGE_NAME}.modules")
    Module = module.Module
    test_module_name = generate_unique_name("test_module")
    test_module = types.ModuleType(test_module_name)
    test_module.__name__ = test_module_name
    sys.modules[test_module_name] = test_module
    empty_dict = {
        "test_module": test_module,
        "some_value": 42
    }
    try:
        assert not isinstance(test_module, Module)
        module.reclassify_modules(empty_dict)
        assert not isinstance(test_module, Module)
        test_module2_name = generate_unique_name("test_module2")
        test_module2 = types.ModuleType(test_module2_name)
        test_module2.__name__ = test_module2_name
        test_module2.__package__ = ""  # Empty string
        sys.modules[test_module2_name] = test_module2
        dict_with_empty_package = {
            "__package__": "",
            "test_module": test_module2
        }
        assert not isinstance(test_module2, Module)
        module.reclassify_modules(dict_with_empty_package)
        assert not isinstance(test_module2, Module)
    finally: cleanup_temp_modules(test_module_name, test_module2_name)


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
    fragment = base.generate_docstring( 'module attributes accretion' )
    assert fragment in Object.__doc__
