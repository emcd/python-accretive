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


''' Standard annotations across Python versions. '''

# ruff: noqa: F401
# pylint: disable=unused-import


from types import ModuleType as Module

from typing_extensions import (
    Annotated as Annotation,
    Any,
    Callable,
    Collection,     # TODO: Python 3.9: collections.abc.Collection
    Dict,           # TODO: Python 3.9: dict
    Doc,
    Hashable,       # TODO: Python 3.9: collections.abc.Hashable
    ItemsView,      # TODO: Python 3.9: collections.abc.ItemsView
    Iterable,       # TODO: Python 3.9: collections.abc.Iterable
    Iterator,       # TODO: Python 3.9: collections.abc.Iterator
    KeysView,       # TODO: Python 3.9: collections.abc.KeysView
    Mapping,        # TODO: Python 3.9: collections.abc.Mapping
    MutableMapping, # TODO: Python 3.9: collections.abc.MutableMapping
    Never,
    Self,
    Tuple,          # TODO: Python 3.9: collections.abc.Sequence
    Type,           # TODO: Python 3.9: type
    TypeAlias,
    Union,          # TODO: Python 3.10: bitwise-OR operator ('|')
    ValuesView,     # TODO: Python 3.9: collections.abc.ValuesView
    cast,
)


# TODO? Python 3.10: Import 'NotImplementedType' from 'types'.
# Note: According to https://stackoverflow.com/a/75185542/14833542,
#       Mypy implicitly considers 'NotImplemented' as a result of the dunder
#       methods for comparison.
#ComparisonResult: TypeAlias = Union[ bool, NotImplementedType ]
ComparisonResult: TypeAlias = bool

DictionaryNominativeArgument: TypeAlias = Annotation[
    Any,
    Doc(
        'Zero or more keyword arguments from which to initialize '
        'dictionary data.' )
]

# TODO: Support taking our dictionaries, themselves, as arguments.
#       Supposed to work via structural typing, but must match protocol.
#       https://github.com/python/mypy/issues/2922
#       https://github.com/python/mypy/issues/2922#issuecomment-1186587232
#       https://github.com/python/typing/discussions/1127#discussioncomment-2538837
#       https://mypy.readthedocs.io/en/latest/protocols.html
DictionaryPositionalArgument: TypeAlias = Annotation[
    Union[ Mapping[ Hashable, Any ], Iterable[ Tuple[ Hashable, Any] ] ],
    Doc(
        'Zero or more iterables from which to initialize dictionary data. '
        'Each iterable must be dictionary or sequence of key-value pairs. '
        'Duplicate keys will result in an error.' )
]

DictionaryProducer: TypeAlias = Annotation[
    Callable[ [ ], Any ],
    Doc( 'Callable which produces values for absent dictionary entries.' )
]

ModuleReclassifier: TypeAlias = Callable[ [ Mapping[ str, Any ] ], None ]


__all__ = ( )
