# router.py
import sys

from .add_file_path_comment import main as path_comment_main
from .collect_files_content import main as collect_main

COMMANDS = {
    "py-concat": collect_main,
    "path-comment": path_comment_main,
}


def print_help():
    print(
        """
asmobelt – personal CLI toolbox

Usage:
  asmobelt <command> [options]

Commands:
  py-concat
  path-comment
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
    sys.argv = [argv[0]] + argv[2:]

    return COMMANDS[cmd]()
