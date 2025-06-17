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

# ruff: noqa: F811


from . import __


is_public_identifier = __.is_public_identifier
mutables_default = ( )
visibles_default = ( is_public_identifier, )


def assign_attribute_if_absent_mutable( # noqa: PLR0913
    objct: object, /, *,
    ligation: __.AssignerLigation,
    attributes_namer: __.AttributesNamer,
    error_class_provider: __.ErrorClassProvider,
    level: str,
    name: str,
    value: __.typx.Any,
) -> None:
    ''' Assigns attribute if it is absent or mutable, else raises error. '''
    if not hasattr( objct, name ):
        ligation( name, value )
        return
    leveli = 'instance' if level == 'instances' else level
    behaviors_name = attributes_namer( leveli, 'behaviors' )
    behaviors = __.ccutils.getattr0( objct, behaviors_name, frozenset( ) )
    if __.immutability_label not in behaviors:
        ligation( name, value )
        return
    names_name = attributes_namer( level, 'mutables_names' )
    names: __.BehaviorExclusionNamesOmni = (
        getattr( objct, names_name, frozenset( ) ) )
    if names == '*' or name in names:
        ligation( name, value )
        return
    predicates_name = attributes_namer( level, 'mutables_predicates' )
    predicates: __.BehaviorExclusionPredicates = (
        getattr( objct, predicates_name, ( ) ) )
    for predicate in predicates:
        if predicate( name ):
            # TODO? Cache predicate hit.
            ligation( name, value )
            return
    regexes_name = attributes_namer( level, 'mutables_regexes' )
    regexes: __.BehaviorExclusionRegexes = (
        getattr( objct, regexes_name, ( ) ) )
    for regex in regexes:
        if regex.fullmatch( name ):
            # TODO? Cache regex hit.
            ligation( name, value )
            return
    target = __.ccutils.describe_object( objct )
    raise error_class_provider( 'AttributeImmutability' )( name, target )


def _provide_error_class( name: str ) -> type[ Exception ]:
    ''' Provides error class for this package. '''
    match name:
        case 'AttributeImmutability':
            from .exceptions import AttributeImmutability as error
        case _:
            from .exceptions import ErrorProvideFailure
            raise ErrorProvideFailure( name, reason = 'Does not exist.' )
    return error


_dataclass_core = __.dcls.dataclass( kw_only = True, slots = True )
_dynadoc_configuration = (
    __.ccstd.dynadoc.produce_dynadoc_configuration(
        introspection = __.dynadoc_introspection_control_on_class,
        table = __.fragments ) )
_class_factory = __.funct.partial(
    __.ccstd.class_factory,
    assigner_core = assign_attribute_if_absent_mutable,
    attributes_namer = __.calculate_attrname,
    dynadoc_configuration = _dynadoc_configuration,
    error_class_provider = _provide_error_class )
_class_factory_immutable = __.funct.partial(
    __.ccstd.class_factory,
    attributes_namer = __.calculate_attrname,
    dynadoc_configuration = _dynadoc_configuration,
    error_class_provider = _provide_error_class )


@_class_factory( )
class Class( type ):
    ''' Metaclass for standard classes. '''

    _dynadoc_fragments_ = (
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class Dataclass( type ):
    ''' Metaclass for standard dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( kw_only_default = True )
class DataclassMutable( type ):
    ''' Metaclass for dataclasses with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
class AbstractBaseClass( __.abc.ABCMeta ):
    ''' Metaclass for standard abstract base classes. '''

    _dynadoc_fragments_ = (
        'cfc produce abstract base class',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
class ProtocolClass( type( __.typx.Protocol ) ):
    ''' Metaclass for standard protocol classes. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class ProtocolDataclass( type( __.typx.Protocol ) ):
    ''' Metaclass for standard protocol dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( kw_only_default = True )
class ProtocolDataclassMutable( type( __.typx.Protocol ) ):
    ''' Metaclass for protocol dataclasses with mutable instance attributes.
    '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
class _Class( type ):
    ''' Metaclass for immutable classes. '''

    _dynadoc_fragments_ = (
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class _Dataclass( type ):
    ''' Metaclass for immutable dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
@__.typx.dataclass_transform( kw_only_default = True )
class _DataclassMutable( type ):
    ''' Metaclass for immutable dataclasses with mutable instances. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
class _AbstractBaseClass( __.abc.ABCMeta ):
    ''' Metaclass for immutable abstract base classes. '''

    _dynadoc_fragments_ = (
        'cfc produce abstract base class',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
class _ProtocolClass( type( __.typx.Protocol ) ):
    ''' Metaclass for immutable protocol classes. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class _ProtocolDataclass( type( __.typx.Protocol ) ):
    ''' Metaclass for immutable protocol dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory_immutable( )
@__.typx.dataclass_transform( kw_only_default = True )
class _ProtocolDataclassMutable( type( __.typx.Protocol ) ):
    ''' Metaclass for immutable protocol dataclasses with mutable instances.
    '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class accrete', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


class Object( metaclass = _Class ):
    ''' Standard base class. '''

    _dynadoc_fragments_ = (
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance accrete' )


class ObjectMutable( metaclass = _Class, instances_mutables = '*' ):
    ''' Base class with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class DataclassObject( metaclass = _Dataclass ):
    ''' Standard base dataclass. '''

    _dynadoc_fragments_ = (
        'dataclass',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance accrete' )


class DataclassObjectMutable( metaclass = _DataclassMutable ):
    ''' Base dataclass with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'dataclass',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class Protocol( __.typx.Protocol, metaclass = _ProtocolClass ):
    ''' Standard base protocol class. '''

    _dynadoc_fragments_ = (
        'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance accrete' )


class ProtocolMutable(
    __.typx.Protocol, metaclass = _ProtocolClass, instances_mutables = '*'
):
    ''' Base protocol class with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class DataclassProtocol(
    __.typx.Protocol, metaclass = _ProtocolDataclass,
):
    ''' Standard base protocol dataclass. '''

    _dynadoc_fragments_ = (
        'dataclass', 'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance accrete' )


class DataclassProtocolMutable(
    __.typx.Protocol, metaclass = _ProtocolDataclassMutable,
):
    ''' Base protocol dataclass with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'dataclass', 'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


@__.typx.overload
def dataclass_with_standard_behaviors( # pragma: no cover
    cls: type[ __.U ], /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> type[ __.U ]: ...


@__.typx.overload
def dataclass_with_standard_behaviors( # pragma: no cover
    cls: __.AbsentSingleton = __.absent, /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> __.ClassDecoratorFactory[ __.U ]: ...


@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
def dataclass_with_standard_behaviors(
    cls: __.Absential[ type[ __.U ] ] = __.absent, /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> type[ __.U ] | __.ClassDecoratorFactory[ __.U ]:
    ''' Decorates dataclass to enforce standard behaviors on instances. '''
    decorate = __.funct.partial(
        __.ccstd.dataclass_with_standard_behaviors,
        attributes_namer = __.calculate_attrname,
        error_class_provider = _provide_error_class,
        assigner_core = assign_attribute_if_absent_mutable,
        decorators = decorators,
        mutables = mutables, visibles = visibles )
    if not __.is_absent( cls ): return decorate( )( cls )
    return decorate( )  # No class to decorate; keyword arguments only.


@__.typx.overload
def with_standard_behaviors( # pragma: no cover
    cls: type[ __.U ], /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> type[ __.U ]: ...


@__.typx.overload
def with_standard_behaviors( # pragma: no cover
    cls: __.AbsentSingleton = __.absent, /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> __.ClassDecoratorFactory[ __.U ]: ...


def with_standard_behaviors(
    cls: __.Absential[ type[ __.U ] ] = __.absent, /, *,
    decorators: __.ClassDecorators[ __.U ] = ( ),
    mutables: __.BehaviorExclusionVerifiersOmni = mutables_default,
    visibles: __.BehaviorExclusionVerifiersOmni = visibles_default,
) -> type[ __.U ] | __.ClassDecoratorFactory[ __.U ]:
    ''' Decorates class to enforce standard behaviors on instances. '''
    decorate = __.funct.partial(
        __.ccstd.with_standard_behaviors,
        attributes_namer = __.calculate_attrname,
        error_class_provider = _provide_error_class,
        assigner_core = assign_attribute_if_absent_mutable,
        decorators = decorators,
        mutables = mutables, visibles = visibles )
    if not __.is_absent( cls ): return decorate( )( cls )
    return decorate( )  # No class to decorate; keyword arguments only.
