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


''' Accretive metaclasses. '''


from . import __


class Class( type ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete class attributes after they are assigned.
    '''

    def __delattr__( class_, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( class_, name, value ):
        from .exceptions import ImmutableAttributeError
        if hasattr( class_, name ): raise ImmutableAttributeError( name )
        super( ).__setattr__( name, value )


class ABCFactory( Class, __.ABCFactory ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete class attributes after they are assigned.
    '''

    def __setattr__( class_, name, value ):
        # pylint: disable=magic-value-comparison
        if '__abstractmethods__' == name or name.startswith( '_abc_' ):
            __.ABCFactory.__setattr__( class_, name, value )
            return
        # pylint: enable=magic-value-comparison
        super( ).__setattr__( name, value )


__all__ = __.discover_public_attributes( globals( ) )
