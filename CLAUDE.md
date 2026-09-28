# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyasmobelt is a personal CLI toolbox providing utilities for code file manipulation. It's installed as an `asmobelt` command via pip.

## Development Commands

```bash
# Install locally for development
make install   # or: pip install -e .

# Format code (ruff check + ruff format)
make format    # or: make f
```

## CLI Usage

```bash
asmobelt <command> [options]
```

**Commands:**
- `add-path-comment` - Add file path as first-line comment to source files
- `chown` - Run `sudo chown -R asmo:asmo` on a target directory
- `concat-py-files` - Concatenate file contents into a single output file (useful for LLM prompts)
- `format [path] [--check]` - Format Python code using ruff
- `uuid` - Generate UUIDs
- `version` / `--version` / `-v` - Print installed version

**Git commands** (aliases are case-insensitive):
- `git-pull-all` (alias `gpa`) - Find every `.git` repo under a path and run `git pull`
- `git-branch-all` (alias `gba`) - Find every `.git` repo under a path and show its current branch
- `git-cleanup` - Delete local branches merged into master/main/dev (dry-run by default)
- `git-cleanup-all` (alias `gca`) - Run `git-cleanup` for every `.git` repo under a path

**Docker commands:**
- `docker-builder-prune` - Prune builder cache
- `docker-container-prune` - Prune stopped containers
- `docker-image-prune` - Prune dangling images
- `docker-size` - Show docker images sizes
- `docker-stop-all` - Stop all running containers
- `docker-system-prune` - Prune system (containers, networks, images, cache)

`docker-container-prune`, `docker-stop-all` and `docker-system-prune` refuse to run without `--confirm`.

## Architecture

The CLI uses a simple router pattern:
- `cli.py` - Entry point that calls the router
- `router.py` - Command dispatcher mapping command names to handler functions
- Each command has its own module with a `main()` function that uses argparse

To add a new command:
1. Create `asmobelt/new_command.py` with a `main()` function
2. Add the command to `COMMANDS` dict in `router.py`

## Makefiles

Modular makefiles live in `makefiles/` and are included from the root `Makefile`:
- `format.mk` - Ruff-based formatting and linting
- `asmobelt.mk` - Asmobelt CLI command targets
- `install.mk` - Pip install target (note: `make install` runs `git pull` first)
- `git.mk` - Git operations (available for inclusion)
- `clean.mk` - Remove build/cache leftovers (`__pycache__`, `.ruff_cache`, egg-info)

## Code Style

- Line length: 120 characters (configured in pyproject.toml)
- Formatting and linting via ruff
