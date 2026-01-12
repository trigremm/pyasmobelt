# Repository Guidelines

## Project Structure & Module Organization
- `asmobelt/` contains the CLI source; `asmobelt/cli.py` is the entrypoint and `asmobelt/router.py` dispatches commands.
- Individual commands live as modules in `asmobelt/` (e.g., `asmobelt/collect_files_content.py`).
- Build metadata is in `pyproject.toml`; helper make targets live in `Makefile` and `asmobelt.mk`.
- There is no dedicated `tests/` directory at this time.

## Build, Test, and Development Commands
- `pip install -e .` installs the CLI in editable mode for local development.
- `make format` (or `make f`) runs `autoflake`, `isort`, and `black` across the repo.
- `make add-path-comment` runs the CLI against `backend/app/` (best-effort; ignores errors).
- `make concat-py-files` generates `prompt_backend_app.txt` from `backend/app/` (best-effort; ignores errors).

## Coding Style & Naming Conventions
- Python 3.10+; keep imports single-line and line length at 120.
- Format with `autoflake`, `isort`, and `black` via `make format`.
- CLI commands are kebab-cased (e.g., `add-path-comment`, `concat-py-files`).
- New commands should expose a `main()` function in a new `asmobelt/<command>.py` module and be registered in `asmobelt/router.py`.

## Testing Guidelines
- No automated test suite is present. If you add tests, document how to run them and place them under `tests/` (e.g., `pytest -q`).

## Commit & Pull Request Guidelines
- Commit messages are short, imperative, and lower-case (e.g., “rename path-comment to add-path-comment”).
- PRs should describe behavior changes, note any new CLI commands, and include example usage if the interface changes.

## Agent-Specific Instructions
- See `CLAUDE.md` for additional development notes and CLI architecture conventions.
