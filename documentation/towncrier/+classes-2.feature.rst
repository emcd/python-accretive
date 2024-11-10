Accept a ``decorators`` argument with all of the metaclasses to produce classes
which have a sequence of class decorators applied before class attribute
accretion is enforced. Some class decorators are compatible with accretion but
some are not; this gives a way to ensure that they are applied without
attribute enforcement. Advanced cases, such as ``dataclasses.dataclass( slots
= True )``, which produces a replacement class, are correctly supported by this
machinery on CPython.
