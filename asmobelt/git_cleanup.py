# git_cleanup.py
import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_PROTECTED = ("master", "main", "dev")


def _run_git(repo: Path, *args: str, capture: bool = True) -> tuple[int, str]:
    cmd = ["git", "-C", str(repo), *args]
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=capture,
        text=True,
    )
    return result.returncode, (result.stdout or "")


def _is_git_repo(repo: Path) -> bool:
    code, _ = _run_git(repo, "rev-parse", "--git-dir")
    return code == 0


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete local branches merged into master/main/dev (dry-run by default).",
    )
    parser.add_argument("-d", "--dir", default=".", help="Repository directory (default: current dir).")
    parser.add_argument(
        "--protected",
        action="append",
        default=[],
        help=f"Protected branch (repeatable). Default: {', '.join(DEFAULT_PROTECTED)}.",
    )
    parser.add_argument("--confirm", action="store_true", help="Actually delete (without it, just dry-run).")
    parser.add_argument("-f", "--force", action="store_true", help="Use 'git branch -D' instead of '-d'.")
    args = parser.parse_args()

    repo = Path(args.dir).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        return 1
    if not _is_git_repo(repo):
        print(f"Error: {repo} is not a git repository", file=sys.stderr)
        return 1

    protected = list(args.protected) if args.protected else list(DEFAULT_PROTECTED)
    locals_ = _local_branches(repo)
    existing_protected = [b for b in protected if b in locals_]
    if not existing_protected:
        print(
            f"Error: none of the protected branches exist locally: {', '.join(protected)}",
            file=sys.stderr,
        )
        return 1

    current = _current_branch(repo)

    candidates: set[str] = set()
    for branch in existing_protected:
        candidates |= _merged_into(repo, branch)

    keep = set(protected) | ({current} if current else set())
    candidates -= keep

    if not candidates:
        print(f"Nothing to delete. Protected (existing): {', '.join(existing_protected)}")
        return 0

    sorted_candidates = sorted(candidates)
    print(f"Repo: {repo}")
    print(f"Protected: {', '.join(existing_protected)}")
    print(f"Current branch: {current or '(detached)'}")
    print(f"Branches merged into protected ({len(sorted_candidates)}):")
    for b in sorted_candidates:
        print(f"  {b}")

    if not args.confirm:
        print()
        print("Dry-run. Pass --confirm to actually delete.")
        return 0

    flag = "-D" if args.force else "-d"
    print()
    print(f"Deleting with 'git branch {flag}' ...")
    failures: list[str] = []
    for b in sorted_candidates:
        code, out = _run_git(repo, "branch", flag, b)
        if code == 0:
            print(f"  deleted: {b}")
        else:
            failures.append(b)
            msg = out.strip() or "(no output)"
            print(f"  FAILED:  {b} -- {msg}", file=sys.stderr)

    print()
    print(f"Done. {len(sorted_candidates) - len(failures)}/{len(sorted_candidates)} deleted.")
    if failures:
        print("Failed:")
        for b in failures:
            print(f"  - {b}")
        return 1
    return 0
