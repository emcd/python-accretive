# Accretive Dictionaries

## Purpose
To provide dictionary implementations that enforce grow-only semantics, where new entries can be added but existing entries cannot be modified or removed. This ensures data consistency for configuration registries, plugin systems, and other use cases requiring sticky state.

## Requirements

### Requirement: Basic Dictionary
The system SHALL provide a standard accretive dictionary implementation that allows adding new entries but prevents modifying or removing existing ones.

Priority: Critical

#### Scenario: Adding new entries
- **WHEN** a user adds a new key-value pair to the dictionary
- **THEN** the entry is successfully added
- **AND** the value can be retrieved using the key

#### Scenario: Modifying existing entries
- **WHEN** a user attempts to update the value of an existing key
- **THEN** an `EntryImmutability` exception is raised
- **AND** the original value remains unchanged

#### Scenario: Removing entries
- **WHEN** a user attempts to delete an existing key
- **THEN** an exception (likely `TypeError` or `EntryImmutability`) is raised
- **AND** the entry remains in the dictionary

### Requirement: Producer Dictionary
The system SHALL provide a dictionary that auto-generates values for missing keys using a factory function, similar to `collections.defaultdict` but with accretive behavior.

Priority: High

#### Scenario: Accessing missing keys
- **WHEN** a user accesses a missing key
- **THEN** a new value is generated using the factory function
- **AND** the new value is stored in the dictionary associated with the key
- **AND** the value is returned to the user

#### Scenario: Immutability of generated values
- **WHEN** a value has been generated for a key
- **THEN** subsequent attempts to modify that key raise `EntryImmutability`

### Requirement: Validator Dictionary
The system SHALL provide a dictionary that validates entries before addition using a predicate function, ensuring only valid data can be added.

Priority: Medium

#### Scenario: Adding valid entries
- **WHEN** a user adds a key-value pair that passes the predicate function
- **THEN** the entry is successfully added

#### Scenario: Adding invalid entries
- **WHEN** a user adds a key-value pair that fails the predicate function
- **THEN** an `EntryInvalidity` exception is raised
- **AND** the entry is not added to the dictionary

### Requirement: Combined Producer-Validator
The system SHALL provide a dictionary combining auto-generation and validation behaviors.

Priority: Medium

#### Scenario: Generating valid values
- **WHEN** a missing key is accessed and the factory generates a value that passes validation
- **THEN** the value is stored and returned

#### Scenario: Generating invalid values
- **WHEN** a missing key is accessed and the factory generates a value that fails validation
- **THEN** an `EntryInvalidity` exception is raised
