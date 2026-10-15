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


''' Common names and type aliases. '''

# ruff: noqa: F401


from . import imports as __


from classcore.standard.nomina import ( # isort: skip
                            AssignerLigation,
                            AttributesNamer,
                            BehaviorExclusionNamesOmni,
                            BehaviorExclusionRegexes,
                            BehaviorExclusionPredicates,
                            BehaviorExclusionVerifiersOmni,
                            ClassDecorator,
                            ClassDecorators,
                            ClassDecoratorFactory,
    DecorationPreparers as  ClassDecorationPreparers,
                            DynadocConfiguration,
                            ErrorClassProvider,
                            ModuleReclassifier,
                            concealment_label,
                            immutability_label,
                            is_public_identifier,
)


H = __.typx.TypeVar( 'H', bound = __.cabc.Hashable ) # Hash Key
T = __.typx.TypeVar( 'T', bound = type ) # Class
U = __.typx.TypeVar( 'U' )  # Class
V = __.typx.TypeVar( 'V' ) # Value


ComparisonResult: __.typx.TypeAlias = bool | __.types.NotImplementedType
NominativeArguments: __.typx.TypeAlias = __.cabc.Mapping[ str, __.typx.Any ]
PositionalArguments: __.typx.TypeAlias = __.cabc.Sequence[ __.typx.Any ]

DictionaryNominativeArgument: __.typx.TypeAlias = __.typx.Annotated[
    V,
    __.ddoc.Doc(
        'Zero or more keyword arguments from which to initialize '
        'dictionary data.' ),
]
DictionaryPositionalArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.cabc.Mapping[ H, V ] | __.cabc.Iterable[ tuple[ H, V ] ],
    __.ddoc.Doc(
        'Zero or more iterables from which to initialize dictionary data. '
        'Each iterable must be dictionary or sequence of key-value pairs. '
        'Duplicate keys will result in an error.' ),
]
DictionaryProducer: __.typx.TypeAlias = __.typx.Annotated[
    __.cabc.Callable[ [ ], V ],
    __.ddoc.Doc(
        'Callable which produces values for absent dictionary entries.' ),
]
DictionaryValidator: __.typx.TypeAlias = __.typx.Annotated[
    __.cabc.Callable[ [ H, V ], bool ],
    __.ddoc.Doc(
        'Callable which validates entries before addition to dictionary.' ),
]


package_name = __name__.split( '.', maxsplit = 1 )[ 0 ]


_levels = frozenset( ( 'class', 'classes', 'instance', 'instances' ) )
_cores = frozenset( (
    'behaviors',
    'construction_arguments',
    'dynadoc_configuration',
    'in_progress',
    'mutables_names', 'mutables_predicates', 'mutables_regexes',
    'visibles_names', 'visibles_predicates', 'visibles_regexes',
    'assigner_core', 'deleter_core', 'surveyor_core' ) )
_hex_digits = frozenset( '0123456789abcdef' )
_digest_length = 64
_mangled_cores = frozenset( ( 'class_behaviors', 'class_in_progress' ) )


class AttrnameCalculator:
    ''' Calculates framework attribute names from level and core.

        Mirrors the classcore reference implementation with the accretive
        package prefix. Exposes the ``is_internal_name`` detector consumed
        by classcore 1.13+ metaclass-carried internal-name contributions,
        so accretive internal names flow into attribute explanations and
        concealment.
    '''

    def is_internal_name( self, name: str ) -> bool:
        prefix = f"_{package_name}_"
        if not name.startswith( prefix ):
            return False
        body = name[ len( prefix ): ]
        # Static stems: _{package}_{level}_{core}_ with trailing underscore.
        # The class-level behaviors and in_progress stems are stored
        # mangled only, so they are excluded from static acceptance.
        if body.endswith( '_' ):
            level, _, core = body[ :-1 ].partition( '_' )
            if level in _levels and core in _cores:
                return not (
                    'class' == level
                    and f"{level}_{core}" in _mangled_cores )
            return False
        # Mangled forms: one of the mangled cores + 64 lowercase hex,
        # no trailing underscore. The classcore mangling accessors append
        # digests to these stems only.
        for mangled_core in _mangled_cores:
            mangled_prefix = f"{mangled_core}_"
            if body.startswith( mangled_prefix ):
                suffix = body[ len( mangled_prefix ): ]
                return (
                    _digest_length == len( suffix )
                    and all( c in _hex_digits for c in suffix ) )
        return False

    def __call__( self, level: str, core: str ) -> str:
        return f"_{package_name}_{level}_{core}_"


calculate_attrname = AttrnameCalculator( )
