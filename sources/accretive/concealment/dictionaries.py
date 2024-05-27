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


''' Accretive dictionaries with attributes concealment. '''


from .. import __
from .. import dictionaries as _dictionaries


class Dictionary( __.ConcealerExtension, _dictionaries.Dictionary ):
    ''' Simple accretive dictionary.

        Cannot alter or remove existing entries.
    '''


class ProducerDictionary(
    __.ConcealerExtension,
    _dictionaries.ProducerDictionary
):
    ''' Accretive dictionary which produces values for missing entries.

        Cannot alter or remove existing entries.

        Accretive equivalent to 'collections.defaultdict'.
    '''


__all__ = __.discover_public_attributes( globals( ) )
