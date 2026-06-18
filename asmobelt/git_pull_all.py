# git_pull_all.py
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_EXCLUDES = {"node_modules", ".venv", "venv", "__pycache__"}
DEFAULT_JOBS = 8
DEFAULT_TIMEOUT = 120


def _find_git_repos(root: Path, excludes: set[str]) -> list[Path]:
    repos: list[Path] = []
    for git_dir in root.rglob(".git"):
        if not git_dir.is_dir():
            continue
        if any(part in excludes for part in git_dir.parts):
            continue
        repos.append(git_dir.parent)
    return sorted(repos)


def _git_env() -> dict[str, str]:
    """Force git to never block on an interactive prompt (credentials, SSH host keys)."""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.setdefault("GIT_SSH_COMMAND", "ssh -oBatchMode=yes")
    return env


def _pull(repo: Path, ff_only: bool, timeout: int) -> tuple[bool, str]:
    cmd = ["git", "-C", str(repo), "pull"]
    if ff_only:
        cmd.append("--ff-only")
    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=_git_env(),
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


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
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=DEFAULT_JOBS,
        help=f"Number of repos to pull in parallel (default: {DEFAULT_JOBS}).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Per-repo timeout in seconds, so a stuck repo can't block the run (default: {DEFAULT_TIMEOUT}).",
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

    ff_only = not args.no_ff_only
    failures: list[Path] = []

    def work(repo: Path) -> tuple[Path, bool, str]:
        rel = repo.relative_to(root) if repo != root else Path(".")
        ok, output = _pull(repo, ff_only, args.timeout)
        return rel, ok, output

    jobs = max(1, args.jobs)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for rel, ok, output in pool.map(work, repos):
            status = "OK " if ok else "FAIL"
            print(f"==> [{status}] {rel}")
            if output:
                for line in output.splitlines():
                    print(f"        {line}")
            if not ok:
                failures.append(rel)

    print()
    print(f"Done. {len(repos) - len(failures)}/{len(repos)} repos pulled successfully.")
    if failures:
        print("Failed:")
        for rel in failures:
            print(f"  - {rel}")
        return 1
    return 0
