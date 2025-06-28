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


''' Assert correct function of exceptions module. '''


import pytest

from . import PACKAGE_NAME, cache_import_module


CLASS_NAMES = (
    'Omniexception', 'Omnierror',
    'AttributeImmutability',
    'EntryImmutability',
    'EntryInvalidity',
    'ErrorProvideFailure',
)
MODULE_QNAME = f"{PACKAGE_NAME}.exceptions"


@pytest.mark.parametrize( 'class_name', CLASS_NAMES )
def test_000_class_exists( class_name ):
    ''' Class exists in module. '''
    module = cache_import_module( MODULE_QNAME )
    assert hasattr( module, class_name )
    class_ = getattr( module, class_name )
    assert issubclass( class_, BaseException )


@pytest.mark.parametrize( 'class_name', CLASS_NAMES )
def test_001_omniexception_subclass( class_name ):
    ''' Class is subclass of family root. '''
    module = cache_import_module( MODULE_QNAME )
    omniclass = module.Omniexception
    class_ = getattr( module, class_name )
    assert issubclass( class_, omniclass )


def test_200_error_provide_failure():
    ''' ErrorProvideFailure formats message correctly. '''
    module = cache_import_module( MODULE_QNAME )
    exc = module.ErrorProvideFailure( 'TestError', reason = 'Testing' )
    message = str( exc )
    assert 'TestError' in message
    assert 'Testing' in message
    assert 'Could not provide error class' in message
