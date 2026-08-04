# git_cleanup_all.py
import argparse
import sys
from pathlib import Path

from ._git_common import DEFAULT_EXCLUDES
from ._git_common import DEFAULT_PROTECTED
from ._git_common import _current_branch
from ._git_common import _find_git_repos
from ._git_common import _local_branches
from ._git_common import _merged_into
from ._git_common import _run_git


def _cleanup_repo(repo: Path, protected: list[str], confirm: bool, force: bool) -> tuple[int, int]:
    """Return (deleted_count, failed_count) for the repo."""
    locals_ = _local_branches(repo)
    existing_protected = [b for b in protected if b in locals_]
    if not existing_protected:
        print(f"  skipped: none of the protected branches exist locally ({', '.join(protected)})")
        return 0, 0

    current = _current_branch(repo)

    candidates: set[str] = set()
    for branch in existing_protected:
        candidates |= _merged_into(repo, branch)

    keep = set(protected) | ({current} if current else set())
    candidates -= keep

    if not candidates:
        print(f"  nothing to delete (protected: {', '.join(existing_protected)})")
        return 0, 0

    sorted_candidates = sorted(candidates)
    print(f"  protected: {', '.join(existing_protected)}; current: {current or '(detached)'}")
    print(f"  merged into protected ({len(sorted_candidates)}):")
    for b in sorted_candidates:
        print(f"    {b}")

    if not confirm:
        return 0, 0

    flag = "-D" if force else "-d"
    deleted = 0
    failed = 0
    for b in sorted_candidates:
        code, out = _run_git(repo, "branch", flag, b)
        if code == 0:
            deleted += 1
            print(f"    deleted: {b}")
        else:
            failed += 1
            msg = out.strip() or "(no output)"
            print(f"    FAILED:  {b} -- {msg}", file=sys.stderr)
    return deleted, failed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Find every .git repo under a path and delete local branches merged "
            "into master/main/dev (dry-run by default)."
        ),
    )
    parser.add_argument("-d", "--dir", default=".", help="Root directory to scan (default: current dir).")
    parser.add_argument(
        "--protected",
        action="append",
        default=[],
        help=f"Protected branch (repeatable). Default: {', '.join(DEFAULT_PROTECTED)}.",
    )
    parser.add_argument("--confirm", action="store_true", help="Actually delete (without it, just dry-run).")
    parser.add_argument("-f", "--force", action="store_true", help="Use 'git branch -D' instead of '-d'.")
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

    protected = list(args.protected) if args.protected else list(DEFAULT_PROTECTED)

    total_deleted = 0
    total_failed = 0
    for repo in repos:
        rel = repo.relative_to(root) if repo != root else Path(".")
        print(f"==> {rel}")
        deleted, failed = _cleanup_repo(repo, protected, args.confirm, args.force)
        total_deleted += deleted
        total_failed += failed

    print()
    if args.confirm:
        print(f"Done. {len(repos)} repos scanned, {total_deleted} branch(es) deleted, {total_failed} failed.")
        return 1 if total_failed else 0
    print(f"Dry-run. {len(repos)} repos scanned. Pass --confirm to actually delete.")
    return 0
