# pyasmobelt

Personal CLI toolbox (collect files, add path comments, and more).

## Install

```bash
pip install -e .
```

## Usage

```bash
asmobelt <command> [options]
```

### Commands

#### concat-py-files

Concatenate file contents from a directory into a single output file.

Options:
- `-p, --path` (required): directory to scan
- `-o, --output`: output file (default: `prompt.txt`)
- `-i, --ignore`: extra ignore patterns (space-separated)
- `-e, --include`: comma-separated extensions/filenames to include
- `-x, --exclude`: comma-separated extensions/filenames to exclude

Example:

```bash
asmobelt concat-py-files -p backend/app -o prompt_backend_app.txt
```

#### add-path-comment

Insert a file-path comment at the top of supported source files.

Options:
- `-f, --files`: specific files to process
- `--stdin`: read additional file paths from stdin
- `-d, --directory`: process all supported files in a directory recursively
- `--root`: root dir for relative paths (defaults to `--directory` or cwd)
- `--ignore-dirs`: directory names to ignore when using `--directory`
- `--max-remove`: max existing header lines to remove (default: 3)
- `--no-trim-leading-blank-lines`: keep blank lines after removing old header
- `--dry-run`: report changes without writing
- `-v, --verbose`: verbose output

Examples:

```bash
# Process a directory (root defaults to directory)
asmobelt add-path-comment -d backend/app

# Process specific files
asmobelt add-path-comment -f file1.py file2.js

# Use with git (modified files)
git ls-files --modified | asmobelt add-path-comment --stdin --root backend/app
```

#### uuid

Generate UUIDs with randomized uppercase letters.

Options:
- `-n, --count`: number of UUIDs to generate (default: 20)
- `--upper-ratio`: probability that each hex letter is uppercased (0 to 1)
- `--block-case`: randomize case per dash-separated block instead of per letter

Example:

```bash
asmobelt uuid -n 20 --upper-ratio 0.6 --block-case
```

#### format

Format Python code using ruff.

```bash
asmobelt format
```

#### Docker commands

```bash
asmobelt docker-builder-prune    # Prune builder cache (>36h)
asmobelt docker-container-prune  # Prune stopped containers
asmobelt docker-image-prune      # Prune dangling images
asmobelt docker-size             # Show docker images sizes
asmobelt docker-stop-all         # Stop all running containers
asmobelt docker-system-prune     # Prune system (containers, networks, images, cache)
```

## Development

```bash
make install   # pip install -e .
make format    # ruff check --fix + ruff format (or: make f)
```

### Makefiles

Modular makefiles in `makefiles/` included from root `Makefile`:
- `format.mk` - Ruff-based formatting and linting
- `asmobelt.mk` - Asmobelt CLI command targets
- `install.mk` - Pip install
- `git.mk` - Git operations (available for inclusion)
