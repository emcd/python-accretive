# Accretion Enforcement

## Purpose
To provide cross-cutting accretion enforcement that ensures attributes and entries become immutable after their initial assignment. This is the core behavior shared by all accretive types (dictionaries, namespaces, classes, modules) and is implemented via classcore's class factory system.

## Requirements

### Requirement: Attribute Immutability Enforcement
The system SHALL enforce that attributes become immutable after their first assignment on accretive objects.

Priority: Critical

#### Scenario: First assignment succeeds
- **WHEN** an attribute is assigned for the first time on an accretive object
- **THEN** the assignment succeeds and the value is stored

#### Scenario: Reassignment raises error
- **WHEN** an attribute is reassigned on an accretive object
- **THEN** an `AttributeImmutability` exception is raised
- **AND** the original value remains unchanged

#### Scenario: Deletion raises error
- **WHEN** deletion of an existing attribute is attempted on an accretive object
- **THEN** an `AttributeImmutability` exception is raised
- **AND** the attribute remains unchanged

### Requirement: Entry Immutability Enforcement
The system SHALL enforce that dictionary entries become immutable after their first assignment.

Priority: Critical

#### Scenario: New entry addition
- **WHEN** a new key-value pair is added to an accretive dictionary
- **THEN** the entry is successfully stored

#### Scenario: Existing entry modification
- **WHEN** modification of an existing entry is attempted
- **THEN** an `EntryImmutability` exception is raised
- **AND** the original entry remains unchanged

#### Scenario: Existing entry deletion
- **WHEN** deletion of an existing entry is attempted
- **THEN** an `EntryImmutability` exception is raised
- **AND** the entry remains unchanged

### Requirement: Initialization Window
The system SHALL allow unrestricted attribute assignment during object initialization, enabling compatibility with `__init__` methods and class decorators like `@dataclass`.

Priority: Critical

#### Scenario: Init-time assignment
- **WHEN** attributes are assigned within `__init__` or similar initialization context
- **THEN** assignments succeed regardless of accretive behavior

#### Scenario: Post-init immutability
- **WHEN** initialization is complete and an attribute is reassigned
- **THEN** accretive behavior is enforced

### Requirement: Mutable Exclusions by Name
The system SHALL allow specific attributes to be declared mutable by name, enabling selective modification while maintaining immutability for all other attributes.

Priority: High

#### Scenario: Named mutable attribute
- **WHEN** an attribute name is listed in the mutables names exclusion set
- **THEN** that attribute can be reassigned at any time
- **AND** other attributes remain immutable

#### Scenario: Wildcard mutables
- **WHEN** the mutables names exclusion is set to `'*'`
- **THEN** all attributes are mutable

### Requirement: Mutable Exclusions by Predicate
The system SHALL allow attributes to be declared mutable based on predicate functions.

Priority: Medium

#### Scenario: Predicate match
- **WHEN** an attribute name matches a mutable predicate function
- **THEN** that attribute can be reassigned
- **AND** non-matching attributes remain immutable

### Requirement: Mutable Exclusions by Regex
The system SHALL allow attributes to be declared mutable based on regular expression patterns.

Priority: Medium

#### Scenario: Regex match
- **WHEN** an attribute name fully matches a mutable regex pattern
- **THEN** that attribute can be reassigned
- **AND** non-matching attributes remain immutable

### Requirement: classcore Integration
The system SHALL delegate accretion enforcement to classcore's class factory system, ensuring consistent behavior configuration across all accretive types.

Priority: Critical

#### Scenario: Metaclass-based enforcement
- **WHEN** a class uses an accretive metaclass
- **THEN** the metaclass intercepts `__setattr__` and `__delattr__` via classcore's assigner system
- **AND** enforcement logic is consistent across all accretive types
