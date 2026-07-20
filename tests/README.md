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

## Test Standards

These standards are shared with sister projects (frigid, classcore) for
cross-project alignment.

### Exception Message Verification

All exception classes should have tests verifying their message content.

```python
def test_NNN_exception_message_FORMAT():
    ''' Exception message includes expected context. '''
    with raises( ExceptionClass ) as exc_info:
        raise ExceptionClass( *args )
    assert 'expected_text' in str( exc_info.value )
```

Required tests:

- **AttributeImmutability**: message includes attribute name and target
- **EntryImmutability**: message includes entry key
- **EntryInvalidity**: message includes entry key and value
- **ErrorProvideFailure**: message includes error name and reason

### Pickle/Copy Round-Trip Tests

All public data structures should survive pickle and copy round-trips.

```python
def test_NNN_pickle_roundtrip():
    ''' Object survives pickle round-trip. '''
    import pickle
    original = Constructor( *args )
    restored = pickle.loads( pickle.dumps( original ) )
    assert original == restored
    # Verify immutability preserved
    with raises( ExceptionClass ):
        restored[ 'new_key' ] = 'value'

def test_NNN_copy_roundtrip():
    ''' Object survives copy round-trip. '''
    import copy
    original = Constructor( *args )
    copied = copy.copy( original )
    assert original == copied
    assert original is not copied
```

Required tests:

- **Dictionary variants**: pickle, copy, deepcopy
- **Namespace**: pickle, copy, deepcopy
- **Accretive objects**: pickle, copy

### Protocol Metaclass Tests

Protocol metaclasses should be tested for both protocol behavior and
immutability enforcement.

```python
def test_NNN_protocol_metaclass():
    ''' Protocol metaclass enforces immutability. '''
    class MyProtocol( Protocol, metaclass=ProtocolClass ):
        def my_method( self ) -> None: ...

    assert MyProtocol._is_protocol
    MyProtocol.attr = 1
    with raises( AttributeImmutability ):
        MyProtocol.attr = 2
```

Required tests:

- **ProtocolClass**: basic protocol + immutability
- **ProtocolDataclass**: dataclass protocol + immutability
- **ProtocolDataclassMutable**: dataclass protocol + mutability
- **AbstractBaseClass**: abstract methods + immutability

### Decorator Application Tests

Decorator functions should be tested for both direct application and
factory usage.

```python
def test_NNN_decorator_direct():
    ''' Decorator applied directly to class. '''
    @with_standard_behaviors
    class MyClass:
        def __init__( self ):
            self.attr = 'value'

    obj = MyClass()
    assert obj.attr == 'value'
    with raises( AttributeImmutability ):
        obj.attr = 'other'

def test_NNN_decorator_factory():
    ''' Decorator used as factory with arguments. '''
    @with_standard_behaviors( mutables=( 'mutable_attr', ) )
    class MyClass:
        def __init__( self ):
            self.immutable = 'fixed'
            self.mutable = 'changeable'

    obj = MyClass()
    obj.mutable = 'changed'  # Succeeds
    with raises( AttributeImmutability ):
        obj.immutable = 'other'  # Fails
```

Required tests:

- **with_standard_behaviors**: direct application, factory, mutables
- **dataclass_with_standard_behaviors**: direct application, factory, mutables
