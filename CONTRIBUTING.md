# Contributing to sbt-framework

Thank you for taking the time to look at the toolkit. This file explains how to report a problem, how
to run the tests and linters, and how to open a pull request.

## Support

The project has a single maintainer, who responds on a best-effort basis. There is no guaranteed
response time. Issues and pull requests are read in the order they arrive.

## Reporting a problem

Open an issue at <https://github.com/spectralbranding/sbt-framework/issues> and choose the template
that fits:

- **Bug report**: something returns a wrong result, raises an unexpected error or disagrees with the
  documentation. Give the toolkit version (`pyproject.toml` or the release tag), the smallest input
  that shows the problem, the output you expected and the output you got.
- **Feature request**: a change in behaviour or a new capability. Say what you want to do and why the
  current toolkit does not let you do it.

Questions about Spectral Brand Theory itself are better answered by the papers listed in the README
than by an issue.

## Setting up

The toolkit needs Python 3.14 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/spectralbranding/sbt-framework.git
cd sbt-framework
uv sync --all-extras --dev
```

## Running the tests and linters

These are the checks that continuous integration runs on every pull request:

```bash
uv run pytest
uv run black --check .
uv run flake8 .
uv run mypy src/ --ignore-missing-imports
```

`./reproduce.sh` runs the full verification in one command and writes a log to `output/logs/`.

## Opening a pull request

1. Fork the repository and create a branch from `main`.
2. Keep the change to one topic. If it fixes an issue, name the issue in the description
   (for example `Closes #12`).
3. Add or update tests for any change in behaviour. Validator changes need a test that fails
   without the change.
4. Keep the documentation in step with the code: `docs/FRAMEWORK.md` for the method, `docs/GLOSSARY.md`
   for terms, `CHANGELOG.md` under `[Unreleased]` for anything a user would notice.
5. Run the checks above, then open the pull request against `main`.

Signals use one scale, 1 to 10, in every template, prompt and validator (see `docs/FRAMEWORK.md`,
"Signal scale and structural zeros"). A change that introduces another range for a brand signal will
fail `tests/test_signal_scale.py`.

## Licence

Code contributions are accepted under the MIT licence of the repository (`LICENSE`); data, figures
and other rendered artifacts under CC BY 4.0 (`LICENSE-data`).
