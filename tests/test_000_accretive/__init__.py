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


''' Package of tests. '''

# pylint: disable=magic-value-comparison


package_name = 'accretive'


_modules_cache = { }
def cache_import_module( module_name = '' ):
    ''' Imports module from package by name and caches it. '''
    from importlib import import_module
    if not module_name:
        qname = package_name
        arguments = ( package_name, )
    else:
        qname = f"{package_name}.{module_name}"
        arguments = ( f".{module_name}", package_name, )
    if qname not in _modules_cache:
        _modules_cache[ qname ] = import_module( *arguments )
    return _modules_cache[ qname ]


package = cache_import_module( )


def _discover_module_names( ):
    from itertools import chain
    from pathlib import Path
    return tuple( chain(
        (   path.stem
            for path in Path( package.__file__ ).parent.glob( '*.py' )
            if '__init__.py' != path.name ),
        (   path.name
            for path in Path( package.__file__ ).parent.glob( '*' )
            if '__pycache__' != path.name and path.is_dir( ) ) ) )
module_names = _discover_module_names( )
