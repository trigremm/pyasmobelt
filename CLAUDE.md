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
- `concat-py-files` - Concatenate file contents into a single output file (useful for LLM prompts)
- `format` - Format Python code using ruff
- `uuid` - Generate UUIDs

**Docker commands:**
- `docker-builder-prune` - Prune builder cache
- `docker-container-prune` - Prune stopped containers
- `docker-image-prune` - Prune dangling images
- `docker-size` - Show docker images sizes
- `docker-stop-all` - Stop all running containers
- `docker-system-prune` - Prune system (containers, networks, images, cache)

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
- `install.mk` - Pip install target
- `git.mk` - Git operations (available for inclusion)

## Code Style

- Line length: 120 characters (configured in pyproject.toml)
- Formatting and linting via ruff
