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


''' Assert basic characteristics of package. '''


import pytest

from . import cache_import_module, discover_module_names, package_name


package = cache_import_module( )


def test_000_package_sanity( ):
    ''' Package is sane. '''
    assert package.__package__ == package_name
    assert package.__name__ == package_name


@pytest.mark.parametrize( 'module_name', discover_module_names( ) )
def test_010_attribute_module_existence( module_name ):
    ''' Package module is attribute of package. '''
    assert module_name in package.__dict__


@pytest.mark.parametrize( 'module_name', discover_module_names( ) )
def test_011_attribute_module_classification( module_name ):
    ''' Package module is in package attributes directory. '''
    from inspect import ismodule
    assert ismodule( getattr( package, module_name ) )


@pytest.mark.parametrize(
    'module_name',
    ( module_name for module_name in discover_module_names( )
      if not module_name.startswith( '_' ) )
)
def test_012_attribute_module_visibility( module_name ):
    ''' Package module is in package attributes directory. '''
    assert module_name in dir( package )


@pytest.mark.parametrize(
    'module_name',
    ( module_name for module_name in discover_module_names( )
      if module_name.startswith( '_' ) )
)
def test_013_attribute_module_invisibility( module_name ):
    ''' Package module is not in package attributes directory. '''
    assert module_name not in dir( package )


@pytest.mark.parametrize( 'aname', ( '__all__', '__version__', ) )
def test_015_miscellaneous_attribute_existence( aname ):
    assert aname in package.__dict__


@pytest.mark.parametrize(
    'aname, aclass',
    ( ( '__all__', tuple ), ( '__version__', str ), )
)
def test_016_miscellaneous_attribute_classification( aname, aclass ):
    assert isinstance( getattr( package, aname ), aclass )


@pytest.mark.parametrize( 'aname', ( '__version__', ) )
def test_017_miscellaneous_attribute_visibility( aname ):
    assert aname in dir( package )
