# Accretive Exceptions

## Purpose
To provide a clear and comprehensive exception hierarchy for handling violations of accretive constraints (immutability, validity).

## Requirements

### Requirement: Exception Hierarchy
The system SHALL provide a clear exception hierarchy for accretive violations, rooted in a common base class.

Priority: Critical

#### Scenario: Catching all errors
- **WHEN** a user catches `Omnierror`
- **THEN** all exceptions raised by the package are caught

#### Scenario: Catching immutability errors
- **WHEN** a user catches `AttributeImmutability` or `EntryImmutability`
- **THEN** violations of attribute or dictionary entry immutability are caught

#### Scenario: Catching validation errors
- **WHEN** a user catches `EntryInvalidity`
- **THEN** validation failures in Validator Dictionaries are caught
