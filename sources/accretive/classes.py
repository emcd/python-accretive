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


from __future__ import annotations

from . import __


ClassDecorators: __.a.TypeAlias = (
    __.cabc.Iterable[ __.cabc.Callable[ [ type ], type ] ] )


_behavior = 'accretive'


class Class( type ):
    ''' Accretive class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: str = None, # TODO: Optional
        **args: __.a.Any
    ) -> Class:
        class_ = type.__new__(
            factory, name, bases, namespace, **args )
        return _class__new__( # type: ignore
            class_, decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

Class.__doc__ = __.generate_docstring(
    Class,
    'description of class factory class',
    'class attributes accretion'
)


class ABCFactory( __.ABCFactory ): # type: ignore
    ''' Accretive abstract base class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: str = None, # TODO: Optional
        **args: __.a.Any
    ) -> ABCFactory:
        class_ = __.ABCFactory.__new__(
            factory, name, bases, namespace, **args )
        return _class__new__( # type: ignore
            class_, decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ABCFactory.__doc__ = __.generate_docstring(
    ABCFactory,
    'description of class factory class',
    'class attributes accretion'
)


class ProtocolClass( __.a.Protocol.__class__ ): # type: ignore
    ''' Accretive protocol class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: str = None, # TODO: Optional
        **args: __.a.Any
    ) -> ProtocolClass:
        class_ = __.a.Protocol.__class__.__new__(
            factory, name, bases, namespace, **args )
        return _class__new__( # type: ignore
            class_, decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ProtocolClass.__doc__ = __.generate_docstring(
    ProtocolClass,
    'description of class factory class',
    'class attributes accretion'
)


def _class__new__(
    original: type,
    decorators: ClassDecorators = ( ),
    docstring: str = None, # TODO: Optional
) -> type:
    # Handle decorators similar to immutable implementation.
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    class_decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if class_decorators_: return original
    if docstring: original.__doc__ = docstring
    setattr( original, '_class_decorators_', class_decorators_ )
    reproduction = original
    for decorator in decorators:
        class_decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            _repair_class_reproduction( original, reproduction )
        original = reproduction
    class_decorators_.clear( )  # Flag '__init__' to enable accretion
    return reproduction


def _class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set accretion.
    if class_.__dict__.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := class_.__dict__.get( '_class_behaviors_' ) ):
        class_behaviors.add( _behavior )
    else: setattr( class_, '_class_behaviors_', { _behavior } )


def _class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore accretive base classes.
    if _behavior not in class_.__dict__.get( '_class_behaviors_', ( ) ):
        return False
    from .exceptions import IndelibleAttributeError
    raise IndelibleAttributeError( name )


def _class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore accretive base classes.
    if _behavior not in class_.__dict__.get( '_class_behaviors_', ( ) ):
        return False
    if hasattr( class_, name ):
        from .exceptions import IndelibleAttributeError
        raise IndelibleAttributeError( name )
    return False  # Allow setting new attributes


def _repair_class_reproduction( original: type, reproduction: type ) -> None:
    from platform import python_implementation
    match python_implementation( ):
        case 'CPython':
            _repair_cpython_class_closures( original, reproduction )


def _repair_cpython_class_closures( # pylint: disable=too-complex
    oldcls: type, newcls: type
) -> None:
    def try_repair_closure( function: __.cabc.Callable ) -> bool:
        try: index = function.__code__.co_freevars.index( '__class__' )
        except ValueError: return False
        closure = function.__closure__[ index ]
        if oldcls is closure.cell_contents: # pragma: no branch
            closure.cell_contents = newcls
            return True
        return False # pragma: no cover

    from inspect import isfunction, unwrap
    for attribute in newcls.__dict__.values( ): # pylint: disable=too-many-nested-blocks
        attribute_ = unwrap( attribute )
        if isfunction( attribute_ ) and try_repair_closure( attribute_ ):
            return
        if isinstance( attribute_, property ):
            for aname in ( 'fget', 'fset', 'fdel' ):
                accessor = getattr( attribute_, aname )
                if None is accessor: continue
                if try_repair_closure( accessor ): return # pragma: no branch
