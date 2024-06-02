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


''' Protected accretive objects with attribute concealment. '''


from .. import __
from .. import objects as _objects
from . import classes as _classes


class Object(
    __.ConcealerExtension, _objects.Object,
    metaclass = _classes.Class,
    docstring = __.generate_docstring(
        _objects.Object,
        'instance attributes concealment',
        'protection of class',
    )
):
    ''' Accretive objects. '''


__all__ = __.discover_public_attributes( globals( ) )
