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


Module
===============================================================================

Accretive modules have an interface nearly equivalent to
:py:class:`types.ModuleType`, i.e., standard Python modules. However, once an
attribute has been assigned, it cannot be reassigned or deleted. This protects
accretive modules from accidental (or unsophisticated malicious) tampering.

.. doctest:: Module

    >>> from accretive import Module

Initialization
-------------------------------------------------------------------------------

While modules are typically initialized during import of their sources, they
may also be created dynamically. As with standard Python modules, a name is
required when dynamically creating a module.

.. doctest:: Module

    >>> m = Module( 'foo' )
    >>> m
    <module 'foo'>

Immutability
-------------------------------------------------------------------------------

Existing attributes cannot be reassigned.

.. doctest:: Module

    >>> m.__name__
    'foo'
    >>> m.__name__ = 'bar'
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute '__name__'.

Or deleted.

.. doctest:: Module

    >>> del m.__name__
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute '__name__'.

Attribute Assignment
-------------------------------------------------------------------------------

However, new attributes can be assigned.

.. doctest:: Module

    >>> m.__version__ = '1.0a3'
    >>> vars( m )
    {'__name__': 'foo', '__doc__': None, '__package__': None, '__loader__': None, '__spec__': None, '__version__': '1.0a3'}

Reclassification
-------------------------------------------------------------------------------

Existing non-accretive modules can be reclassified as accretive modules. For
application developers, this can provide an extra layer of safety around some
modules. (However, library developers should never reclassify any modules
except those in the packages that they distribute. Reclassifying other modules
that are used by applications could break contracts.)

Consider the following scenario:

.. doctest:: Module

    >>> import getpass
    >>> true_getpass = getpass.getpass
    >>> import functools
    >>> @functools.wraps( true_getpass )
    ... def pwned_getpass( prompt = 'Password: ', stream = None ):
    ...     password = true_getpass( prompt = prompt, stream = stream )
    ...     # Send intercepted password, stack trace, and host details to malicious collector.
    ...     return password
    ...
    >>> getpass.getpass = pwned_getpass

In the above scenario, a "trusted" standard library module has been
monkey-patched to provide a compromised function. We can prevent
unsophisticated monkey-patching by reclassifying the module.

.. doctest:: Module

    >>> getpass.getpass = true_getpass
    >>> getpass.__class__ = Module
    >>> getpass.getpass = pwned_getpass
    Traceback (most recent call last):
    ...
    accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'getpass'.

.. warning::

    We are unable to prevent tampering of a module's underlying attributes
    dictionary, ``__dict__``. So, accretive modules do not provide any true
    resistance against determined tampering. They do provide security against
    accidental alterations of attributes though.

Mass Reclassification
-------------------------------------------------------------------------------

For cases where multiple modules should be reclassified, a convenience function
is provided. This function looks for all modules in a dictionary, such as the
attributes dictionary for another module, and reclassifies the modules to
accretive modules.

.. code-block:: python

    from accretive import reclassify_modules
    reclassify_modules( globals( ) )
