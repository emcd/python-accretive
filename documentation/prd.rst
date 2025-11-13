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
Product Requirements Document
*******************************************************************************

Executive Summary
===============================================================================

Accretive is a Python library providing data structures that enforce a grow-only
constraint: values can be added but never modified or removed once set. The
library offers accretive variants of familiar Python types (dictionaries,
namespaces, classes, modules) with consistent APIs and flexible configuration
options for selective mutability.

The library addresses the need for collections that accumulate state with
immutability guarantees, particularly valuable for configuration registries,
plugin systems, and scenarios requiring sticky state. By providing a middle
ground between fully immutable and fully mutable collections, Accretive enables
developers to build safer, more predictable systems.

Problem Statement
===============================================================================

Who Experiences the Problem
-------------------------------------------------------------------------------

Python developers building systems that require:

* Configuration registries where entries must persist once registered
* Plugin architectures where registered extensions must remain available
* Caching systems where entries should never be invalidated
* Event handlers or callback registries with guaranteed availability
* Any scenario requiring grow-only collections with immutability guarantees

When and Where It Occurs
-------------------------------------------------------------------------------

The problem manifests in production systems when:

* Configuration values are accidentally overwritten, causing unpredictable behavior
* Plugin registrations are removed, breaking dependent functionality
* Cached entries are invalidated prematurely, causing performance issues
* State mutation creates race conditions in concurrent systems
* Debugging reveals unexpected state changes with unclear origins

Impact and Consequences
-------------------------------------------------------------------------------

Without accretive data structures:

* **Correctness Issues**: Accidental state mutation leads to bugs that are
  difficult to reproduce and diagnose
* **Concurrency Problems**: Mutable shared state creates race conditions and
  synchronization complexity
* **Maintenance Burden**: Developers must manually enforce immutability through
  documentation and code review
* **Runtime Failures**: State tampering can cause critical system failures in
  production environments
* **Testing Complexity**: Mutable state makes unit tests fragile and dependent
  on execution order

Current Workarounds and Limitations
-------------------------------------------------------------------------------

Existing approaches include:

* **Frozen dataclasses**: Provide immutability but prevent any growth; cannot
  add new attributes after initialization
* **Manual immutability enforcement**: Requires discipline, documentation, and
  code review; error-prone and not enforceable at runtime
* **Copy-on-write patterns**: Add performance overhead and memory consumption;
  complexity scales with collection size
* **Read-only wrappers**: Limited to specific collection types; do not support
  selective mutability or initialization phases

These solutions fail to provide the specific combination of:

* Allowing growth (new entries/attributes)
* Preventing modification of existing entries/attributes
* Supporting flexible initialization patterns
* Maintaining familiar Python APIs
* Enabling selective mutability when needed

Goals and Objectives
===============================================================================

Primary Objectives
-------------------------------------------------------------------------------

**REQ-OBJ-001 [Critical]: Accretive Behavior**

Provide data structures that enforce grow-only semantics: new values can be
added, but existing values cannot be modified or removed.

Success Metrics:

* 100% prevention of modification attempts on existing entries
* Clear, informative exceptions when immutability is violated
* Zero false positives (legitimate additions incorrectly rejected)

**REQ-OBJ-002 [Critical]: Familiar APIs**

Maintain APIs consistent with standard Python types (dict, SimpleNamespace,
type, ModuleType) to minimize learning curve.

Success Metrics:

* All standard collection operations supported except mutation
* Initialization patterns match standard library types
* Drop-in replacement possible in most use cases

**REQ-OBJ-003 [High]: Flexible Mutability**

Support selective mutability for specific attributes/entries when needed during
initialization or for specific use cases.

Success Metrics:

* Configuration options for mutable attribute patterns
* Support for unprotected initialization phases
* Compatibility with standard decorators (dataclasses, etc.)

Secondary Objectives
-------------------------------------------------------------------------------

**REQ-OBJ-004 [Medium]: Performance Efficiency**

Minimize performance overhead compared to standard mutable collections.

Success Metrics:

* Lookup operations within 10% of standard dict/object performance
* Addition operations within 20% of standard performance
* Memory overhead less than 15% compared to standard types

**REQ-OBJ-005 [Medium]: Comprehensive Type Coverage**

Provide accretive variants for common Python types beyond basic collections.

Success Metrics:

* Dictionary types with standard, producer, and validator variants
* Namespace types matching SimpleNamespace functionality
* Class metaclasses supporting dataclasses and standard classes
* Module reclassification utilities

Target Users
===============================================================================

User Personas
-------------------------------------------------------------------------------

**Persona 1: Library Author**

* Building reusable libraries with plugin architectures
* Needs guaranteed availability of registered extensions
* Values correctness and predictability over flexibility
* Intermediate to advanced Python knowledge
* Uses type hints and modern Python features

**Persona 2: Application Developer**

* Building configuration systems for production applications
* Needs to prevent accidental configuration overwrites
* Values safety and clear error messages
* Intermediate Python knowledge
* May work in teams with varying skill levels

**Persona 3: System Architect**

* Designing concurrent or distributed systems
* Needs to minimize shared mutable state
* Values architectural patterns and best practices
* Advanced Python knowledge
* Concerned with maintainability and long-term evolution

User Needs and Motivations
-------------------------------------------------------------------------------

* **Safety**: Prevent accidental state mutation that leads to bugs
* **Predictability**: Guarantee that once-set values remain constant
* **Simplicity**: Minimal API surface and familiar patterns
* **Flexibility**: Support legitimate use cases requiring selective mutability
* **Performance**: Acceptable overhead for the safety guarantees provided
* **Debuggability**: Clear error messages identifying violation sources

Technical Proficiency Levels
-------------------------------------------------------------------------------

* **Minimum**: Intermediate Python (understands classes, decorators, type hints)
* **Typical**: Advanced Python (understands metaclasses, descriptors, protocols)
* **Documentation**: Should serve both proficiency levels with clear examples

Usage Contexts
-------------------------------------------------------------------------------

* Plugin registration systems
* Configuration management
* Event handler registries
* Cache implementations
* State management in web frameworks
* Concurrent programming with shared state

Functional Requirements
===============================================================================

Accretive Dictionary Types
-------------------------------------------------------------------------------

**REQ-DICT-001 [Critical]: Basic Dictionary**

Provide a standard accretive dictionary implementation.

As a library author, I want a dictionary that allows adding new entries but
prevents modifying existing ones, so that plugin registrations remain stable.

Acceptance Criteria:

* Supports initialization from iterables and keyword arguments
* Implements collections.abc.Mapping protocol
* Allows ``__setitem__`` for new keys only
* Raises ``EntryImmutability`` exception on modification attempts
* Prevents ``__delitem__`` operations on existing keys
* Supports all read operations (get, keys, values, items, etc.)

**REQ-DICT-002 [High]: Producer Dictionary**

Provide a dictionary that auto-generates values for missing keys.

As an application developer, I want a dictionary with default factories like
defaultdict but with accretive behavior, so that I can accumulate grouped data
safely.

Acceptance Criteria:

* Accepts factory function for generating default values
* Generates value on first access to missing key
* Generated values become immutable after creation
* Behaves identically to Dictionary for existing keys

**REQ-DICT-003 [Medium]: Validator Dictionary**

Provide a dictionary that validates entries before addition.

As a system architect, I want to enforce type or value constraints on
dictionary entries, so that invalid data never enters the registry.

Acceptance Criteria:

* Accepts predicate function for validation
* Calls predicate with (key, value) on each addition attempt
* Raises ``EntryInvalidity`` exception on validation failure
* Allows only valid entries to be added and made immutable

**REQ-DICT-004 [Medium]: Combined Producer-Validator**

Provide a dictionary combining producer and validator behaviors.

Acceptance Criteria:

* Generated default values must pass validation
* Validation failures raise clear exceptions
* Behaves as expected from both parent classes

Accretive Namespace Types
-------------------------------------------------------------------------------

**REQ-NS-001 [Critical]: Basic Namespace**

Provide an accretive namespace similar to types.SimpleNamespace.

As a library author, I want an object where I can add attributes dynamically but
prevent later modification, so that configuration objects remain consistent.

Acceptance Criteria:

* Allows dynamic attribute assignment with dot notation
* Prevents modification of existing attributes
* Prevents deletion of existing attributes
* Raises ``AttributeImmutability`` exception on violations
* Supports initialization from iterables and keyword arguments
* Provides readable ``__repr__`` listing all attributes

Accretive Class Types
-------------------------------------------------------------------------------

**REQ-CLASS-001 [Critical]: Standard Metaclass**

Provide a metaclass for creating classes with accretive instances.

As an application developer, I want to create custom classes whose instances
have accretive behavior, so that I can build domain-specific immutable types.

Acceptance Criteria:

* Works as a metaclass (``metaclass=Class``)
* Instance attributes become immutable after first assignment
* Supports selective mutability via configuration
* Integrates with classcore class factory system
* Supports dynadoc documentation generation

**REQ-CLASS-002 [High]: Dataclass Metaclass**

Provide a metaclass for dataclasses with accretive instances.

As a library author, I want to use @dataclass decorator with accretive behavior,
so that I can leverage dataclass features with immutability guarantees.

Acceptance Criteria:

* Compatible with @dataclass decorator
* Frozen instances by default
* Supports kw_only parameters
* Field values immutable after initialization
* Proper dataclass_transform type checking support

**REQ-CLASS-003 [Medium]: Mutable Dataclass Metaclass**

Provide a metaclass for dataclasses with selectively mutable instances.

Acceptance Criteria:

* Instance attributes can be declared mutable
* Class-level immutability maintained
* Supports standard dataclass features
* Clear documentation of mutability patterns

Accretive Module Types
-------------------------------------------------------------------------------

**REQ-MOD-001 [High]: Module Reclassification**

Provide utilities to reclassify existing modules as accretive.

As a library author, I want to make module-level constants truly constant, so
that module state cannot be tampered with at runtime.

Acceptance Criteria:

* ``Module`` class extends types.ModuleType
* Module attributes become immutable after finalization
* ``finalize_module`` utility for reclassification
* Recursive reclassification for package hierarchies
* Integration with dynadoc for documentation

Error Handling
-------------------------------------------------------------------------------

**REQ-ERR-001 [Critical]: Exception Hierarchy**

Provide clear exception hierarchy for accretive violations.

As an application developer, I want informative exceptions when immutability is
violated, so that I can quickly identify and fix the source of violations.

Acceptance Criteria:

* ``Omnierror`` base class for all package errors
* ``AttributeImmutability`` for attribute violations
* ``EntryImmutability`` for dictionary entry violations
* ``EntryInvalidity`` for validation failures
* Exception messages include attribute/key names and context
* Exceptions inherit from appropriate standard types (TypeError, ValueError)

Non-Functional Requirements
===============================================================================

Performance Requirements
-------------------------------------------------------------------------------

**REQ-PERF-001**: Dictionary lookup operations complete within 10% of standard
dict performance for collections up to 100,000 entries.

**REQ-PERF-002**: Attribute access on accretive objects completes within 15% of
standard object attribute access.

**REQ-PERF-003**: Import time overhead less than 100ms for the entire package.

Compatibility Requirements
-------------------------------------------------------------------------------

**REQ-COMPAT-001**: Support Python 3.10 and above.

**REQ-COMPAT-002**: Compatible with static type checkers (mypy, pyright).

**REQ-COMPAT-003**: Compatible with standard decorators (@dataclass, @property,
etc.).

**REQ-COMPAT-004**: Works correctly with pickling and unpickling.

Usability Requirements
-------------------------------------------------------------------------------

**REQ-USE-001**: API matches standard library conventions where possible.

**REQ-USE-002**: Error messages clearly identify violation source and suggest
fixes.

**REQ-USE-003**: Comprehensive documentation with practical examples.

**REQ-USE-004**: Docstrings for all public APIs generated via dynadoc.

Reliability Requirements
-------------------------------------------------------------------------------

**REQ-REL-001**: 100% test coverage for core functionality.

**REQ-REL-002**: Zero known bugs in immutability enforcement.

**REQ-REL-003**: Comprehensive test suite covering edge cases.

Maintainability Requirements
-------------------------------------------------------------------------------

**REQ-MAINT-001**: Follows project-standard filesystem organization.

**REQ-MAINT-002**: Uses cascading import hub pattern (``__`` subpackage).

**REQ-MAINT-003**: Integrates with classcore for consistent behavior.

**REQ-MAINT-004**: Clear separation between public API and internal implementation.

Constraints and Assumptions
===============================================================================

Technical Constraints
-------------------------------------------------------------------------------

* **Python Immutability Limitations**: True immutability is impossible in
  Python; enforcement is best-effort and can be circumvented by determined users
  with intermediate Python knowledge. The library encourages immutability rather
  than guarantees it.

* **Metaclass Limitations**: Classes can only have one metaclass; users cannot
  combine accretive metaclasses with other custom metaclasses without multiple
  inheritance or creative workarounds.

* **Performance Overhead**: Attribute assignment interception adds overhead
  compared to standard types; acceptable for most use cases but may be
  prohibitive for performance-critical inner loops.

Dependencies
-------------------------------------------------------------------------------

* **classcore**: Core dependency providing class factory system and behavior
  configuration mechanisms.

* **dynadoc**: Documentation generation from type annotations and fragments.

* **absence**: Sentinel values for distinguishing absent vs None parameters.

* **frigid**: Immutable data structures for internal configuration storage.

Assumptions
-------------------------------------------------------------------------------

* Users have intermediate to advanced Python knowledge
* Users understand the limitations of Python immutability enforcement
* Users prioritize correctness and safety over maximum performance
* Users accept minimal performance overhead for immutability guarantees
* Standard library types (dict, object, module) will maintain backward
  compatibility

Out of Scope
===============================================================================

The following features are explicitly excluded from the current product scope:

**Deep Immutability**

Accretive does not enforce immutability of nested values. If a dictionary entry
is itself mutable (e.g., a list), that object can still be modified. Only the
binding between key and value is immutable.

**Cryptographic Guarantees**

The library does not provide cryptographic verification of immutability or
tamper detection. Immutability enforcement is best-effort in Python's dynamic
environment.

**Multi-Process Synchronization**

Accretive does not provide synchronization primitives for multi-process
scenarios. Thread-safety within a single process is supported, but distributed
consistency is out of scope.

**Migration Tools**

Automatic migration from standard types to accretive types is not provided.
Users must manually adopt accretive types in their codebases.

**Performance Optimization Beyond Standard Types**

While performance overhead should be minimal, optimizations to make accretive
types faster than standard types are not a goal.

**Alternative Immutability Models**

Other immutability patterns (copy-on-write, persistent data structures, etc.)
are not provided. The library focuses exclusively on accretive semantics.