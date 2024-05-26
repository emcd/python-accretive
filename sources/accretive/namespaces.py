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


''' Accretive namespaces. '''


from . import __
from . import objects as _objects


class Namespace( _objects.Object ):
    ''' Simple accretive namespace.

        An accretive namespace only accepts new attributes; attempts to alter
        or delete existing attributes result in errors.
    '''

    def __init__( self, *iterables, **nomargs ):
        super( ).__init__( )
        super( ).__getattribute__( '__dict__' ).update( *iterables, **nomargs )

    def __repr__( self ):
        return "{fqname}( {contents} )".format(
            fqname = __.discover_fqname( self ),
            contents = ', '.join( map(
                lambda entry: f"{entry[0]} = {entry[1]!r}",
                super( ).__getattribute__( '__dict__' ).items( ) ) ) )


class ConcealerNamespace( __.ConcealerExtension, Namespace ):
    ''' Accretive namespace with attribute concealment.

        Cannot reassign or delete attributes after they are assigned.

        By default, only lists public attributes. Additional attributes can be
        added to the listing by providing an '_attribute_visibility_includes_'
        attribute on a subclass.
    '''


__all__ = __.discover_public_attributes( globals( ) )
