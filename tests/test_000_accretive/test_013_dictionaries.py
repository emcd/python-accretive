# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Assert correct function of internal dictionary types. '''


import pytest

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__.dictionaries"
EXCEPTIONS_QNAME = f"{PACKAGE_NAME}.__.exceptions"
THESE_CLASSES_NAMES = ( 'AccretiveDictionary', )


def test_100_instantiation( ):
    ''' Validates instantiation of AccretiveDictionary.

        Ensures the class can be instantiated with positional and nominative
        arguments.
    '''
    module = cache_import_module( MODULE_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )
    assert isinstance( dictionary, factory )
    assert dictionary[ 'key1' ] == 1
    assert dictionary[ 'key2' ] == 2


def test_101_accretion( ):
    ''' Validates accretion behavior of AccretiveDictionary.

        Ensures new entries can be added, but existing entries cannot be
        modified or removed.
    '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( EXCEPTIONS_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )

    # Add new entry
    dictionary[ 'new_key' ] = 3
    assert dictionary[ 'new_key' ] == 3

    # Attempt to modify existing entry
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary[ 'key1' ] = 999
    assert dictionary[ 'key1' ] == 1

    # Attempt to delete existing entry
    with pytest.raises( exceptions.EntryImmutability ):
        del dictionary[ 'key1' ]
    assert dictionary[ 'key1' ] == 1


def test_102_update_behavior( ):
    ''' Validates update behavior of AccretiveDictionary.

        Ensures update adds new entries but raises EntryImmutability for
        existing entries.
    '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( EXCEPTIONS_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )

    # Update with new entries
    dictionary.update( [ ( 'new_key1', 4 ), ( 'new_key2', 5 ) ] )
    assert dictionary[ 'new_key1' ] == 4
    assert dictionary[ 'new_key2' ] == 5

    # Update with existing entry (positional)
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary.update( [ ( 'key1', 999 ) ] )
    assert dictionary[ 'key1' ] == 1

    # Update with existing entry (keyword)
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary.update( key1 = 999 )
    assert dictionary[ 'key1' ] == 1


def test_103_invalid_operations( ):
    ''' Validates invalid operations on AccretiveDictionary.

        Ensures clear, pop, and popitem raise OperationInvalidity.
    '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( EXCEPTIONS_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )

    # Test clear
    with pytest.raises( exceptions.OperationInvalidity, match = "'clear'" ):
        dictionary.clear( )

    # Test pop
    with pytest.raises( exceptions.OperationInvalidity, match = "'pop'" ):
        dictionary.pop( 'key1' )
    with pytest.raises( exceptions.OperationInvalidity, match = "'pop'" ):
        dictionary.pop( 'key1', 0 )

    # Test popitem
    with pytest.raises( exceptions.OperationInvalidity, match = "'popitem'" ):
        dictionary.popitem( )


def test_104_copy_behavior( ):
    ''' Validates copy behavior of AccretiveDictionary.

        Ensures copy creates a fresh, independent instance with the same data.
    '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( EXCEPTIONS_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )
    dictionary[ 'new_key' ] = 3

    copied = dictionary.copy( )
    assert isinstance( copied, factory )
    assert copied == dictionary
    assert copied is not dictionary

    # Modify copy (should work for new entries, not existing ones)
    copied[ 'new_key2' ] = 4
    assert copied[ 'new_key2' ] == 4
    assert 'new_key2' not in dictionary

    # Ensure original remains immutable for existing entries
    with pytest.raises( exceptions.EntryImmutability ):
        dictionary[ 'key1' ] = 999
    assert dictionary[ 'key1' ] == 1


def test_105_invalid_inputs( ):
    ''' Validates behavior with invalid inputs to AccretiveDictionary.

        Ensures update raises TypeError for non-iterable or non-mapping inputs.
    '''
    module = cache_import_module( MODULE_QNAME )
    factory = getattr( module, 'AccretiveDictionary' )
    dictionary = factory( key1 = 1, key2 = 2 )

    with pytest.raises( TypeError ):
        dictionary.update( 42 )  # Non-iterable input

    with pytest.raises( TypeError ):
        dictionary.update( None )  # Non-iterable input

    with pytest.raises( TypeError ):
        dictionary.update( [ 1, 2, 3 ] )  # Invalid iterable structure
