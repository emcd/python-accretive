# Accretive Classes

## Purpose
To provide metaclasses and decorators for creating user-defined accretive types. Includes metaclasses for standard classes, dataclasses, abstract base classes, and protocols — all enforcing attribute immutability after initialization.

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

### Requirement: Abstract Base Class Metaclass
The system SHALL provide a metaclass for abstract base classes with accretive instances, compatible with `abc.ABCMeta`.

Priority: Medium

#### Scenario: Defining an accretive abstract class
- **WHEN** a class inherits from `ABC` or uses `ABCMeta` with the accretive abstract metaclass
- **THEN** the class supports abstract methods
- **AND** concrete instances exhibit accretive behavior

### Requirement: Protocol Metaclass
The system SHALL provide metaclasses for protocol classes with accretive behavior, compatible with `typing.Protocol`.

Priority: Medium

#### Scenario: Defining an accretive protocol
- **WHEN** a class inherits from `Protocol` with an accretive protocol metaclass
- **THEN** the class behaves as a protocol
- **AND** instances exhibit accretive behavior

### Requirement: Base Classes
The system SHALL provide ready-to-use base classes: `Object`, `ObjectMutable`, `DataclassObject`, `DataclassObjectMutable`, `Protocol`, `ProtocolMutable`, `DataclassProtocol`, and `DataclassProtocolMutable`.

Priority: High

#### Scenario: Using Object base class
- **WHEN** a class inherits from `Object`
- **THEN** instances have immutable attributes after initialization

#### Scenario: Using ObjectMutable base class
- **WHEN** a class inherits from `ObjectMutable`
- **THEN** instance attributes are mutable

#### Scenario: Using DataclassObject base class
- **WHEN** a class inherits from `DataclassObject`
- **THEN** the class behaves as a dataclass with immutable instances

### Requirement: Class Decorator
The system SHALL provide a `with_standard_behaviors` decorator that adds accretive behavior to any class without requiring metaclass configuration.

Priority: High

#### Scenario: Decorating a class
- **WHEN** a class is decorated with `@with_standard_behaviors`
- **THEN** instances of that class exhibit accretive behavior
- **AND** the class retains its original metaclass

#### Scenario: Decorating with mutable attributes
- **WHEN** `@with_standard_behaviors(mutables=...)` specifies mutable attributes
- **THEN** those attributes remain mutable
- **AND** other attributes remain immutable

### Requirement: Dataclass Decorator
The system SHALL provide a `dataclass_with_standard_behaviors` decorator that adds accretive behavior to dataclasses.

Priority: High

#### Scenario: Decorating a dataclass
- **WHEN** a dataclass is decorated with `@dataclass_with_standard_behaviors`
- **THEN** instances have immutable fields after initialization

### Requirement: ABC Internals Exemption
The system SHALL exempt abstract base class internals (`_abc_cache`, `_abc_negative_cache`, `_abc_negative_cache_version`, `_abc_registry`) from immutability enforcement on protocol classes.

Priority: Medium

#### Scenario: ABC cache mutation
- **WHEN** Python's ABC machinery modifies `_abc_cache` on a protocol class
- **THEN** the modification succeeds without raising `AttributeImmutability`

### Requirement: Attribute Concealment
The system SHALL delegate attribute concealment (filtering from `dir()`) to classcore's class factory system.

Priority: Low

#### Scenario: Concealed attributes
- **WHEN** a class uses an accretive metaclass with concealment configured
- **THEN** concealed attributes are not visible in `dir()` output
- **AND** concealment is managed by classcore's behavior system
