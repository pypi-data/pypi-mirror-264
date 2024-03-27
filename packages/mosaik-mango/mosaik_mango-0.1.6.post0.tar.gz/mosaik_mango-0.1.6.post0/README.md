# mosaik-mango

This is an adapter for using the agent framework [mango] in a [mosaik] simulation.

This simulator is still work in progress.
If you have need for a particular entity or attribute, leave an [issue here].

[mango]: https://pypi.org/project/mango-agents/
[mosaik]: https://mosaik.offis.de
[issue here]: https://gitlab.com/mosaik/components/mosaik-mango/-/issues


## Usage

### Installation

This package can be installed from PyPI as `mosaik-mango`.


## Development

For the development of this simulator, the following tools are employed:

-   [Hatch](https://hatch.pypa.io/latest/) is used as a packaging manager.
    This offers the following commands:

    -   `hatch fmt` to format the code (using ruff)
    -   `hatch run test:test` to run pytest in a test matrix consisting of Python versions 3.9 and 3.11 and mosaik versions 3.2 and 3.3.0b1.
    -   `hatch run python` for running Python.
    -   `hatch run` to run arbitrary commands in the managed virtualenv.

    Also, we use `hatch-vcs` to automatically deduce version numbers from git tags.
    Adding a new tag starting with v on the main branch should automatically release this on PyPI.


-   [pre-commit](https://pre-commit.com/) is used to run hooks before committing and pushing.
    Install pre-commit (I recommend `pipx`) and install the hooks using `pre-commit install`.
