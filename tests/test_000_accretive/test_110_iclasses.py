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


""" Assert correct function of immutable class support code. """


# from re import compile as re_compile

import pytest

from . import (
    PACKAGE_NAME,
    cache_import_module,
)


ICLASSES_MODULE_QNAME = f"{PACKAGE_NAME}.iclasses"


def test_010_provide_error_class_failure( ):
    """ Error provider fails on invalid name. """
    iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    with pytest.raises( exceptions.ErrorProvideFailure ):
        iclasses.provide_error_class( 'NonExistent' )


# def test_020_assign_attribute_if_absent_mutable_by_predicate( ):
#     """ Attribute assigner allows mutable attribute by predicate. """
#     iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
#     class Object:
#         _instance_behaviors_ = frozenset( ( 'immutability', ) )
#         _instance_mutables_predicates_ = (
#             lambda name: name.startswith( 'foo' ), )
#     obj = Object( )
#     obj.foo_bar = 1
#     assert 1 == obj.foo_bar
#     ligation = ( lambda name, value: setattr( obj, name, value ) )
#     iclasses.assign_attribute_if_absent_mutable(
#         obj,
#         ligation = ligation,
#         attributes_namer = (
#             lambda level, name: f"_{level}_{name}_" ),
#         error_class_provider = iclasses.provide_error_class,
#         level = 'instance',
#         name = 'foo_bar',
#         value = 2 )
#     assert 2 == obj.foo_bar


# def test_021_assign_attribute_if_absent_mutable_by_regex( ):
#     """ Attribute assigner allows mutable attribute by regex. """
#     iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
#     class Object:
#         _instance_behaviors_ = frozenset( ( 'immutability', ) )
#         _instance_mutables_regexes_ = ( re_compile( r'foo_.*' ), )
#     obj = Object( )
#     obj.foo_bar = 1
#     assert 1 == obj.foo_bar
#     ligation = ( lambda name, value: setattr( obj, name, value ) )
#     iclasses.assign_attribute_if_absent_mutable(
#         obj,
#         ligation = ligation,
#         attributes_namer = (
#             lambda level, name: f"_{level}_{name}_" ),
#         error_class_provider = iclasses.provide_error_class,
#         level = 'instance',
#         name = 'foo_bar',
#         value = 2 )
#     assert 2 == obj.foo_bar


# def test_022_assign_attribute_if_absent_mutable_class_level( ):
#     """ Attribute assigner allows mutable attribute at class level. """
#     iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
#     class Object:
#         _class_behaviors_ = frozenset( ( 'immutability', ) )
#         _class_mutables_names_ = ( 'foo_bar', )
#     obj = Object( )
#     obj.foo_bar = 1
#     assert 1 == obj.foo_bar
#     ligation = ( lambda name, value: setattr( obj, name, value ) )
#     iclasses.assign_attribute_if_absent_mutable(
#         obj,
#         ligation = ligation,
#         attributes_namer = (
#             lambda level, name: f"_{level}_{name}_" ),
#         error_class_provider = iclasses.provide_error_class,
#         level = 'class',
#         name = 'foo_bar',
#         value = 2 )
#     assert 2 == obj.foo_bar


# def test_023_assign_attribute_if_absent_mutable_wildcard( ):
#     """ Attribute assigner allows any mutable attribute by wildcard. """
#     iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
#     class Object:
#         _instance_behaviors_ = frozenset( ( 'immutability', ) )
#         _instance_mutables_names_ = '*'
#     obj = Object( )
#     ligation = ( lambda name, value: setattr( obj, name, value ) )
#     iclasses.assign_attribute_if_absent_mutable(
#         obj,
#         ligation = ligation,
#         attributes_namer = (
#             lambda level, name: f"_{level}_{name}_" ),
#         error_class_provider = iclasses.provide_error_class,
#         level = 'instance',
#         name = 'foo_bar',
#         value = 2 )
#     assert 2 == obj.foo_bar


# def test_024_assign_attribute_if_absent_mutable_absent( ):
#     """ Attribute assigner allows absent attribute. """
#     iclasses = cache_import_module( ICLASSES_MODULE_QNAME )
#     class Object:
#         _instance_behaviors_ = frozenset( ( 'immutability', ) )
#     obj = Object( )
#     ligation = ( lambda name, value: setattr( obj, name, value ) )
#     iclasses.assign_attribute_if_absent_mutable(
#         obj,
#         ligation = ligation,
#         attributes_namer = (
#             lambda level, name: f"_{level}_{name}_" ),
#         error_class_provider = iclasses.provide_error_class,
#         level = 'instance',
#         name = 'foo_bar',
#         value = 2 )
#     assert 2 == obj.foo_bar
