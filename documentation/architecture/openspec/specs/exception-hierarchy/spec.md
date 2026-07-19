# Exception Hierarchy

## Purpose
To provide a clear and comprehensive exception hierarchy for handling violations of accretive constraints (immutability, validity). Exceptions use multiple inheritance to support both package-specific and standard exception handling patterns.

## Requirements

### Requirement: Common Exception Base
The system SHALL provide an `Omniexception` base class that serves as the root of the package exception hierarchy, enabling catch-all exception handling.

Priority: Critical

#### Scenario: Catching all errors
- **WHEN** a user catches `Omnierror` (the base operational error class)
- **THEN** all exceptions raised by the package are caught

### Requirement: Attribute Immutability Exception
The system SHALL provide an `AttributeImmutability` exception that inherits from both `Omnierror` and standard library `AttributeError` and `TypeError`.

Priority: Critical

#### Scenario: Catching attribute violations
- **WHEN** a user catches `AttributeImmutability`
- **THEN** violations of attribute immutability are caught
- **AND** the exception is also caught by `AttributeError` and `TypeError` handlers

### Requirement: Entry Immutability Exception
The system SHALL provide an `EntryImmutability` exception for violations of dictionary entry immutability.

Priority: Critical

#### Scenario: Catching entry violations
- **WHEN** a user catches `EntryImmutability`
- **THEN** violations of dictionary entry immutability are caught

### Requirement: Entry Invalidity Exception
The system SHALL provide an `EntryInvalidity` exception for validation failures in validator dictionaries.

Priority: High

#### Scenario: Catching validation failures
- **WHEN** a user catches `EntryInvalidity`
- **THEN** validation failures in Validator Dictionaries are caught

### Requirement: Dual Inheritance Pattern
The system SHALL use multiple inheritance for exceptions, inheriting from both the package base (`Omnierror`) and appropriate standard library exceptions, enabling both specific and general exception handling.

Priority: Critical

#### Scenario: Package-specific handling
- **WHEN** a user catches `Omnierror`
- **THEN** all package exceptions are caught

#### Scenario: Standard library compatibility
- **WHEN** a user catches a standard library exception (e.g., `AttributeError`)
- **THEN** accretive exceptions that inherit from it are also caught
