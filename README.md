# poetry-export-requirements

## Prerequisite

- python3.5 or later

## Features

- Support all arguments of [poetry extra](https://python-poetry.org/docs/cli/#export)

## Usage

Add hooks in your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/ehx/poetry-exrpot
  rev: master
  hooks:
    - id: export-requirements  # Export dependencies
    - id: export-requirements-dev  # Export dev-dependencies without hashes
      args: [--without-hashes]
```
