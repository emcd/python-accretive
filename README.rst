Contains a Python library package that provides accretive data structures.
These are data structures which grow but do not shrink. In other words, entries
can be added to them but altered or removed.

Examples
===============================================================================


Accretive Namespace
-------------------------------------------------------------------------------

>>> from accretive import Namespace
>>> ns = Namespace( apples = 12, bananas = 6, cherries = 42 )
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42 )
>>> ns.blueberries = 96
>>> ns.strawberries = 24
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )
>>> del ns.apples
Traceback (most recent call last):
...
accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.
>>> ns.apples = 14
Traceback (most recent call last):
...
accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )


Accretive Dictionary
-------------------------------------------------------------------------------

>>> from accretive import Dictionary
>>> dct = Dictionary( apples = 12, bananas = 6, cherries = 42 )
>>> dct
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42} )
>>> dct.update( blueberries = 96, strawberries = 24 )
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )
>>> del dct[ 'bananas' ]
Traceback (most recent call last):
...
accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.
>>> dct[ 'bananas' ] = 11
Traceback (most recent call last):
...
accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.
>>> dct
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )


Installation
===============================================================================

::

      pip install accretive


.. todo:: Entities of interest.

.. todo:: Examples of use.
