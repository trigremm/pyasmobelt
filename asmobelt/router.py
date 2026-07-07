# router.py
import sys
from importlib import import_module
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version


def _lazy(module: str, attr: str = "main"):
    """Return a zero-arg callable that imports module.attr on first call.

    Keeps command modules out of the import graph until a command actually
    runs, so `import asmobelt.router` stays cheap (the cli.py lazy-import intent).
    """

    def _run():
        return getattr(import_module(f".{module}", __package__), attr)()

    return _run


COMMANDS = {
    "add-path-comment": _lazy("add_file_path_comment"),
    "chown": _lazy("chown_backend"),
    "concat-py-files": _lazy("collect_files_content"),
    "docker-builder-prune": _lazy("docker", "builder_prune_main"),
    "docker-container-prune": _lazy("docker", "container_prune_main"),
    "docker-image-prune": _lazy("docker", "image_prune_main"),
    "docker-size": _lazy("docker", "size_main"),
    "docker-stop-all": _lazy("docker", "stop_all_main"),
    "docker-system-prune": _lazy("docker", "system_prune_main"),
    "format": _lazy("format"),
    "git-branch-all": _lazy("git_branch_all"),
    "git-cleanup": _lazy("git_cleanup"),
    "git-cleanup-all": _lazy("git_cleanup_all"),
    "git-pull-all": _lazy("git_pull_all"),
    "uuid": _lazy("uuid"),
}

# Short aliases (case-insensitive: GPA == gpa)
ALIASES = {
    "gpa": "git-pull-all",
    "gba": "git-branch-all",
    "gca": "git-cleanup-all",
}


def get_version():
    try:
        return _pkg_version("pyasmobelt")
    except PackageNotFoundError:
        return "unknown"


def print_help():
    print(
        """
asmobelt - personal CLI toolbox

Usage:
  asmobelt <command> [options]

Commands:
  add-path-comment       Add file path as first-line comment
  chown                  sudo chown -R asmo:asmo on ./backend (or given path)
  concat-py-files        Concatenate file contents into single output
  format                 Format Python code using ruff
  git-branch-all         Show current branch of every .git repo under a directory  (alias: GBA)
  git-cleanup            Delete local branches merged into master/main/dev (dry-run by default)
  git-cleanup-all        Run git-cleanup across every .git repo under a directory  (alias: GCA)
  git-pull-all           Run git pull in every .git repo under a directory  (alias: GPA)
  uuid                   Generate UUIDs

Docker (danger zone - some require --confirm):
  docker-builder-prune   Prune builder cache (>36h)
  docker-container-prune Prune stopped containers
  docker-image-prune     Prune dangling images
  docker-size            Show docker images sizes
  docker-stop-all        Stop all running containers
  docker-system-prune    Prune system (containers, networks, images, cache)
"""
    )


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print_help()
        return 0

    cmd = argv[1]

    if cmd in ("--version", "-v", "version"):
        print(f"asmobelt {get_version()}")
        return 0

    # Resolve short aliases (case-insensitive), e.g. GPA -> git-pull-all
    cmd = ALIASES.get(cmd.lower(), cmd)

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}\n")
        print_help()
        return 1

    # Remove the command from sys.argv so underlying argparse sees clean args
    sys.argv = [f"{argv[0]} {cmd}", *argv[2:]]

    return COMMANDS[cmd]()
