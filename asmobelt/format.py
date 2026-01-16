# format.py
import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format Python code using ruff (line-length=120, single-line imports, remove unused)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to format (default: current directory)",
    )
    parser.add_argument("--check", action="store_true", help="Check formatting without making changes")

    args = parser.parse_args()

    ruff_config = "lint.isort.force-single-line=true"

    if args.check:
        # Check mode - just report issues
        check_cmd = [
            "ruff",
            "check",
            "--select",
            "I,F401,F841",
            "--line-length",
            "120",
            "--config",
            ruff_config,
            args.path,
        ]
        format_cmd = ["ruff", "format", "--check", "--line-length", "120", args.path]
    else:
        # Fix mode - apply changes
        check_cmd = [
            "ruff",
            "check",
            "--fix",
            "--select",
            "I,F401,F841",
            "--line-length",
            "120",
            "--config",
            ruff_config,
            args.path,
        ]
        format_cmd = ["ruff", "format", "--line-length", "120", args.path]

    try:
        # Run ruff check (isort + remove unused imports/vars)
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
