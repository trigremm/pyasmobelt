# router.py
import sys

from .add_file_path_comment import main as path_comment_main
from .chown_backend import main as chown_backend_main
from .collect_files_content import main as collect_main
from .docker import builder_prune_main
from .docker import container_prune_main
from .docker import image_prune_main
from .docker import size_main
from .docker import stop_all_main
from .docker import system_prune_main
from .format import main as format_main
from .git_cleanup import main as git_cleanup_main
from .git_pull_all import main as git_pull_all_main
from .uuid import main as uuid_main

COMMANDS = {
    "add-path-comment": path_comment_main,
    "chown": chown_backend_main,
    "concat-py-files": collect_main,
    "docker-builder-prune": builder_prune_main,
    "docker-container-prune": container_prune_main,
    "docker-image-prune": image_prune_main,
    "docker-size": size_main,
    "docker-stop-all": stop_all_main,
    "docker-system-prune": system_prune_main,
    "format": format_main,
    "git-cleanup": git_cleanup_main,
    "git-pull-all": git_pull_all_main,
    "uuid": uuid_main,
}


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
  git-cleanup            Delete local branches merged into master/main/dev (dry-run by default)
  git-pull-all           Run git pull in every .git repo under a directory
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

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}\n")
        print_help()
        return 1

    # Remove the command from sys.argv so underlying argparse sees clean args
    sys.argv = [f"{argv[0]} {cmd}", *argv[2:]]

    return COMMANDS[cmd]()
