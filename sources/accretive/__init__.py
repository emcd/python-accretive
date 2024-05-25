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


''' Accretive data structures.

    Accretive data structures can grow but never shrink. Once something is
    added to them, it cannot be altered or removed. They are particularly
    useful for registrations, collected during initialization, which then must
    be part of guaranteed state during later runtime. '''

# ruff: noqa: F401,F403


from . import __
from . import aaliases
from . import classes
from . import dictionaries
from . import exceptions
from . import modules
from . import namespaces
from . import objects
from . import qaliases

from .classes import *
from .dictionaries import *
from .exceptions import *
from .modules import *
from .namespaces import *
from .objects import *


__all__ = __.discover_public_attributes( globals( ) )
__version__ = '1.0a202405121610'


modules.reclassify_modules( globals( ) )
_attribute_visibility_includes_ = frozenset( ( '__version__', ) )
__.modules[ __package__ ].__class__ = modules.ConcealerModule
