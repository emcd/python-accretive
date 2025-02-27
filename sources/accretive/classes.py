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
''' Accretive classes.

    Provides metaclasses for creating classes with accretive attributes. Once a
    class attribute is set, it cannot be reassigned or deleted.

    The implementation includes:

    * ``Class``: Standard metaclass for accretive classes; derived from
      :py:class:`type`.
    * ``ABCFactory``: Metaclass for abstract base classes; derived from
      :py:class:`abc.ABCMeta`.
    * ``ProtocolClass``: Metaclass for protocol classes; derived from
      :py:class:`typing.Protocol`.

    These metaclasses are particularly useful for:

    * Creating classes with constant class attributes
    * Defining stable abstract base classes
    * Building protocol classes with fixed interfaces

    >>> from accretive import Class
    >>> class Example( metaclass = Class ):
    ...     x = 1
    >>> Example.y = 2  # Add new class attribute
    >>> Example.x = 3  # Attempt reassignment
    Traceback (most recent call last):
        ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete attribute 'x'.

    For cases where some attributes need to remain mutable, use the ``mutables`` parameter:

    >>> class Config( metaclass = Class, mutables = ( 'version', ) ):
    ...     name = 'MyApp'
    ...     version = '1.0.0'
    >>> Config.version = '1.0.1'  # Can modify designated mutable attributes
    >>> Config.version
    '1.0.1'
    >>> Config.name = 'NewApp'    # Other attributes remain immutable
    Traceback (most recent call last):
        ...
    accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete attribute 'name'.
'''
# pylint: enable=line-too-long

# TODO? Allow predicate functions and regex patterns as mutability checkers.


from __future__ import annotations

from . import __


ClassDecorators: __.typx.TypeAlias = (
    __.cabc.Iterable[ __.cabc.Callable[ [ type ], type ] ] )


_behavior = 'accretion'


class Class( type ):
    ''' Accretive class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        clscls: type[ Class ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> Class:
        class_ = type.__new__(
            clscls, name, bases, namespace, **args )
        return _class__new__(
            class_,
            decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

Class.__doc__ = __.generate_docstring(
    Class,
    'description of class factory class',
    'class attributes accretion' )


class ABCFactory( __.abc.ABCMeta ):
    ''' Accretive abstract base class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        clscls: type[ ABCFactory ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> ABCFactory:
        class_ = __.abc.ABCMeta.__new__(
            clscls, name, bases, namespace, **args )
        return _class__new__(
            class_,
            decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ABCFactory.__doc__ = __.generate_docstring(
    ABCFactory,
    'description of class factory class',
    'class attributes accretion' )


# pylint: disable=bad-classmethod-argument,no-self-argument
class ProtocolClass( type( __.typx.Protocol ) ):
    ''' Accretive protocol class factory. '''

    def __new__( # pylint: disable=too-many-arguments
        clscls: type[ ProtocolClass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> ProtocolClass:
        class_ = super( ProtocolClass, clscls ).__new__( # pylint: disable=too-many-function-args
            clscls, name, bases, namespace, **args )
        return _class__new__(
            class_,
            decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )
# pylint: enable=bad-classmethod-argument,no-self-argument

ProtocolClass.__doc__ = __.generate_docstring(
    ProtocolClass,
    'description of class factory class',
    'class attributes accretion' )


def _accumulate_mutables(
    class_: type, mutables: __.cabc.Collection[ str ]
) -> frozenset[ str ]:
    return frozenset( mutables ).union( *(
        frozenset( base.__dict__.get( '_class_mutables_', ( ) ) )
        for base in class_.__mro__ ) )

# pylint: disable=protected-access
def _class__new__(
    original: type,
    decorators: ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    mutables: __.cabc.Collection[ str ] = ( ),
) -> type:
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    class_decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if class_decorators_: return original
    if not __.is_absent( docstring ): original.__doc__ = docstring
    original._class_mutables_ = _accumulate_mutables( original, mutables )
    original._class_decorators_ = class_decorators_
    reproduction = original
    for decorator in decorators:
        class_decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            __.repair_class_reproduction( original, reproduction )
        original = reproduction
    class_decorators_.clear( )  # Flag '__init__' to enable accretion
    return reproduction
# pylint: enable=protected-access


# pylint: disable=protected-access
def _class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set immutability.
    # Consult class attributes dictionary to ignore immutable base classes.
    cdict = class_.__dict__
    if cdict.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := cdict.get( '_class_behaviors_' ) ):
        class_behaviors.add( _behavior )
    else: class_._class_behaviors_ = { _behavior }
# pylint: enable=protected-access


def _class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore accretive base classes.
    cdict = class_.__dict__
    if name in cdict.get( '_class_mutables_', ( ) ): return False
    if _behavior not in cdict.get( '_class_behaviors_', ( ) ): return False
    from .exceptions import AttributeImmutabilityError
    raise AttributeImmutabilityError( name )


def _class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore accretive base classes.
    cdict = class_.__dict__
    if name in cdict.get( '_class_mutables_', ( ) ): return False
    if _behavior not in cdict.get( '_class_behaviors_', ( ) ): return False
    if hasattr( class_, name ):
        from .exceptions import AttributeImmutabilityError
        raise AttributeImmutabilityError( name )
    return False  # Allow setting new attributes
