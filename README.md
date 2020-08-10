# poetry-export-requirements

Use this pre-commit hook to ensure that the requirement output is stage for commit when you use a Poetry to manage packages and add new dependencies.

pre-commit: https://github.com/pre-commit/pre-commit

## Prerequisite

- python3.6 or later

## Features

- Support all arguments of [poetry export](https://python-poetry.org/docs/cli/#export) command

## Usage

Add hooks in your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/ehx/poetry-export-requirements
  rev: master
  hooks:
    - id: export-requirements  # Export dependencies
    - id: export-requirements-dev  # Export dev-dependencies without hashes
      args: [--without-hashes]
```

## Additional arguments

```text
--without-output: Don't check that requirements output isn't staged in commit
```
