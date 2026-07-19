# Test Organization

## Test Module Numbering Scheme

The test suite uses a hierarchical numbering system for clear organization.

### Package-Level Organization

- **test_000_accretive/**: Main test package for the accretive package
  - **test_000_package.py**: Package-level tests (imports, version, metadata)
  - **test_010_base.py**: Base functionality and common test utilities
  - **test_013_dictionaries.py**: Early dictionary-related utilities or base classes
  - **test_100_classes.py**: Tests for accretive classes (Class, Dataclass, Object)
  - **test_110_iclasses.py**: Tests for internal class implementations
  - **test_200_exceptions.py**: Exception hierarchy testing
  - **test_300_namespaces.py**: Namespace class tests
  - **test_400_modules.py**: Module class and finalize_module tests
  - **test_500_dictionaries.py**: Dictionary classes tests

### Numbering Conventions

| Range     | Component                              |
|-----------|----------------------------------------|
| 000-099   | Package infrastructure and shared utilities |
| 100-199   | Class and metaclass functionality      |
| 200-299   | Exception handling and error cases     |
| 300-399   | Namespace implementations              |
| 400-499   | Module implementations                 |
| 500-599   | Dictionary implementations             |

### Test Function Numbering

Within each test module, functions are numbered by component:

- **000-099**: Basic functionality tests for the module
- **100-199, 200-299, etc.**: Each function/class gets its own 100-number block
- **Increments of 10-20**: For closely related test variations within a block
