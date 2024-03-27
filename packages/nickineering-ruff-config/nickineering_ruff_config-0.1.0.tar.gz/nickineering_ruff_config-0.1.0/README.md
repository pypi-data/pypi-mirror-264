# Nickineering's Default Ruff Config

An aggressive Ruff config designed to get as much as possible from Ruff quickly.

## Usage

Install [Ruff](https://docs.astral.sh/ruff/) and create a `ruff.toml` or another
Ruff supported configuration file in your project root. Inside that file extend
this config like so:

```toml
extend = ["nickineering-ruff-config/ruff.toml"]

# Override these settings, or add your own here

# For example:
[format]
docstring-code-format = false
```

Although it is not required, I recommend creating a `Makefile` or other command
runner so that calls to Ruff run both the lint and format commands. An example
`Makefile` is below:

```makefile
lint:
    ruff format && ruff check --fix
```

## Publishing

A Github Action is automatically run deploying this code to PyPi when a new
version is published in Github.
