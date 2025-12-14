# Accretive Classes

## Purpose
To provide metaclasses that enforce accretive behavior on class instances, ensuring that instance attributes become immutable after their initial assignment. This supports creating robust objects where state accumulation is permitted but state mutation is forbidden.

## Requirements

### Requirement: Standard Metaclass
The system SHALL provide a metaclass for creating classes with accretive instances where instance attributes become immutable after first assignment.

Priority: Critical

#### Scenario: Defining an accretive class
- **WHEN** a class is defined with `metaclass=Class` (the accretive metaclass)
- **THEN** instances of that class exhibit accretive behavior

#### Scenario: Assigning attributes
- **WHEN** an attribute is assigned for the first time on an instance
- **THEN** the assignment succeeds

#### Scenario: Reassigning attributes
- **WHEN** an attribute is reassigned on an instance
- **THEN** an `AttributeImmutability` exception is raised

### Requirement: Dataclass Metaclass
The system SHALL provide a metaclass for dataclasses with accretive instances, compatible with the `@dataclass` decorator.

Priority: High

#### Scenario: Defining an accretive dataclass
- **WHEN** a class is decorated with `@dataclass` and uses the accretive dataclass metaclass
- **THEN** the class behaves as a dataclass
- **AND** instances exhibit accretive behavior (fields are immutable after initialization)

### Requirement: Mutable Dataclass Metaclass
The system SHALL provide a metaclass for dataclasses that supports selective mutability for specific attributes.

Priority: Medium

#### Scenario: Selective mutability
- **WHEN** a class is defined with specific attributes marked as mutable
- **THEN** those attributes can be reassigned
- **AND** other attributes remain immutable
