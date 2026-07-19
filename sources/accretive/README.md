# Accretive Architecture

Accretive provides a family of data structures that enforce a grow-only
constraint: values can be added but never modified or removed once set. This
library addresses the need for collections that accumulate state with
immutability guarantees, useful for configuration registries, plugin systems,
and scenarios requiring sticky state.

## Core Architectural Concept

The library implements accretion through attribute assignment interception at
the metaclass level. When an assignment is attempted, the system checks whether
the attribute already exists and whether it is marked as mutable. If the
attribute exists and is not mutable, an exception is raised.

## Major Components

The architecture is organized into four primary component categories:

### Accretive Dictionaries

Mapping-based collections that prevent modification of existing entries:

- **AbstractDictionary**: Base class defining the accretive dictionary
  interface. Implements `collections.abc.Mapping` with custom `__setitem__`
  to enforce immutability of existing entries.
- **Dictionary**: Standard accretive dictionary implementation. Supports
  initialization from multiple iterables and keyword arguments.
- **ProducerDictionary**: Auto-generates values for missing keys via factory
  function. Similar to `collections.defaultdict` with accretive behavior.
- **ValidatorDictionary**: Validates entries before addition using predicate
  function. Invalid entries are rejected rather than added.
- **ProducerValidatorDictionary**: Combines producer and validator behaviors.
  Generated values must pass validation before being stored.

### Accretive Namespaces

Attribute-based containers modeled after `types.SimpleNamespace`:

- **Namespace**: Allows dynamic attribute addition with immutability after
  assignment. Uses custom metaclass to intercept attribute assignment via
  `__setattr__` and `__delattr__`.

### Accretive Classes

Metaclasses and decorators for creating user-defined accretive types:

- **Class**: Standard metaclass for classes with accretive instances.
- **Dataclass**: Metaclass for dataclasses with immutable instances.
- **DataclassMutable**: Metaclass for dataclasses with mutable instance
  attributes but immutable class-level behavior.
- **Object**: Concrete class providing standard accretive behavior via
  composition rather than metaclass.

These leverage the `classcore` library's class factory system to provide
consistent behavior configuration across all class types.

### Accretive Modules

Runtime module reclassification for enforcing module-level immutability:

- **Module**: Accretive variant of `types.ModuleType`.
- **finalize_module**: Utility to reclassify existing modules as accretive,
  optionally processing entire package hierarchies recursively.

## Component Relationships

### Architecture Layers

The system is organized in layers of abstraction:

```text
┌─────────────────────────────────────────────────────────┐
│  Public API Layer                                       │
│  (dictionaries, namespaces, classes, modules)           │
└─────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Behavior Implementation Layer (iclasses)               │
│  (assign_attribute_if_absent_mutable)                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Foundation Layer (classcore)                           │
│  (class_factory, assigner system)                       │
└─────────────────────────────────────────────────────────┘
```

### External Dependencies

- **classcore**: Provides the class factory system and behavior configuration
  mechanisms. The `class_factory` function creates metaclasses with
  configurable attribute assignment interceptors.
- **dynadoc**: Automatic docstring generation from type annotations and
  documentation fragments.
- **absence**: Sentinel value for optional parameters, distinguishing between
  `None` and truly absent values.
- **frigid**: Immutable data structures used internally for storing
  configuration and metadata.

## Key Architectural Patterns

### Metaclass-Based Interception

All accretive behavior is implemented via metaclass `__setattr__` and
`__delattr__` hooks that delegate to the `assigner_core` function. This
allows consistent behavior across all accretive types while maintaining
compatibility with standard Python semantics.

### Assignment Core Strategy

The `assign_attribute_if_absent_mutable` function implements the core logic:

1. Check if attribute exists using `hasattr`
2. If absent, allow assignment
3. If present, check immutability behaviors configuration
4. Check mutables exclusions (names, predicates, regexes)
5. If not mutable, raise `AttributeImmutability` exception
6. Otherwise, allow assignment

### Cascading Import Hub Pattern

The `__` subpackage centralizes all external imports, providing consistent
namespace management and reducing import duplication. All modules use
`from . import __` to access common dependencies.

## Data Flow

### Entry Addition Flow (Dictionaries)

1. User calls `dict[key] = value` or `dict.update(...)`
2. `__setitem__` checks if key exists
3. If key exists, raises `EntryImmutability` exception
4. If key absent, calls `_pre_setitem_` for validation
5. Calls `_store_item_` to persist entry
6. Entry becomes immutable

### Attribute Assignment Flow (Namespaces, Classes, Modules)

1. User assigns `obj.attr = value` or `del obj.attr`
2. Metaclass intercepts via `__setattr__` or `__delattr__`
3. Delegates to `assign_attribute_if_absent_mutable`
4. Function checks existence and mutability status
5. If immutable and exists, raises `AttributeImmutability` exception
6. Otherwise completes assignment/deletion

## Performance Considerations

- **Import Centralization**: The `__` pattern front-loads import costs to
  package initialization time rather than individual module import time.
- **Attribute Lookup**: Immutability checks require metadata lookups
  (behaviors, mutables predicates) on each assignment attempt. Cached lookups
  minimize this overhead.
- **Dictionary Storage**: Uses standard `dict` internally for O(1) lookups.

## Error Handling Strategy

The package defines a clear exception hierarchy rooted in `Omniexception`:

- **Omnierror**: Base for all operational errors
- **AttributeImmutability**: Raised when attempting to modify immutable
  attributes (inherits from `AttributeError` and `TypeError`)
- **EntryImmutability**: Raised when attempting to modify dictionary entries
- **EntryInvalidity**: Raised when validation fails in validator dictionaries
- **ErrorProvideFailure**: Raised when error class lookup fails

This design allows both specific exception handling (catch
`AttributeImmutability`) and general handling (catch `Omnierror`).

## Project Structure

```text
python-accretive/
├── LICENSE.txt              # Project license
├── README.rst               # Project overview and quick start
├── pyproject.toml           # Python packaging and tool configuration
├── documentation/           # Sphinx documentation source
├── sources/                 # All source code
├── tests/                   # Test suites
└── .auxiliary/              # Development workspace
```

### Package Layout

```text
sources/
└── accretive/                   # Main Python package
    ├── __/                      # Centralized import hub
    │   ├── __init__.py          # Re-exports core utilities
    │   ├── dictionaries.py      # Internal dictionary utilities and type aliases
    │   ├── doctab.py            # Documentation fragment table
    │   ├── exceptions.py        # Internal exception utilities
    │   ├── imports.py           # External library imports
    │   └── nomina.py            # Package-specific naming constants
    ├── __init__.py              # Package entry point
    ├── py.typed                 # Type checking marker
    ├── classes.py               # Accretive class metaclasses and decorators
    ├── dictionaries.py          # Accretive dictionary implementations
    ├── exceptions.py            # Package exception hierarchy
    ├── iclasses.py              # Internal class implementations
    ├── modules.py               # Accretive module implementation
    └── namespaces.py            # Accretive namespace implementation
```

All package modules use the `__` import hub pattern for consistent
namespace management and reduced import duplication.

## Design Rationale

### Why Accretive (Grow-Only) Semantics?

The library implements accretive (grow-only) semantics rather than other
immutability patterns:

| Pattern | Trade-off |
|---------|-----------|
| **Fully immutable** | No growth after initialization (frozen dataclasses, tuples) |
| **Copy-on-write** | Performance overhead, memory consumption |
| **Persistent data structures** | Complexity, unfamiliar APIs |
| **Accretive (grow-only)** | Middle ground — values accumulate but never change |

Accretive semantics are useful for registries, plugin systems, caches, and
configuration objects where state must accumulate reliably but never be
modified or removed once set. This provides clear use case differentiation
from fully immutable libraries like `frigid`.

### Why Metaclass-Based Interception?

Alternatives considered:

- **Descriptors**: Only work for class-level attributes, not instance attributes
- **Direct `__setattr__` override**: Doesn't integrate well with class factory pattern
- **Proxies**: Add indirection and complicate type checking

Metaclass interception via `__setattr__` and `__delattr__` hooks provides
consistent behavior across all accretive types while maintaining compatibility
with standard Python semantics and classcore's class factory system.

### Why classcore Integration?

Building on classcore's `class_factory` and behavior configuration system
rather than implementing from scratch provides:

- Consistent configuration API across all types (Class, Dataclass, Module, etc.)
- Reuse of well-tested behavior management code
- Integration with dynadoc and behavior exclusions (mutables predicates/regexes)

### Why Multiple Inheritance for Exceptions?

Exceptions inherit from both the package base (`Omnierror`) and appropriate
standard library exceptions (`AttributeError`, `TypeError`, `ValueError`).
This enables both specific handling (`catch AttributeImmutability`) and
general handling (`catch Omnierror`) while remaining compatible with
standard exception hierarchies.
