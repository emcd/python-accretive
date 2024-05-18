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


''' Accretive class factory classes (aka., metaclasses). '''


from . import __


class _ConcealerExtension( type ):

    _class_attribute_visibility_includes_ = frozenset( )

    def __dir__( class_ ):
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in class_._class_attribute_visibility_includes_ ) )


class Class( type ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete attributes after they are assigned.
    '''

    def __delattr__( class_, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( class_, name, value ):
        from .exceptions import ImmutableAttributeError
        if hasattr( class_, name ): raise ImmutableAttributeError( name )
        super( ).__setattr__( name, value )


class ConcealerClass( _ConcealerExtension, Class ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete attributes after they are assigned.

        By default, only lists public attributes. Additional attributes can be
        added to the listing by providing a
        '_class_attribute_visibility_includes_' attribute on a subclass.
    '''


class ABCFactory( Class, __.ABCFactory ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete attributes after they are assigned.
    '''

    def __setattr__( class_, name, value ):
        from .exceptions import ImmutableAttributeError
        if hasattr( class_, name ):
            #if '__abstractmethods__' == name or name.startswith( '_abc_' ):
            if name.startswith( '_abc_' ):
                __.ABCFactory.__setattr__( class_, name, value )
                return
            raise ImmutableAttributeError( name )
        __.ABCFactory.__setattr__( class_, name, value )


class ConcealerABCFactory( _ConcealerExtension, ABCFactory ):
    ''' Enforces class attributes accretion.

        Cannot reassign or delete attributes after they are assigned.

        By default, only lists public attributes. Additional attributes can be
        added to the listing by providing a
        '_class_attribute_visibility_includes_' attribute on a subclass.
    '''


__all__ = __.discover_public_attributes( globals( ) )
