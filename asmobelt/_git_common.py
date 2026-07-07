# _git_common.py
import os
import subprocess
from pathlib import Path

DEFAULT_EXCLUDES = {"node_modules", ".venv", "venv", "__pycache__"}
DEFAULT_PROTECTED = ("master", "main", "dev")


def _find_git_repos(root: Path, excludes: set[str]) -> list[Path]:
    repos: list[Path] = []
    for dirpath, dirnames, _filenames in os.walk(root):
        # prune excluded dirs in-place so we never descend into them
        dirnames[:] = [d for d in dirnames if d not in excludes]
        if ".git" in dirnames:
            repos.append(Path(dirpath))
            # never recurse into the repo's own git internals
            dirnames.remove(".git")
    return sorted(repos)


def _run_git(repo: Path, *args: str, capture: bool = True) -> tuple[int, str]:
    cmd = ["git", "-C", str(repo), *args]
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=capture,
        text=True,
    )
    return result.returncode, (result.stdout or "")


def _current_branch(repo: Path) -> str:
    code, out = _run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0:
        return ""
    return out.strip()


def _local_branches(repo: Path) -> set[str]:
    code, out = _run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/")
    if code != 0:
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def _merged_into(repo: Path, branch: str) -> set[str]:
    code, out = _run_git(repo, "branch", "--merged", branch, "--format=%(refname:short)")
    if code != 0:
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}
