# Accretive Namespaces

## Purpose
To provide a namespace implementation similar to `types.SimpleNamespace` that allows adding attributes dynamically but prevents modification or deletion of existing attributes, suitable for configuration objects and structured data carriers.

## Requirements

### Requirement: Basic Namespace
The system SHALL provide an accretive namespace that allows adding attributes dynamically but prevents modification or deletion of existing attributes.

Priority: Critical

#### Scenario: Adding new attributes
- **WHEN** a user assigns a value to a new attribute
- **THEN** the attribute is added to the namespace
- **AND** the value can be accessed via dot notation

#### Scenario: Modifying existing attributes
- **WHEN** a user attempts to reassign an existing attribute
- **THEN** an `AttributeImmutability` exception is raised
- **AND** the original value remains unchanged

#### Scenario: Deleting attributes
- **WHEN** a user attempts to delete an existing attribute
- **THEN** an exception is raised
- **AND** the attribute remains in the namespace
