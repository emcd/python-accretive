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


# pylint: disable=line-too-long
''' Accretive objects.

    Provides the base class for objects with accretive attributes. Once an
    attribute is set on an instance, it cannot be reassigned or deleted.

    The implementation uses a special dictionary type for attribute storage
    that enforces the accretive behavior. This makes it suitable as a base
    class for:

    * Configuration objects
    * Plugin interfaces
    * Immutable data containers
    * Objects requiring attribute stability

    >>> from accretive import Object
    >>> obj = Object( )
    >>> obj.x = 1  # Add new instance attribute
    >>> obj.y = 2  # Add another instance attribute
    >>> obj.x = 3  # Attempt modification
    Traceback (most recent call last):
        ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'x'.

    The `accretive` decorator can be used to make any class accretive:

    >>> from accretive import accretive
    >>> @accretive
    ... class Config:
    ...     def __init__( self, debug = False ):
    ...         self.debug = debug
    ...
    >>> config = Config( debug = True )
    >>> config.debug  # Access existing attribute
    True
    >>> config.verbose = True  # Add new attribute
    >>> config.debug = False  # Attempt to modify existing attribute
    Traceback (most recent call last):
        ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'debug'.
'''
# pylint: enable=line-too-long


from . import __


def _check_behavior( obj: object ) -> bool:
    behaviors: __.cabc.MutableSet[ str ]
    if _check_dict( obj ):
        attributes = getattr( obj, '__dict__' )
        behaviors = attributes.get( '_behaviors_', set( ) )
    else: behaviors = getattr( obj, '_behaviors_', set( ) )
    return __.behavior_label in behaviors


def _check_dict( obj: object ) -> bool:
    # Return False even if '__dict__' in '__slots__'.
    if hasattr( obj, '__slots__' ): return False
    return hasattr( obj, '__dict__' )


def accretive( class_: type[ __.C ] ) -> type[ __.C ]: # pylint: disable=too-complex
    ''' Decorator which makes class accretive after initialization.

        Cannot be applied to classes which define their own __setattr__
        or __delattr__ methods.
    '''
    for method in ( '__setattr__', '__delattr__' ):
        if method in class_.__dict__:
            from .exceptions import DecoratorCompatibilityError
            raise DecoratorCompatibilityError( class_.__name__, method )
    original_init = next(
        base.__dict__[ '__init__' ] for base in class_.__mro__
        if '__init__' in base.__dict__ ) # pylint: disable=magic-value-comparison

    def __init__(
        self: object, *posargs: __.typx.Any, **nomargs: __.typx.Any
    ) -> None:
        # TODO: Use accretive set for behaviors.
        original_init( self, *posargs, **nomargs )
        behaviors: __.cabc.MutableSet[ str ]
        if _check_dict( self ):
            attributes = getattr( self, '__dict__' )
            behaviors = attributes.get( '_behaviors_', set( ) )
            if not behaviors: attributes[ '_behaviors_' ] = behaviors
            setattr( self, '__dict__', __.AccretiveDictionary( attributes ) )
        else:
            behaviors = getattr( self, '_behaviors_', set( ) )
            if not behaviors: setattr( self, '_behaviors_', behaviors )
        behaviors.add( __.behavior_label )

    def __delattr__( self: object, name: str ) -> None:
        if _check_behavior( self ): # pragma: no branch
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__delattr__( name ) # pragma: no cover

    def __setattr__( self: object, name: str, value: __.typx.Any ) -> None:
        if _check_behavior( self ) and hasattr( self, name ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__setattr__( name, value )

    class_.__init__ = __init__
    class_.__delattr__ = __delattr__
    class_.__setattr__ = __setattr__
    return class_


@accretive
class Object:
    ''' Accretive objects. '''

    __slots__ = ( '__dict__', '_behaviors_' )

    def __repr__( self ) -> str:
        return "{fqname}( )".format( fqname = __.calculate_fqname( self ) )

Object.__doc__ = __.generate_docstring(
    Object, 'instance attributes accretion' )
