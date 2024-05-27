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
from . import objects as _objects


class Module( _objects.Object, __.Module ):
    ''' Enforces module attributes accretion.

        Cannot reassign or delete module attributes after they are assigned.
    '''


def reclassify_modules( attributes, to_class = Module ):
    ''' Reclassifies modules in dictionary with custom module type.

        Default custom module type enforces module attributes accretion.
    '''
    for attribute in attributes.values( ):
        if not isinstance( attribute, __.Module ): continue
        if isinstance( attribute, to_class ): continue
        attribute.__class__ = to_class


__all__ = __.discover_public_attributes( globals( ) )
