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


''' Accretive objects. '''


from . import __


class Object:
    ''' Enforces object attributes accretion.

        Cannot reassign or delete attributes after they are assigned.
    '''

    def __delattr__( self, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( self, name, value ):
        from .exceptions import ImmutableAttributeError
        if hasattr( self, name ): raise ImmutableAttributeError( name )
        super( ).__setattr__( name, value )


class ConcealerObject( __.ConcealerExtension, Object ):
    ''' Enforces object attributes accretion and concealment.

        Cannot reassign or delete attributes after they are assigned.

        By default, only lists public attributes. Additional attributes can be
        added to the listing by providing an '_attribute_visibility_includes_'
        attribute on a subclass.
    '''


__all__ = __.discover_public_attributes( globals( ) )
