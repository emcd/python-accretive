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


''' Docstrings table for reuse across entities. '''


from . import imports as __


fragments: __.cabc.Mapping[ str, str ] = __.types.MappingProxyType( {

    'cfc class accrete':
    ''' By default, accretes class attributes. ''',

    'cfc class conceal':
    ''' By default, conceals non-public class attributes. ''',

    'cfc class protect':
    ''' By default, protects class attributes. ''',

    'cfc dynadoc': ''' Applies Dynadoc decoration to classes. ''',

    'cfc instance accrete':
    ''' Produces classes which can accrete instance attributes. ''',

    'cfc instance conceal':
    ''' Produces classes which can conceal instance attributes. ''',

    'cfc instance protect':
    ''' Produces classes which can protect instance attributes. ''',

    'cfc produce abstract base class':
    ''' Produces abstract base classes compatible with :py:class:`abc.ABCMeta`.
    ''',

    'cfc produce dataclass':
    ''' Produces inheritable dataclasses with keyword-only instantiation. ''',

    'cfc produce protocol class':
    ''' Produces :pep:`544` protocol classes. ''',

    'class accretion':
    ''' By default, class attributes are accretive. ''',

    'class concealment':
    ''' By default, non-public class attributes are invisible. ''',

    'class protection':
    ''' By default, class attributes are immutable. ''',

    'class instance accrete':
    ''' By default, accretes instance attributes. ''',

    'class instance conceal':
    ''' By default, conceals non-public instance attributes. ''',

    'class instance protect':
    ''' By default, protects instance attributes. ''',

    'dataclass':
    ''' Inheritable dataclass with keyword-only instantiation. ''',

    'protocol class':
    ''' Protocol class (:pep:`544`). Nominal and structural subtyping. ''',

    'class dynadoc': ''' Is decorated by Dynadoc. ''',

    'dictionary entries accrete': ''' Accretes dictionary entries. ''',

    'dictionary entries produce':
    ''' Produces default entries on attempt to access absent ones. ''',

    'dictionary entries validate':
    ''' Validates dictionary entries on initialization. ''',

    'module':
    ''' Python module class, derived from :py:class:`types.ModuleType`. ''',

    'module conceal':
    ''' By default, conceals non-public module attributes. ''',

    'module protect':
    ''' By default, protects module attributes. ''',

    'namespace':
    ''' Namespace object, modeled after :py:class:`types.SimpleNamespace. ''',

    'class attributes accretion': '''
Prevents reassignment or deletion of class attributes after they have been
assigned. Only assignment of new class attributes is permitted.
''',

    'description of class factory class': '''
Derived from :py:class:`type`, this is a metaclass. A metaclass is a class
factory class. I.e., it is a class that produces other classes as its
instances.
''',

    'description of module': '''
Derived from :py:class:`types.ModuleType`, this class is suitable for use as a
Python module class.
''',

    'description of namespace': '''
A namespace is an object, whose attributes can be determined from iterables and
keyword arguments, at initialization time. The string representation of the
namespace object reflects its current instance attributes. Modeled after
:py:class:`types.SimpleNamespace`.
''',

    'instance attributes accretion': '''
Prevents reassignment or deletion of instance attributes after they have been
assigned. Only assignment of new instance attributes is permitted.
''',

    'module attributes accretion': '''
Prevents reassignment or deletion of module attributes after they have been
assigned. Only assignment of new module attributes is permitted.

This behavior helps ensure that module-level constants remain constant and that
module interfaces remain stable during runtime.
''',

} )
