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


''' Assert basic characteristics of package modules. '''

# pylint: disable=magic-value-comparison


import pytest

from . import package_name


_module_names_cache = [ ]
def _discover_module_names( ):
    from importlib import import_module
    from itertools import chain
    from pathlib import Path
    package = import_module( package_name )
    if not _module_names_cache:
        _module_names_cache.extend( chain(
            (   path.stem
                for path in Path( package.__file__ ).parent.glob( '*.py' )
                if '__init__.py' != path.name ),
            (   path.name
                for path in Path( package.__file__ ).parent.glob( '*' )
                if '__pycache__' != path.name and path.is_dir( ) ) ) )
    return _module_names_cache


_modules_cache = { }
@pytest.mark.parametrize( 'module_name', _discover_module_names( ) )
def test_001_import_package_modules( module_name ):
    ''' Can import package modules. '''
    from importlib import import_module
    module = import_module( f".{module_name}", package_name )
    module_qname = f"{package_name}.{module_name}"
    assert module_qname == module.__name__
    _modules_cache[ module_qname ] = module
