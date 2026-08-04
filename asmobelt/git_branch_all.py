# git_branch_all.py
import argparse
import subprocess
import sys
from pathlib import Path

from ._git_common import DEFAULT_EXCLUDES
from ._git_common import _find_git_repos


def _current_branch(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "(error)"
    branch = result.stdout.strip()
    if branch == "HEAD":
        return "(detached)"
    return branch or "(unknown)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Find every .git repo under a path and show its current branch.")
    parser.add_argument("-d", "--dir", default=".", help="Root directory to scan (default: current dir).")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Extra directory name to skip. Can be passed multiple times.",
    )
    args = parser.parse_args()

    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        return 1

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    repos = _find_git_repos(root, excludes)

    if not repos:
        print(f"No git repositories found under {root}")
        return 0

    rows: list[tuple[str, str]] = []
    for repo in repos:
        rel = repo.relative_to(root) if repo != root else Path(".")
        rows.append((str(rel), _current_branch(repo)))

    width = max(len(rel) for rel, _ in rows)
    for rel, branch in rows:
        print(f"{rel.ljust(width)}  {branch}")

    print()
    print(f"Done. {len(repos)} repos.")
    return 0
