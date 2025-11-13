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


*******************************************************************************
Suggested Architectural Decision Records
*******************************************************************************

This document lists potential ADRs that could be created to document the
architectural decisions already implemented in the codebase. These are provided
as suggestions for future documentation efforts.

ADR-001: Metaclass-Based Interception for Accretive Behavior
===============================================================================

**Decision**: Use metaclass-based interception via ``__setattr__`` and
``__delattr__`` hooks that delegate to a configurable ``assigner_core``
function.

**Context**: Need to intercept attribute assignment to enforce immutability
after first assignment. Multiple approaches available: descriptors,
``__getattribute__``/``__setattr__`` overrides, proxies, metaclasses.

**Key Alternatives**:

* Descriptors: Only work for class-level attributes, not instance attributes
* Direct ``__setattr__`` override: Doesn't integrate well with class factory
  pattern
* Proxies: Add indirection and complicate type checking

**Consequences**: Consistent behavior across all accretive types, integration
with classcore's class factory system, single metaclass constraint, clean
separation of assignment logic from type definitions.

ADR-002: Grow-Only Semantics vs Other Immutability Patterns
===============================================================================

**Decision**: Implement accretive (grow-only) semantics: values can be added
but never modified or removed.

**Context**: Need immutability guarantees for collections. Multiple patterns
available: fully immutable, copy-on-write, persistent data structures,
accretive (grow-only).

**Key Alternatives**:

* Fully immutable: No growth after initialization (frozen dataclasses, tuples)
* Copy-on-write: Performance overhead, memory consumption
* Persistent data structures: Complexity, unfamiliar APIs

**Consequences**: Middle ground between mutable and immutable, useful for
registries/plugins/caches, shallow immutability only, clear use case
differentiation from existing libraries.

ADR-003: Integration with classcore Class Factory
===============================================================================

**Decision**: Build on classcore's ``class_factory`` and behavior configuration
system.

**Context**: Need consistent behavior configuration across multiple class types
(Class, Dataclass, Module, etc.). Could implement from scratch or build on
existing infrastructure.

**Key Alternatives**:

* Implement custom metaclass infrastructure: Duplication, maintenance burden
* Use standard Python mechanisms only: Less flexibility, more boilerplate

**Consequences**: Dependency on classcore package, consistent configuration API
across all types, reuse of well-tested behavior management code, leverages
dynadoc integration and behavior exclusions (mutables predicates/regexes).

ADR-004: Exception Hierarchy Multiple Inheritance
===============================================================================

**Decision**: Use multiple inheritance for exceptions: inherit from both package
base (``Omnierror``) and appropriate standard library exceptions
(``AttributeError``, ``TypeError``, ``ValueError``).

**Context**: Need exceptions that are both package-specific (for targeted
catching) and compatible with standard library exception handling patterns.

**Key Alternatives**:

* Only inherit from package base: Breaks compatibility with standard exception
  handlers
* Only inherit from stdlib: Can't catch all package errors with single base

**Consequences**: Both specific (``catch AttributeImmutability``) and general
(``catch Omnierror``) handling possible, compatible with standard exception
hierarchies, clear isinstance checks work as expected.
