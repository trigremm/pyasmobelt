# _git_common.py
import os
import signal
import subprocess
import threading
from contextlib import suppress
from pathlib import Path

DEFAULT_EXCLUDES = {"node_modules", ".venv", "venv", "__pycache__"}
DEFAULT_PROTECTED = ("master", "main", "dev")

# Non-interactive ssh: never wait on a passphrase/host-key prompt, and never let a
# stalled TCP connection sit there until the kernel gives up on it.
SSH_OPTS = "-oBatchMode=yes -oConnectTimeout=10 -oServerAliveInterval=10 -oServerAliveCountMax=3"


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


def _git_env() -> dict[str, str]:
    """Env that keeps git non-interactive: no credential, passphrase or host-key prompt can block us."""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    # `echo` answers every credential question with an empty string, so https remotes
    # fail fast instead of waiting on an askpass helper (GUI ones ignore the flag above).
    env["GIT_ASKPASS"] = "echo"
    env["SSH_ASKPASS_REQUIRE"] = "never"
    # Keep a caller-provided ssh command, but append our options; ssh honours the first
    # occurrence of an option, so anything the caller set already wins.
    base = env.get("GIT_SSH_COMMAND", "").strip() or "ssh"
    env["GIT_SSH_COMMAND"] = f"{base} {SSH_OPTS}"
    return env


_RUNNING: set[subprocess.Popen] = set()
_RUNNING_LOCK = threading.Lock()


def _kill_process_group(proc: subprocess.Popen) -> None:
    """Kill git *and* whatever it spawned.

    Killing git alone is not enough: its ssh child inherits the stdout pipe, so reading
    that pipe keeps blocking until ssh exits on its own.
    """
    with suppress(OSError):
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        return
    with suppress(OSError):
        proc.kill()


def _kill_running() -> None:
    """Kill every git process this run still has in flight (used on Ctrl-C)."""
    with _RUNNING_LOCK:
        procs = list(_RUNNING)
    for proc in procs:
        _kill_process_group(proc)


def _run_git_captured(repo: Path, *args: str, timeout: int) -> tuple[bool, str]:
    """Run a git command non-interactively, capturing stdout+stderr, honouring `timeout`."""
    proc = subprocess.Popen(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=_git_env(),
        start_new_session=True,  # own process group, so we can kill ssh children too
    )
    with _RUNNING_LOCK:
        _RUNNING.add(proc)
    try:
        try:
            output, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_process_group(proc)
            with suppress(subprocess.TimeoutExpired):
                proc.communicate(timeout=5)
            return False, f"timed out after {timeout}s"
        return proc.returncode == 0, (output or "").strip()
    finally:
        with _RUNNING_LOCK:
            _RUNNING.discard(proc)


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
