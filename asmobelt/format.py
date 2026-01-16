# format.py
import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format and lint Python code using ruff (reads config from pyproject.toml)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to format (default: current directory)",
    )
    parser.add_argument("--check", action="store_true", help="Check formatting without making changes")

    args = parser.parse_args()

    if args.check:
        check_cmd = ["ruff", "check", args.path]
        format_cmd = ["ruff", "format", "--check", args.path]
    else:
        check_cmd = ["ruff", "check", "--fix", args.path]
        format_cmd = ["ruff", "format", args.path]

    try:
        # Run ruff check (linting: pycodestyle, pyflakes, isort, pylint, etc.)
        subprocess.run(check_cmd, check=False)
        # Run ruff format (black-like formatting)
        result = subprocess.run(format_cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print(
            "Error: ruff is not installed. Install it with: pip install ruff",
            file=sys.stderr,
        )
        return 1
