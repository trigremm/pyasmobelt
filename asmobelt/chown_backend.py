# chown_backend.py
import argparse
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description="Run sudo chown -R asmo:asmo on a target directory.")
    parser.add_argument("path", nargs="?", default="backend", help="Target directory (default: backend).")
    args = parser.parse_args()

    return subprocess.run(["sudo", "chown", "-R", "asmo:asmo", args.path], check=False).returncode
