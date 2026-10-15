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


''' Assert correct function of common names. '''


import pytest

from .__ import (
    PACKAGE_NAME,
    cache_import_module,
)


nomina = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
calculate_attrname = nomina.calculate_attrname

DIGEST_64 = '0123456789abcdef' * 4

POSITIVE_STATIC_NAMES = (
    '_accretive_classes_behaviors_',
    '_accretive_class_mutables_names_',
    '_accretive_class_mutables_predicates_',
    '_accretive_class_mutables_regexes_',
    '_accretive_instances_visibles_names_',
    '_accretive_instances_visibles_predicates_',
    '_accretive_instances_visibles_regexes_',
    '_accretive_classes_dynadoc_configuration_',
    '_accretive_classes_construction_arguments_',
    '_accretive_classes_assigner_core_',
    '_accretive_classes_deleter_core_',
    '_accretive_classes_surveyor_core_',
)

POSITIVE_MANGLED_NAMES = (
    f"_accretive_class_in_progress_{DIGEST_64}",
    f"_accretive_class_behaviors_{DIGEST_64}",
)

NEGATIVE_NAMES = (
    # Foreign prefix.
    '_classcore_class_behaviors_',
    # Unknown level segment.
    '_accretive_lookalike_',
    # Unknown core segment.
    '_accretive_class_lookalike_',
    # Empty core segment.
    '_accretive_class_',
    # Bare prefix.
    '_accretive_',
    # No prefix at all.
    'behaviors',
    # Mangled-only stems without digest.
    '_accretive_class_behaviors_',
    '_accretive_class_in_progress_',
    # Malformed digests.
    f"_accretive_class_in_progress_{DIGEST_64[ : 63 ]}",
    f"{POSITIVE_MANGLED_NAMES[ 0 ]}0",
    f"_accretive_class_in_progress_{'g' * 64}",
    f"_accretive_class_in_progress_{DIGEST_64.upper( )}",
)


def test_100_call_produces_static_stem( ):
    ''' Namer produces expected static stem. '''
    assert (
        '_accretive_class_behaviors_'
        == calculate_attrname( 'class', 'behaviors' ) )


def test_110_exposes_detector( ):
    ''' Namer exposes internal-name detector for classcore seam. '''
    detector = getattr( calculate_attrname, 'is_internal_name', None )
    assert callable( detector )


@pytest.mark.parametrize( 'name', POSITIVE_STATIC_NAMES )
def test_120_detects_static_stems( name ):
    ''' Detector accepts valid static stems. '''
    assert calculate_attrname.is_internal_name( name )


@pytest.mark.parametrize( 'name', POSITIVE_MANGLED_NAMES )
def test_130_detects_mangled_markers( name ):
    ''' Detector accepts valid mangled progress markers. '''
    assert calculate_attrname.is_internal_name( name )


@pytest.mark.parametrize( 'name', NEGATIVE_NAMES )
def test_140_rejects_noninternal_names( name ):
    ''' Detector rejects lookalikes and malformed names. '''
    assert not calculate_attrname.is_internal_name( name )


def test_200_flows_into_explanations( ):
    ''' Accretive internal names surface in classcore explanations. '''
    ccstd = cache_import_module( 'classcore.standard' )
    explain_attribute = getattr( ccstd, 'explain_attribute', None )
    if explain_attribute is None:
        pytest.skip( 'classcore without attribute explanations' )
    classes = cache_import_module( f"{PACKAGE_NAME}.classes" )
    explanation = explain_attribute(
        classes.Class, '_accretive_class_mutables_names_' )
    assert explanation.internal
    explanation = explain_attribute(
        classes.Class, '_accretive_lookalike_' )
    assert not explanation.internal
