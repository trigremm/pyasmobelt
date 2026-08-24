# git_pull_all.py
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path

from ._git_common import DEFAULT_EXCLUDES
from ._git_common import _find_git_repos
from ._git_common import _kill_running
from ._git_common import _run_git_captured

DEFAULT_JOBS = 5
DEFAULT_TIMEOUT = 120


def _pull(repo: Path, ff_only: bool, timeout: int) -> tuple[bool, str]:
    args = ["pull", "--ff-only"] if ff_only else ["pull"]
    return _run_git_captured(repo, *args, timeout=timeout)


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
        help=f"Number of repos to pull in parallel; keep low on slow networks (default: {DEFAULT_JOBS}).",
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Pull repos one at a time (overrides --jobs); use when parallel pulls choke the network.",
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

    jobs = 1 if args.sequential else max(1, args.jobs)
    pool = ThreadPoolExecutor(max_workers=jobs)
    pending = {repo.relative_to(root) if repo != root else Path(".") for repo in repos}
    interrupted = False
    try:
        futures = [pool.submit(work, repo) for repo in repos]
        # as_completed, not pool.map: map yields in submission order, so one slow repo
        # would hide every repo that finished after it.
        for future in as_completed(futures):
            rel, ok, output = future.result()
            pending.discard(rel)
            status = "OK " if ok else "FAIL"
            print(f"==> [{status}] {rel}", flush=True)
            if output:
                for line in output.splitlines():
                    print(f"        {line}", flush=True)
            if not ok:
                failures.append(rel)
    except KeyboardInterrupt:
        interrupted = True
        _kill_running()
        print("\nInterrupted.", file=sys.stderr)
        for rel in sorted(pending):
            print(f"  - not pulled: {rel}", file=sys.stderr)
    finally:
        pool.shutdown(wait=False, cancel_futures=True)

    if interrupted:
        return 130

    print()
    print(f"Done. {len(repos) - len(failures)}/{len(repos)} repos pulled successfully.")
    if failures:
        print("Failed:")
        for rel in sorted(failures):
            print(f"  - {rel}")
        return 1
    return 0
