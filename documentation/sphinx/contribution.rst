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

Contribution to this project is welcome! However, it must follow the code of
conduct for the project.

Code of Conduct
===============================================================================

Please act in the spirit of respect for others, whether you are asking
questions, providing feedback, or answering questions. Volunteers power much of
the open source available for you to use, and they have real emotional states
that can be affected by your interactions.

Specific Considerations
-------------------------------------------------------------------------------

* **Asking Questions**: Follow the `Stack Overflow guidelines on how to ask a
  good question <https://stackoverflow.com/help/how-to-ask>`_.

* **Answering Questions**: Follow the `Stack Overflow guidelines on how to
  write a good answer <https://stackoverflow.com/help/how-to-answer>`_.
  However, avoid responses like "don't do that," as they can be perceived as
  condescending. Recommend rather than command.

* **No Egotism**: Argue by facts and reason, not by appeals to authority or
  perceived popular opinion.

* **Differences of Opinion**: Understand that people will have differences of
  opinion and that every design or implementation choice carries trade-offs and
  costs. There is seldom a right answer.

* **Constructive Critique**: Keep unstructured critique to a minimum. If you
  have solid ideas experiment with them in a fork.

* **No Disruptive Behavior**: Any spamming, trolling, flaming, baiting, or
  other attention-stealing behavior is not welcome.

* **Avoid Sensitive Issues**: Do not engage in offensive or sensitive topics,
  particularly if they are off-topic. This can lead to unnecessary fights, hurt
  feelings, and damaged trust.

* **Avoid Noise**: Do not create noise with "+1" or "me too" comments. Add only
  substantive comments that advance the understanding of an issue. Use
  appropriate reaction mechanisms to upvote comments.

Inspirations
-------------------------------------------------------------------------------

This code of conduct is inspired, in part, by the following sources, which are
worth reading:

* `Python Software Foundation Code of Conduct
  <https://policies.python.org/python.org/code-of-conduct/>`_ (in particular,
  the ``Our Community`` and ``Our Standards: Inappropriate Behavior`` sections)

* `Rust Code of Conduct <https://www.rust-lang.org/policies/code-of-conduct>`_

* `How to Ask Questions the Smart Way
  <http://www.catb.org/~esr/faqs/smart-questions.html>`_ (note that some of the
  showcased responses to "stupid questions" may not be acceptable)

.. note:: Please do not contact the authors of the above documents
          for anything related to this project.

Ways to Contribute
===============================================================================

* File bug reports and feature requests in the `issue tracker
  <https://github.com/emcd/python-accretive/issues>`_. (Please try to avoid
  duplicate issues.)

* Fork the repository and submit `pull requests
  <https://github.com/emcd/python-accretive/pulls>`_ to improve the library or
  its documentation.

Development
===============================================================================

Initial Installation
-------------------------------------------------------------------------------

1. Ensure that you have installed `Git LFS <https://git-lfs.com/>`_.

2. Clone your fork of the repository.

3. Install Git LFS Git hooks in this repository:
   ::

        git lfs install

4. Ensure that you have installed
   `Pipx <https://github.com/pypa/pipx/blob/main/README.md>`_.
   (If installing via ``pip``, you will want to use your system Python rather
   than the current global Python provided by Asdf, Mise, Pyenv, etc....)

5. Ensure that you have installed
   `Hatch <https://github.com/pypa/hatch/blob/master/README.md>`_ via Pipx:
   ::

        pipx install hatch

6. Ensure that you have installed `pre-commit <https://pre-commit.com/>`_ via
   Pipx:
   ::

        pipx install pre-commit

7. Install Git pre-commit and pre-push hooks:
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

Python Interpreter
-------------------------------------------------------------------------------

1. Run:
   ::

        hatch --env develop run python

Shell
-------------------------------------------------------------------------------

1. Run:
   ::

        hatch --env develop shell

Guidelines
-------------------------------------------------------------------------------

* Be sure to install the Git hooks, as mentioned in the ``Installation``
  section. This will save you turnaround time from pull request validation
  failures.

* Maintain or improve the current level of code coverage. Even if code coverage
  is at 100%, consider cases which are not explicitly tested.

* Allow natural and expected Python exceptions to pass through the application
  programming interface boundary. Raise an exception from the library for any
  failure condition that arises from the use of the provided features that are
  part of the interfaces of the underlying Python object types or functions.

* Never swallow exceptions. Either chain a ``__cause__`` with a ``from``
  original exception or raise a new exception with original exception as the
  ``__context__``.

* Avoid ancillary imports into a module namespace. Instead, place common
  imports into the `__` base module or import at the function level. This
  avoids pollution of the module namespace, which should only have public
  attributes which relate to the interface that it is providing. This also
  makes functions more relocatable, since they carry their dependencies with
  them rather than rely on imports within the module which houses them.

* Documentation must be written as Sphinx reStructuredText. The docstrings for
  functions must not include parameter or return type documentation. Parameter
  and return type documentation is handled via :pep:`727` annotations. Pull
  requests, which include Markdown documentation or which attempt to provide
  function docstrings in the style of Google, NumPy, Sphinx, etc..., will be
  rejected.

* Respect the existing code style. Pull requests, which attempt to enforce
  the ``black`` style  or another style, will be rejected. A summary of the
  style is:

  - **Spacing**: Use spaces between identifiers and other tokens. Modern
    writing systems use this convention, which emerged around the 7th century
    of the Common Era, to improve readability. Computer code can generally be
    written this way too... also to improve readability.

  - **Line Width**: Follow :pep:`8` on this: no more than 79 columns for code
    lines. Consider how long lines affect display on laptops or side-by-side
    code panes with enlarged font sizes. (Enlarged font sizes are used to
    reduce eye strain and allow people to code with visual correction.)

  - **Vertical Compactness**: Function definitions, loop bodies, and condition
    bodies, which consist of single statement and which are sufficiently short,
    should be placed on the same line as the statement that introduces the
    body. Blank lines should not be used to group statements within a function
    body. If you need to group statements in a function, then perhaps the
    function should be refactored into multiple functions. Function bodies
    should not be longer than thirty lines long. I.e., one should not have to
    scroll to read a function.

* Use long option names, whenever possible, in command line examples.


Internal Development Interface
===============================================================================


Module ``accretive.__``
-------------------------------------------------------------------------------

.. automodule:: accretive.__
   :ignore-module-all: true


Module ``accretive._annotations``
-------------------------------------------------------------------------------

.. automodule:: accretive._annotations


Module ``accretive._docstrings``
-------------------------------------------------------------------------------

.. automodule:: accretive._docstrings
   :ignore-module-all: true


Release Process
===============================================================================

Initial Release Candidate
-------------------------------------------------------------------------------

1. Checkout the ``master`` branch.
2. Pull from upstream to ensure all changes have been synced.
3. Checkout new release branch: ``release-<major>.<minor>``.
4. Bump alpha to release candidate. Tag. Commit.
5. Run Towncrier. Commit.
6. Push release branch and tag to upstream with tracking enabled.
7. Bump alpha to next minor or major version on ``master`` branch. Tag. Commit.
8. Cherry-pick Towncrier commit back to ``master`` branch.

Release
-------------------------------------------------------------------------------

1. Checkout release branch.
2. Bump release candidate to release. Tag. Commit.
3. Push release branch and tag to upstream.
4. Run the ``release`` workflow in Github Actions, using the release tag.

Postrelease Patch
-------------------------------------------------------------------------------

1. Checkout release branch.
2. Develop and test patch against branch. Add Towncrier entry. Commit.
3. Bump release to patch or increment patch number. Tag. Commit.
4. Run Towncrier. Commit.
5. Push release branch and tag to upstream.
6. Run the ``release`` workflow in Github Actions, using the release tag.
7. Cherry-pick patch and Towncrier commit back to ``master`` branch, resolving
   conflicts as necessary.
