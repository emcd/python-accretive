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


from typing import Any

from typing_extensions import (
    Annotated as Annotation,
    Dict,           # TODO: Python 3.9: collections.abc.Mapping
    Doc,
    Hashable,       # TODO: Python 3.9: collections.abc.Hashable
    Iterable,       # TODO: Python 3.9: collections.abc.Iterable
    Iterator,       # TODO: Python 3.9: collections.abc.Iterator
    Optional,
    Self,
    Tuple,          # TODO: Python 3.9: collections.abc.Sequence
    TypeAlias,
    Union,          # TODO: Python 3.10: bitwise-OR operator ('|')
)


DictionaryArgument: TypeAlias = Union[
    Dict[ Hashable, Any ],
    Iterable[ Tuple[ Hashable, Any] ],
]


__all__ = ( )
