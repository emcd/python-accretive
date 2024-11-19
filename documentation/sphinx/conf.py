''' Configuration file for the Sphinx documentation builder.

    This file only contains a selection of the most common options.
    For a full list, see the documentation:
        https://www.sphinx-doc.org/en/master/usage/configuration.html
    Also, see this nice article on Sphinx customization:
        https://jareddillard.com/blog/common-ways-to-customize-sphinx-themes.html
'''

# mypy: ignore-errors
# pylint: disable=consider-using-namedtuple-or-dataclass
# ruff: noqa: E402,F401


def _prepare( ):
    from pathlib import Path
    from sys import path as module_discovery_locations
    from tomli import load  # TODO: Python 3.11: tomllib
    project_location = Path( __file__ ).parent.parent.parent
    pyproject_location = project_location / 'pyproject.toml'
    module_discovery_locations.insert( 0, str( project_location / 'sources' ) )
    with pyproject_location.open( 'rb' ) as project_file:
        return load( project_file )


def _calculate_copyright_notice( information, copyright_holder ):
    from datetime import datetime as DateTime
    first_year = information[ 'tool' ][ 'SELF' ][ 'year-of-origin' ]
    now_year = DateTime.utcnow( ).year
    if first_year < now_year: year_range = f"{first_year}-{now_year}"
    else: year_range = str( first_year )
    return f"{year_range}, {copyright_holder}"


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

_information = _prepare( )

project = _information[ 'project' ][ 'name' ]
author = _information[ 'project' ][ 'authors' ][ 0 ][ 'name' ]
copyright = ( # pylint: disable=redefined-builtin
    _calculate_copyright_notice( _information, author ) )
from accretive import __version__ as release, __version__ as version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
    'sphinx_inline_tabs',
]

templates_path = [ '_templates' ]

exclude_patterns = [ ]

rst_prolog = f'''
.. |project| replace:: {project}
'''

nitpicky = True
nitpick_ignore = [
    # Workaround for https://bugs.python.org/issue11975
    # Found on Stack Overflow (credit to Astropy project):
    #   https://stackoverflow.com/a/30624034
    ( 'py:class', "D[k] if k in D, else d.  d defaults to None." ),
    ( 'py:class', "None.  Remove all items from D." ),
    ( 'py:class', "a set-like object providing a view on D's items" ),
    ( 'py:class', "a set-like object providing a view on D's keys" ),
    ( 'py:class', "an object providing a view on D's values" ),
    ( 'py:class', "functools.partial" ),
    ( 'py:class', "mappingproxy" ),
    ( 'py:class', "module" ),
    ( 'py:class',
      "v, remove specified key and return the corresponding value." ),
    # Other weirdnesses. (Something is broken in how Sphinx autodoc processes
    # certain typing forms.)
    ( 'py:class', "Doc" ),
    ( 'py:class', "NotImplementedType" ),
    ( 'py:class', "accretive.dictionaries._DictionaryOperations" ),
    ( 'py:class', "accretive.__._H" ),
    ( 'py:class', "accretive.__._V" ),
    ( 'py:class', "accretive.__.Annotated" ),
    ( 'py:class', "accretive.__.H" ),
    ( 'py:class', "accretive.__.V" ),
    ( 'py:class', "collections.abc.Annotated" ),
    ( 'py:class', "typing_extensions._ProtocolMeta" ),
    ( 'py:class', "typing_extensions.Annotated" ),
    ( 'py:class', "typing_extensions.Any" ),
    ( 'py:class', "typing_extensions.Never" ),
    ( 'py:class', "typing_extensions.NoDefault" ),
    ( 'py:class', "typing_extensions.Self" ),
    ( 'py:class', "typing_extensions.TypeIs" ),
    ( 'py:class', "types.Annotated" ),
    ( 'py:class', "types.NoneType" ),
    ( 'py:obj', "accretive.__._H" ),
    ( 'py:obj', "accretive.__._V" ),
    ( 'py:obj', "accretive.__.H" ),
    ( 'py:obj', "accretive.__.V" ),
]

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    # Circular dependency between building HTML and publishing it.
    # Ideally, we want to warn on failure rather than ignore.
    fr'https://emcd\.github\.io/.*{project}.*/.*',
    # Stack Overflow rate limits too aggressively, which breaks matrix builds.
    r'https://stackoverflow\.com/help/.*',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.
# https://github.com/pradyunsg/furo
html_theme = 'furo'
html_theme_options = {
    'navigation_with_keys': True,
    'sidebar_hide_name': True,
}

html_static_path = [ '_static' ]

# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    'member-order': 'groupwise',
    'imported-members': False,
    'inherited-members': True,
    'show-inheritance': True,
    'undoc-members': True,
}

#autodoc_typehints = 'description'

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/3', None),
    'typing-extensions': (
        'https://typing-extensions.readthedocs.io/en/latest', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
