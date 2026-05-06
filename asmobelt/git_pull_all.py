# git_pull_all.py
import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_EXCLUDES = {"node_modules", ".venv", "venv", "__pycache__"}


def _find_git_repos(root: Path, excludes: set[str]) -> list[Path]:
    repos: list[Path] = []
    for git_dir in root.rglob(".git"):
        if not git_dir.is_dir():
            continue
        if any(part in excludes for part in git_dir.parts):
            continue
        repos.append(git_dir.parent)
    return sorted(repos)


def main() -> int:
    parser = argparse.ArgumentParser(description="Find every .git repo under a path and run git pull.")
    parser.add_argument("-d", "--dir", default=".", help="Root directory to scan (default: current dir).")
    parser.add_argument(
        "--no-ff-only",
        action="store_true",
        help="Allow non-fast-forward pulls (default pulls with --ff-only).",
    )
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

    failures: list[Path] = []
    for repo in repos:
        rel = repo.relative_to(root) if repo != root else Path(".")
        print(f"==> Pulling {rel}")
        cmd = ["git", "-C", str(repo), "pull"]
        if not args.no_ff_only:
            cmd.append("--ff-only")
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            failures.append(rel)

    print()
    print(f"Done. {len(repos) - len(failures)}/{len(repos)} repos pulled successfully.")
    if failures:
        print("Failed:")
        for rel in failures:
            print(f"  - {rel}")
        return 1
    return 0
