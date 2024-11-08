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


''' Qualified aliases to accretive data structures.

    Useful for avoiding namespace collisions from attribute imports.
'''

# ruff: noqa: F401
# pylint: disable=unused-import


from . import __
from .classes import (
    ABCFactory as           AccretiveABCFactory,
    Class as                AccretiveClass,
)
from .dictionaries import (
    Dictionary as           AccretiveDictionary,
    ProducerDictionary as   AccretiveProducerDictionary,
)
from .modules import (
    Module as               AccretiveModule,
    reclassify_modules as   reclassify_modules_as_accretive,
)
from .namespaces import (
    Namespace as            AccretiveNamespace,
)
from .objects import (
    Object as               AccretiveObject,
)
