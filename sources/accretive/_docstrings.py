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


''' Docstrings table for reuse across subpackages. '''


from types import MappingProxyType as _DictionaryProxy


TABLE = _DictionaryProxy( {

    'abc attributes exemption': '''
Derived from and compatible with :py:class:`abc.ABCMeta`. The
``__abstractmethods__`` class attribute and the class attributes, whose names
start with ``_abc_``, are exempt from the accretion mechanism so that the
internal method abstraction machinery can function correctly.
''',

    'class attributes accretion': '''
Prevents reassignment or deletion of class attributes after they have been
assigned. Only assignment of new class attributes is permitted.
''',

    'class attributes concealment': '''
By default, all class attributes, whose names do not start with ``_``, are
returned from an invocation of :py:func:`dir`. Additional class attributes can
be returned, if the ``_class_attribute_visibility_includes_`` attribute is
provided on a subclass.
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

    'dictionary entries accretion': '''
Prevents alteration or removal of dictionary entries after they have been
added. Only addition of new dictionary entries is permitted.
''',

    'dictionary entries production': '''
When an attempt to access a missing entry is made, then the entry is added with
a default value. Modeled after :py:class:`collections.defaultdict`.
''',

    'instance attributes accretion': '''
Prevents reassignment or deletion of instance attributes after they have been
assigned. Only assignment of new instance attributes is permitted.
''',

    'instance attributes concealment': '''
By default, all instance attributes, whose names do not start with ``_``, are
returned from an invocation of :py:func:`dir`. Additional instance attributes
can be returned, if the ``_attribute_visibility_includes_`` attribute is
provided on a subclass.
''',

    'module attributes accretion': '''
Prevents reassignment or deletion of module attributes after they have been
assigned. Only assignment of new module attributes is permitted.
''',

    'module attributes concealment': '''
By default, all module attributes, whose names do not start with ``_``, are
returned from an invocation of :py:func:`dir`. Additional module attributes
can be returned, if the ``_attribute_visibility_includes_`` attribute is
provided on a subclass.
''',

    'protection of class': '''
Enforcement of attributes accretion on this class, itself, is in effect.
''',

    'protection of class factory class': '''
Enforcement of attributes accretion on this metaclass, itself, is in effect.
''',

    'protection of module class': '''
Enforcement of attributes accretion on this module class, itself, is in effect.
''',

    'subpackage behavior: attributes accretion': '''
Accretive data structures can grow at any time but can never shrink. An
accretive dictionary accepts new entires, but cannot have existing entries
altered or removed. Similarly, an accretive namespace accepts new attributes,
but cannot have existing attributes assigned to new values or deleted.
''',

    'subpackage behavior: attributes concealment': '''
Data structures, provided by this subpackage, have concealed attributes.
Concealed attributes do not appear in listings via the :py:func:`dir` builtin
function. By default, only attributes names, which do not start with ``_`` are
made visible, but additional attributes can be included if they are listed on a
particular class attribute that the concealer honors.
''',

    'subpackage behavior: protection of classes': '''
Classes of data structures, provided by this subpackage, have protected
attributes. Attributes are accreted on these classes and cannot be reassigned
or deleted.
''',

} )


__all__ = ( )
