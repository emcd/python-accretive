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


''' Accretive classes. '''


from . import __


class Class( type ):
    ''' Accretive classes. '''

    def __new__(
        factory, name, bases, namespace, docstring = None, **nomargs
    ):
        if docstring: namespace[ '__doc__' ] = docstring
        return super( ).__new__( factory, name, bases, namespace, **nomargs )

    def __delattr__( class_, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )

    def __setattr__( class_, name, value ):
        from .exceptions import IndelibleAttributeError
        if hasattr( class_, name ): raise IndelibleAttributeError( name )
        # Note: CPython cell class is not set in all circumstances.
        #       When it is, then we use two-argument form.
        #       Else, we use three-argument form.
        try: super( ).__setattr__( name, value )
        except TypeError: super( ).__setattr__( class_, name, value )

Class.__doc__ = __.generate_docstring(
    Class,
    'description of class factory class',
    'class attributes accretion'
)


class ABCFactory( Class, __.ABCFactory ):
    ''' Accretive abstract base classes (ABC). '''

    def __setattr__( class_, name, value ):
        # Bypass accretion machinery for ABC magic attributes.
        if ( # pylint: disable=magic-value-comparison
            '__abstractmethods__' == name or name.startswith( '_abc_' )
        ):
            __.ABCFactory.__setattr__( class_, name, value )
            return
        super( ).__setattr__( name, value )

ABCFactory.__doc__ = __.generate_docstring(
    ABCFactory,
    'description of class factory class',
    'class attributes accretion',
    'abc attributes exemption',
)


__all__ = __.discover_public_attributes( globals( ) )
