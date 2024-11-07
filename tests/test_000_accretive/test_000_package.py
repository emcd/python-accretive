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

# mypy: ignore-errors


import pytest

from . import (
    MODULES_NAMES_BY_MODULE_QNAME,
    MODULES_QNAMES,
    PACKAGE_NAME,
    PACKAGES_NAMES,
    PACKAGES_NAMES_BY_MODULE_QNAME,
    cache_import_module,
)


@pytest.mark.parametrize( 'package_name', PACKAGES_NAMES )
def test_000_sanity( package_name ):
    ''' Package is sane. '''
    package = cache_import_module( package_name )
    assert package.__package__ == package_name
    assert package.__name__ == package_name


@pytest.mark.parametrize( 'module_qname', MODULES_QNAMES )
def test_010_attribute_module_existence( module_qname ):
    ''' Package module is attribute of package. '''
    package_name = PACKAGES_NAMES_BY_MODULE_QNAME[ module_qname ]
    package = cache_import_module( package_name )
    module_name = MODULES_NAMES_BY_MODULE_QNAME[ module_qname ]
    assert module_name in package.__dict__


@pytest.mark.parametrize( 'module_qname', MODULES_QNAMES )
def test_011_attribute_module_classification( module_qname ):
    ''' Package attribute is module. '''
    from inspect import ismodule
    package_name = PACKAGES_NAMES_BY_MODULE_QNAME[ module_qname ]
    package = cache_import_module( package_name )
    module_name = MODULES_NAMES_BY_MODULE_QNAME[ module_qname ]
    assert ismodule( getattr( package, module_name ) )


@pytest.mark.parametrize(
    'module_qname',
    (   module_qname for module_qname, module_name
        in MODULES_NAMES_BY_MODULE_QNAME.items( )
        if not module_name.startswith( '_' ) )
)
def test_012_attribute_module_visibility( module_qname ):
    ''' Package module is in package attributes directory. '''
    package_name = PACKAGES_NAMES_BY_MODULE_QNAME[ module_qname ]
    package = cache_import_module( package_name )
    module_name = MODULES_NAMES_BY_MODULE_QNAME[ module_qname ]
    assert module_name in dir( package )


#@pytest.mark.parametrize(
#    'module_qname',
#    (   module_qname for module_qname, module_name
#        in MODULES_NAMES_BY_MODULE_QNAME.items( )
#        if module_name.startswith( '_' ) )
#)
#def test_013_attribute_module_invisibility( module_qname ):
#    ''' Package module is not in package attributes directory. '''
#    package_name = PACKAGES_NAMES_BY_MODULE_QNAME[ module_qname ]
#    package = cache_import_module( package_name )
#    module_name = MODULES_NAMES_BY_MODULE_QNAME[ module_qname ]
#    assert module_name not in dir( package )


@pytest.mark.parametrize( 'aname', ( '__version__', ) )
def test_015_miscellaneous_attribute_existence( aname ):
    ''' Miscellaneous attribute exists in package. '''
    package = cache_import_module( PACKAGE_NAME )
    assert aname in package.__dict__


@pytest.mark.parametrize( 'aname, aclass', ( ( '__version__', str ), ) )
def test_016_miscellaneous_attribute_classification( aname, aclass ):
    ''' Miscellaaneous attribute is correct class. '''
    package = cache_import_module( PACKAGE_NAME )
    assert isinstance( getattr( package, aname ), aclass )


@pytest.mark.parametrize( 'aname', ( '__version__', ) )
def test_017_miscellaneous_attribute_visibility( aname ):
    ''' Miscellaneous attribute is in package attributes directory. '''
    package = cache_import_module( PACKAGE_NAME )
    assert aname in dir( package )


@pytest.mark.parametrize( 'module_qname', MODULES_QNAMES )
def test_100_sanity( module_qname ):
    ''' Package module is sane. '''
    package_name = PACKAGES_NAMES_BY_MODULE_QNAME[ module_qname ]
    module = cache_import_module( module_qname )
    assert module.__package__ == package_name
    assert module.__name__ == module_qname
