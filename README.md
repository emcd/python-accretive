Contains a Python library package that provides accretive data structures.
These are data structures which grow but do not shrink. In other words, entries
can be added to them but altered or removed.

# Installation

## Initial Installation

Currently, there is no installable package. But, the application can be setup
to run from a virtual environment without too much hassle by following these
steps:

1. Ensure that you have installed [Git LFS](https://git-lfs.com/).
1. Clone this repository.
1. Ensure that you have installed
   [Pipx](https://github.com/pypa/pipx/blob/main/README.md#install-pipx).
   (If installing via `pip`, you will want to use your system Python rather
   than the current global Python provided by Asdf, Mise, Pyenv, etc....)
1. Ensure that you have installed
   [Hatch](https://github.com/pypa/hatch/blob/master/README.md) via Pipx:
   ```
   pipx install hatch
   ```

## Installation Updates

1. Run:
   ```
   git pull
   ```
1. Remove the `default` virtual environment:
   ```
   hatch env remove default
   ```

The `default` virtual environment will be automatically rebuilt next time the
application is run via Hatch.

## Development

1. Run:
   ```
   hatch --env develop shell
   ```
