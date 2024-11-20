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


''' Accretive modules.

Provides a module type that enforces attribute immutability after assignment.
This helps ensure that module-level constants remain constant and that module
interfaces remain stable during runtime.

The module implementation is derived from :py:class:`types.ModuleType` and adds
accretive behavior. This makes it particularly useful for:

* Ensuring constants remain constant
* Preventing accidental modification of module interfaces
* Creating plugin modules with stable APIs

Also provides a convenience function:

* ``reclassify_modules``: Converts existing modules to accretive modules.
'''


from . import __


class Module( __.Module ): # type: ignore[misc]
    ''' Accretive modules. '''

    def __delattr__( self, name: str ) -> None:
        from .exceptions import AttributeImmutabilityError
        raise AttributeImmutabilityError( name )

    def __setattr__( self, name: str, value: __.a.Any ) -> None:
        from .exceptions import AttributeImmutabilityError
        if hasattr( self, name ): raise AttributeImmutabilityError( name )
        super( ).__setattr__( name, value )

Module.__doc__ = __.generate_docstring(
    Module, 'description of module', 'module attributes accretion' )


def reclassify_modules(
    attributes: __.cabc.Mapping[ str, __.a.Any ],
    to_class: type[ Module ] = Module
) -> None:
    ''' Reclassifies modules in dictionary with custom module type. '''
    from inspect import ismodule
    for attribute in attributes.values( ):
        if not ismodule( attribute ): continue
        if isinstance( attribute, to_class ): continue
        attribute.__class__ = to_class
