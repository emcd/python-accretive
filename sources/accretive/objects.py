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
from . import classes as _classes


class _Dictionary( # type: ignore
    __.CoreDictionary, metaclass = _classes.ConcealerClass
):

    def __setitem__( self, key, value ):
        from .exceptions import EntryIndicatorValidationFailure
        if not __.is_python_identifier( key ):
            raise EntryIndicatorValidationFailure( key )
        super( ).__setitem__( key, value )


class Object:
    ''' Simple accretive object.

        Cannot reassign or delete attributes after they are assigned.
    '''

    __slots__ = ( '__dict__', )

    def __init__( self, *posargs, **nomargs ):
        super( ).__setattr__( '__dict__', _Dictionary( ) )
        # Pass all arguments down MRO chain without consuming any.
        super( ).__init__( *posargs, **nomargs )

    def __repr__( self ):
        return "{fqname}( )".format( fqname = __.discover_fqname( self ) )

    def __delattr__( self, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( self, name, value ):
        from .exceptions import (
            AbsentAttributeError,
            IllegalAttributeNameError,
            ImmutableAttributeError,
            ImmutableEntryError,
        )
        if not __.is_python_identifier( name ):
            raise IllegalAttributeNameError( name )
        try: dictionary = super( ).__getattribute__( '__dict__' )
        except AttributeError as exc:
            raise AbsentAttributeError( '__dict__' ) from exc
        try: dictionary[ name ] = value
        except ImmutableEntryError:
            raise ImmutableAttributeError( name ) from None


class ConcealerObject( __.ConcealerExtension, Object ):
    ''' Enforces object attributes accretion and concealment.

        Cannot reassign or delete attributes after they are assigned.

        By default, only lists public attributes. Additional attributes can be
        added to the listing by providing an '_attribute_visibility_includes_'
        attribute on a subclass.
    '''


__all__ = __.discover_public_attributes( globals( ) )
