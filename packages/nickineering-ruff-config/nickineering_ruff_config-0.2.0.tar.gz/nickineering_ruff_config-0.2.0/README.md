# Nickineering's Default Ruff Config

![PyPI - Version](https://img.shields.io/pypi/v/nickineering-ruff-config)

A shareable Ruff starting config designed to get as much as possibly from Ruff
quickly.

## Usage

Install [Ruff](https://docs.astral.sh/ruff/) and create a `ruff.toml` or another
Ruff supported configuration file in your project root. Inside that file extend
this config like so:

```toml
extend = "nickineering-ruff-base.toml"

# Override these settings, or add your own here

# For example:
[format]
docstring-code-format = false
```

You will also need to create a script to copy the file, since Ruff does not
support extending from a package. This is a Poetry script which does that as an
example:

```toml
[tool.poetry.scripts]
update-ruff-base = "nickineering_ruff_config:update_ruff_base"
```

You could then run it with `poetry run update-ruff-base`. This would need to be
re-run to install new versions of this package.

You probably want to add the output to your `.gitignore` so you can rely only on
the package. To do so add the following: `nickineering-ruff-base.toml`.

Although it is not required, I recommend creating a `Makefile` or other command
runner so that calls to Ruff run both the lint and format commands. An example
`Makefile` is below:

```makefile
configure:
    poetry install
    poetry run update-ruff-base

lint:
    ruff format
    ruff check --fix
```

## Publishing

A Github Action is automatically run deploying this code to PyPi when a new
release is published in Github.
