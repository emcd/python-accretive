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


''' Accretive metaclasses with attribute concealment. '''


from .. import __
from .. import classes as _classes


class Class( __.ClassConcealerExtension, _classes.Class ):
    ''' Enforces class attributes accretion and concealment.

        Cannot reassign or delete class attributes after they are assigned.

        By default, only lists public class attributes. Additional attributes
        can be added to the listing by providing a
        ``_class_attribute_visibility_includes_`` attribute on a
        subclass.
    '''


class ABCFactory( __.ClassConcealerExtension, _classes.ABCFactory ):
    ''' Enforces class attributes accretion and concealment.

        Cannot reassign or delete class attributes after they are assigned.

        By default, only lists public class attributes. Additional attributes
        can be added to the listing by providing a
        ``_class_attribute_visibility_includes_`` attribute on a
        subclass.
    '''


__all__ = __.discover_public_attributes( globals( ) )
