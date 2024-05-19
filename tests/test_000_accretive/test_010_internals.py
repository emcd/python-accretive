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


''' Assert correct function of internals. '''

# pylint: disable=magic-value-comparison,protected-access


import pytest

from . import cache_import_module, package_name


module_name = '__'
module = cache_import_module( module_name )
module_attribute_names = (
    'ConcealerExtension', 'discover_fqname', 'discover_public_attributes',
)


def test_010_concealer_extension_instantiation( ):
    ''' Class 'ConcealerExtension' instantiates. '''
    obj = module.ConcealerExtension( )
    assert isinstance( obj, module.ConcealerExtension )


def test_011_concealer_extension_attribute_concealment( ):
    ''' Class 'ConcealerExtension' conceals attributes. '''
    obj = module.ConcealerExtension( )
    assert not dir( obj )
    obj.public = 42
    assert 'public' in dir( obj )
    obj._nonpublic = 3.1415926535
    assert '_nonpublic' not in dir( obj )
    obj._attribute_visibility_includes_ = frozenset( ( '_nonpublic', ) )
    assert '_nonpublic' in dir( obj )
    assert '_attribute_visibility_includes_' not in dir( obj )


def test_020_fqname_discovery( ):
    ''' Fully-qualified name of object is discovered. '''
    assert 'builtins.NoneType' == module.discover_fqname( None )
    assert (
        'builtins.type'
        == module.discover_fqname( module.ConcealerExtension ) )
    obj = module.ConcealerExtension( )
    assert (
        f"{package_name}.{module_name}.ConcealerExtension"
        == module.discover_fqname( obj ) )


@pytest.mark.parametrize(
    'provided, expected',
    (
        ( { 'foo': 12 }, ( ) ),
        ( { '_foo': cache_import_module }, ( ) ),
        (
            { name: getattr( module, name )
              for name in module_attribute_names },
            module_attribute_names
        ),
    )
)
def test_030_public_attribute_discovery( provided, expected ):
    ''' Public attributes are discovered from dictionary. '''
    assert expected == module.discover_public_attributes( provided )
