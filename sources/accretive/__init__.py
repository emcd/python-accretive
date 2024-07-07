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


''' Accretive data structures. '''

# ruff: noqa: F401,F403


from . import __
from . import aaliases
from . import classes
from . import complete
from . import concealment
from . import dictionaries
from . import exceptions
from . import modules
from . import namespaces
from . import objects
from . import protection
from . import qaliases

from .classes import *
from .dictionaries import *
from .modules import *
from .namespaces import *
from .objects import *


_subpackages = ( concealment, protection, complete )


__doc__ = __.generate_docstring(
    __.Docstring( __doc__ ),
    'subpackage behavior: attributes accretion',
    __.Docstring(
        'Subpackages with variants of the data structures are available:' ),
    __.Docstring( '\n\n'.join(
        "* :py:mod:`{name}`: {headline}".format(
            name = package.__package__,
            headline = (
                package.__doc__ or '' ).split( '\n', maxsplit = 1 )[ 0 ] )
        for package in _subpackages ) ) )


__all__ = __.discover_public_attributes( globals( ) )
__version__ = '1.0.1'


complete.modules.reclassify_modules( globals( ) )
for _subpackage in _subpackages:
    complete.modules.reclassify_modules( vars( _subpackage ) )
_attribute_visibility_includes_ = frozenset( ( '__version__', ) )
__.modules[ __package__ ].__class__ = complete.modules.Module
