.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

.. include:: <isopub.txt>

*******************************************************************************
Contribution
*******************************************************************************

Contribution to this project is welcome!

.. todo:: Code of Conduct.

Here are some ways that you can help:

.. todo:: Link to issue tracker.

Things to be Done
===============================================================================

.. todolist::

Development
===============================================================================

.. todo:: Link to development guide.

Initial Installation
-------------------------------------------------------------------------------

1. Ensure that you have installed `Git LFS <https://git-lfs.com/>`_.

2. Clone this repository.

3. Ensure that you have installed
   `Pipx <https://github.com/pypa/pipx/blob/main/README.md>`_.
   (If installing via ``pip``, you will want to use your system Python rather
   than the current global Python provided by Asdf, Mise, Pyenv, etc....)

4. Ensure that you have installed
   `Hatch <https://github.com/pypa/hatch/blob/master/README.md>`_ via Pipx:
   ::

       pipx install hatch

5. Ensure that you have installed `pre-commit <https://pre-commit.com/>`_ via
   Pipx:
   ::

       pipx install pre-commit

6. Install Git pre-commit and pre-push hooks:
   ::

       pre-commit install --config .auxiliary/configuration/pre-commit.yaml

Installation Updates
-------------------------------------------------------------------------------

1. Run:
   ::

       git pull

2. Remove the Hatch virtual environments:
   ::

       hatch env prune

Shell
-------------------------------------------------------------------------------

1. Run:
   ::

       hatch --env develop shell


Internal Development Interface
===============================================================================

.. automodule:: accretive.__
   :ignore-module-all: true
