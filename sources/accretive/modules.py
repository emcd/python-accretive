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


''' Accretive modules. '''


from . import __
from . import _annotations as _a


class Module( __.Module ): # type: ignore[misc]
    ''' Accretive modules. '''

    def __delattr__( self, name: str ) -> None:
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( self, name: str, value: _a.Any ) -> None:
        from .exceptions import IndelibleAttributeError
        if hasattr( self, name ): raise IndelibleAttributeError( name )
        super( ).__setattr__( name, value )

Module.__doc__ = __.generate_docstring(
    Module, 'description of module', 'module attributes accretion' )


reclassify_modules: _a.ModuleReclassifier = __.partial_function(
    __.reclassify_modules, to_class = Module )


__all__ = __.discover_public_attributes( globals( ) )
