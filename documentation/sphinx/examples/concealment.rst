.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


Concealment
===============================================================================

The ``accretive.concealment`` subpackage offers variants on the main package
modules. These variants conceal all non-public attributes from the
:py:func:`dir` function by default. Normally hidden attributes can be exposed
on instances by providing a class attribute, named
``_attribute_visibility_includes_``. A similar
``_class_attribute_visibility_includes_`` attribute can be provided on
metaclasses to conceal class attributes.

.. doctest:: Concealment

    >>> from accretive.concealment import Object
    >>> class MyObject( Object ):
    ...     _attribute_visibility_includes_ = frozenset( ( '__dunder_attr__', ) )
    ...     def __init__( self ):
    ...         super( ).__init__( )
    ...         self.visible = 'hi'
    ...         self._hidden = '*lurks*'
    ...         self.__dunder_attr__ = 'hi!'
    ...
    >>> obj = MyObject( )
    >>> dir( obj )
    ['__dunder_attr__', 'visible']
    >>> obj._hidden
    '*lurks*'
    >>> obj.__dict__
    {'visible': 'hi', '_hidden': '*lurks*', '__dunder_attr__': 'hi!'}
