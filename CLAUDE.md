# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyasmobelt is a personal CLI toolbox providing utilities for code file manipulation. It's installed as an `asmobelt` command via pip.

## Development Commands

```bash
# Install locally for development
pip install -e .

# Format code (autoflake, isort, black with 120 line length)
make format   # or: make f
```

## CLI Usage

```bash
asmobelt <command> [options]
```

**Commands:**
- `py-concat` - Concatenate file contents into a single output file (useful for LLM prompts)
- `path-comment` - Add file path as first-line comment to source files

## Architecture

The CLI uses a simple router pattern:
- `cli.py` - Entry point that calls the router
- `router.py` - Command dispatcher mapping command names to handler functions
- Each command has its own module with a `main()` function that uses argparse

To add a new command:
1. Create `asmobelt/new_command.py` with a `main()` function
2. Add the command to `COMMANDS` dict in `router.py`

## Code Style

- Line length: 120 characters
- Single-line imports (enforced by isort)
- Use autoflake to remove unused imports
