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


''' Protected accretive data structures. '''

# ruff: noqa: F401,F403


from .. import __
from . import aaliases
from . import classes
from . import dictionaries
from . import modules
from . import namespaces
from . import objects
from . import qaliases

from .classes import *
from .dictionaries import *
from .modules import *
from .namespaces import *
from .objects import *


__doc__ = __.generate_docstring(
    __.Docstring( __doc__ ),
    'subpackage behavior: attributes accretion',
    'subpackage behavior: protection of classes' )


__all__ = __.discover_public_attributes( globals( ) )
