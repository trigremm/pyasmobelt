# cli.py
#!/usr/bin/env python3
"""
CLI wrapper that dispatches to the appropriate tool inside asmobelt.
"""

from __future__ import annotations


def cli() -> int:
    """Entry-point for `asmobelt` command."""

    import sys

    from .router import main as router_main

    # router_main already expects sys.argv (no need to manipulate here)
    try:
        return router_main(sys.argv)
    except KeyboardInterrupt:
        # Ctrl-C is a normal way to abort a long command; no traceback for it.
        print("\nAborted.", file=sys.stderr)
        return 130
