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

## Development

Format code:

```bash
make format
```
