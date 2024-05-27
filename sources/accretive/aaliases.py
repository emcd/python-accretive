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


''' Abbreviated aliases to accretive data structures.

    Similar to Python builtins.
'''

# ruff: noqa: F401
# pylint: disable=unused-import


from . import __
from .classes import ABCFactory as acabcmeta, Class as actype
from .dictionaries import (
    Dictionary as acdict,
    ProducerDictionary as acdefaultdict,
)
from .modules import Module as acmodule
from .namespaces import Namespace as acnamespace
from .objects import Object as acobject


__all__ = __.discover_public_attributes( globals( ) )
