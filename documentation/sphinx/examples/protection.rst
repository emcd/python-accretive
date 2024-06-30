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


Protection
===============================================================================

The ``accretive.protection`` subpackage offers variants on the main package
modules. The variants are classes with accretive attributes, ensuring that the
classes, themselves, for various kinds of accretive data structures are not
susceptible to accidental state change.

.. doctest:: Protection

    >>> from accretive.protection import Object

Let us illustrate this use case by defining a protected accretive object class.

.. doctest:: Protection

    >>> class MyProtectedObject( Object ):
    ...     class_attr = 'Cannot be changed'
    ...
    >>> MyProtectedObject.class_attr
    'Cannot be changed'

Attempting to reassign the protected class attribute raises an error.

.. doctest:: Protection

    >>> MyProtectedObject.class_attr = 'New value'
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'class_attr'.

Attempting to delete the protected class attribute also raises an error.

.. doctest:: Protection

    >>> del MyProtectedObject.class_attr
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'class_attr'.
