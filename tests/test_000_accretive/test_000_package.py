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


''' Assert basic characteristics of package and modules thereof. '''


import pytest

from . import cache_import_module, module_names, package, package_name


def test_000_sanity( ):
    ''' Package is sane. '''
    assert package.__package__ == package_name
    assert package.__name__ == package_name


@pytest.mark.parametrize( 'module_name', module_names )
def test_010_attribute_module_existence( module_name ):
    ''' Package module is attribute of package. '''
    assert module_name in package.__dict__


@pytest.mark.parametrize( 'module_name', module_names )
def test_011_attribute_module_classification( module_name ):
    ''' Package attribute is module. '''
    from inspect import ismodule
    assert ismodule( getattr( package, module_name ) )


@pytest.mark.parametrize(
    'module_name',
    ( module_name for module_name in module_names
      if not module_name.startswith( '_' ) )
)
def test_012_attribute_module_visibility( module_name ):
    ''' Package module is in package attributes directory. '''
    assert module_name in dir( package )


@pytest.mark.parametrize(
    'module_name',
    ( module_name for module_name in module_names
      if module_name.startswith( '_' ) )
)
def test_013_attribute_module_invisibility( module_name ):
    ''' Package module is not in package attributes directory. '''
    assert module_name not in dir( package )


@pytest.mark.parametrize( 'aname', ( '__version__', ) )
def test_015_miscellaneous_attribute_existence( aname ):
    ''' Miscellaneous attribute exists in package. '''
    assert aname in package.__dict__


@pytest.mark.parametrize( 'aname, aclass', ( ( '__version__', str ), ) )
def test_016_miscellaneous_attribute_classification( aname, aclass ):
    ''' Miscellaaneous attribute is correct class. '''
    assert isinstance( getattr( package, aname ), aclass )


@pytest.mark.parametrize( 'aname', ( '__version__', ) )
def test_017_miscellaneous_attribute_visibility( aname ):
    ''' Miscellaneous attribute is in package attributes directory. '''
    assert aname in dir( package )


def test_030_wildcard_exportation( ):
    ''' Package provides wildcard exports. '''
    assert hasattr( package, '__all__' )
    assert isinstance( package.__all__, tuple )


def test_031_wildcard_exports_existence( ):
    ''' Wildcard exports are attributes of package. '''
    exports = frozenset( package.__all__ )
    assert exports == exports & package.__dict__.keys( )


def test_032_wildcard_exports_visibility( ):
    ''' Wildcard exports are in package attributes directory. '''
    exports = frozenset( package.__all__ )
    assert exports == exports & frozenset( dir( package ) )


@pytest.mark.parametrize( 'module_name', module_names )
def test_100_sanity( module_name ):
    ''' Package module is sane. '''
    module = cache_import_module( module_name )
    qname = f"{package_name}.{module_name}"
    assert module.__package__ == package_name
    assert module.__name__ == qname


@pytest.mark.parametrize( 'module_name', module_names )
def test_130_wildcard_exportation( module_name ):
    ''' Package module provides wildcard exports. '''
    module = cache_import_module( module_name )
    assert hasattr( module, '__all__' )
    assert isinstance( module.__all__, tuple )


@pytest.mark.parametrize( 'module_name', module_names )
def test_131_wildcard_exports_existence( module_name ):
    ''' Wildcard exports are attributes of package module. '''
    module = cache_import_module( module_name )
    exports = frozenset( module.__all__ )
    assert exports == exports & module.__dict__.keys( )


@pytest.mark.parametrize( 'module_name', module_names )
def test_132_wildcard_exports_visibility( module_name ):
    ''' Wildcard exports are in package module attributes directory. '''
    module = cache_import_module( module_name )
    exports = frozenset( module.__all__ )
    assert exports == exports & frozenset( dir( module ) )
