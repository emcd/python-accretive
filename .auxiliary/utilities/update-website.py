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


''' Update website for publication. '''

# mypy: ignore-errors


def main( version: str ):
    ''' Runs website updater. '''
    from shutil import copytree, rmtree
    from tarfile import open as tarfile_open
    paths = _discover_paths( )
    _ensure_paths( paths )
    if paths.website.is_dir( ): rmtree( paths.website )
    if paths.archive.is_file( ):
        with tarfile_open( paths.archive, 'r:xz' ) as archive:
            archive.extractall( path = paths.website )
    available_species = [ ]
    # Create/update destination if origin exists.
    for species in ( 'coverage-pytest', 'sphinx-html' ):
        origin_path = paths.artifacts / species
        if not origin_path.is_dir( ): continue
        destination_path = paths.website / version / species
        if destination_path.is_dir( ): rmtree( destination_path )
        copytree( origin_path, destination_path )
        available_species.append( species )
    index_data = _update_versions_json( paths, version, available_species )
    _update_index_html( paths, index_data )
    ( paths.website / '.nojekyll' ).touch( )
    with tarfile_open( paths.archive, 'w:xz' ) as archive:
        archive.add( paths.website )


def _discover_paths( ):
    from pathlib import Path
    from types import SimpleNamespace
    paths = SimpleNamespace( )
    paths.project = Path( ) # TODO: Discover.
    paths.auxiliary = paths.project / '.auxiliary'
    paths.publications = paths.auxiliary / 'publications'
    paths.archive = paths.publications / 'website.tar.xz'
    paths.template = Path( __file__ ).parent / 'website.html.mako'
    paths.artifacts = paths.auxiliary / 'artifacts'
    paths.website = paths.artifacts / 'website'
    paths.index = paths.website / 'index.html'
    paths.versions = paths.website / 'versions.json'
    return paths


def _ensure_paths( paths ):
    paths.publications.mkdir( exist_ok = True, parents = True )
    paths.website.mkdir( exist_ok = True, parents = True )


def _update_index_html( paths, data ):
    from mako.template import Template
    template = Template( # nosec use_of_mako_templates
        filename = str( paths.template ) )
    with paths.index.open( 'w' ) as file:
        file.write( template.render( **data ) )


def _update_versions_json( paths, version, species ):
    from json import dump as json_dump, load as json_load
    from packaging.version import Version
    if not paths.versions.is_file( ):
        data = { 'versions': { } }
        with paths.versions.open( 'w' ) as file:
            json_dump( data, file, indent = 4 )
    with paths.versions.open( 'r+' ) as file:
        data = json_load( file )
        versions = data[ 'versions' ]
        versions[ version ] = species
        versions = dict( sorted(
            versions.items( ),
            key = lambda entry: Version( entry[ 0 ] ),
            reverse = True ) )
        data[ 'latest_version' ] = next( iter( versions ) )
        data[ 'versions' ] = versions
        file.seek( 0 )
        json_dump( data, file, indent = 4 )
        file.truncate( )
    return data


if '__main__' == __name__:
    from typer import run
    run( main )
