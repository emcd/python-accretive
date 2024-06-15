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
questions, providing feedback, or answering questions. Volunteerism by real
human beings powers much of the open source available for you to use; these
real human beings have real emotional states that can be affected by how you
interact with them.

Beyond acting in a general spirit of respect for others, here are some specific
considerations:

* When asking a question, please consider the `Stack Overflow guidelines on how
  to ask a good question <https://stackoverflow.com/help/how-to-ask>`_.

* When answering a question, please consider the `Stack Overflow guidelines on
  how to write a good answer <https://stackoverflow.com/help/how-to-answer>`_.

  * Note that responses, such as "don't do that" should be avoided, however, as
    they can be perceived as condescending or inflammatory. And, they will also
    make you look worse if you are proven wrong.

  * Recommend, rather than command. Please do not be bossy or imperious.

* Respect that people have differences of opinion and that every design or
  implementation choice carries a trade-off and numerous costs. There is seldom
  a right answer.

* Please keep unstructured critique to a minimum. If you have solid ideas with
  which you want to experiment, make a fork and see how they work in practice.

* Any spamming, trolling, flaming, baiting, or other attention-stealing
  behavior is not welcome.

* Avoid flirting with offensive or sensitive issues, particularly if they are
  off-topic. This all too often leads to unnecessary fights, hurt feelings, and
  damaged trust.

* Do not create noise with "+1" or "me too" comments in issue tracker threads.

  * Please only add substantive comments that will further advance the
    understanding of an issue.

  * If you wish to upvote a comment, then please use an appropriate reacji on
    that comment without writing anything in the thread.

Part of the above list was inspired by the following sources, which are worth
reading in their own right:

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


Module ``accretive.__``
-------------------------------------------------------------------------------

.. automodule:: accretive.__
   :ignore-module-all: true


Module ``accretive._annotations``
-------------------------------------------------------------------------------

.. automodule:: accretive._annotations
   :ignore-module-all: true


Module ``accretive._docstrings``
-------------------------------------------------------------------------------

.. automodule:: accretive._docstrings
   :ignore-module-all: true
