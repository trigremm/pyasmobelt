# docker.py
import argparse
import subprocess
import sys


def _run_command(cmd: list[str], check: bool = True) -> int:
    """Run a shell command and return the exit code."""
    try:
        result = subprocess.run(cmd, check=check)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode
    except FileNotFoundError:
        print("Error: docker command not found", file=sys.stderr)
        return 1


def _require_confirm(args) -> bool:
    """Check if --confirm flag is set, print warning if not."""
    if not args.confirm:
        print("This is a dangerous operation. Add --confirm to proceed.")
        return False
    return True


def stop_all_main() -> int:
    """Stop all running Docker containers."""
    parser = argparse.ArgumentParser(description="Stop all running Docker containers.")
    parser.add_argument("--confirm", action="store_true", help="Confirm the dangerous operation.")
    args = parser.parse_args()

    if not _require_confirm(args):
        return 1

    # Get all running container IDs
    result = subprocess.run(["docker", "ps", "-q"], check=False, capture_output=True, text=True)
    container_ids = result.stdout.strip().split("\n")
    container_ids = [c for c in container_ids if c]

    if not container_ids:
        print("No running containers to stop.")
        return 0

    print(f"Stopping {len(container_ids)} container(s)...")
    return _run_command(["docker", "stop", *container_ids])


def system_prune_main() -> int:
    """Prune Docker system (containers, networks, images, build cache)."""
    parser = argparse.ArgumentParser(description="Prune Docker system.")
    parser.add_argument("--confirm", action="store_true", help="Confirm the dangerous operation.")
    args = parser.parse_args()

    if not _require_confirm(args):
        return 1

    return _run_command(["docker", "system", "prune", "-f", "-a"], check=False)


def container_prune_main() -> int:
    """Prune stopped Docker containers."""
    parser = argparse.ArgumentParser(description="Prune stopped Docker containers.")
    parser.add_argument("--confirm", action="store_true", help="Confirm the dangerous operation.")
    args = parser.parse_args()

    if not _require_confirm(args):
        return 1

    return _run_command(["docker", "container", "prune", "-f"], check=False)


def image_prune_main() -> int:
    """Prune dangling Docker images."""
    parser = argparse.ArgumentParser(description="Prune dangling Docker images.")
    parser.parse_args()

    return _run_command(["docker", "image", "prune", "-f"], check=False)


def builder_prune_main() -> int:
    """Prune Docker builder cache older than 36 hours."""
    parser = argparse.ArgumentParser(description="Prune Docker builder cache older than 36 hours.")
    parser.parse_args()

    return _run_command(["docker", "builder", "prune", "--filter", "until=36h", "-f"], check=False)


def size_main() -> int:
    """Show Docker images sizes."""
    parser = argparse.ArgumentParser(description="Show Docker images sizes.")
    parser.add_argument("--filter", "-f", default=None, help="Filter images by name (grep pattern).")
    args = parser.parse_args()

    print("Docker images sizes:")
    result = subprocess.run(["docker", "images"], check=False, capture_output=True, text=True)

    if args.filter:
        lines = result.stdout.strip().split("\n")
        # Always print header
        if lines:
            print(lines[0])
        for line in lines[1:]:
            if args.filter in line:
                print(line)
    else:
        print(result.stdout)

    return result.returncode
