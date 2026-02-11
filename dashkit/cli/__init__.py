import argparse
import os
import sys

from dotenv import load_dotenv

from dashkit.services.workspaces import load_workspace

from .lighthouse import run_lighthouse
from .printer import run_print
from .tui import run_tui

load_dotenv()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="webaudit")
    subparsers = parser.add_subparsers(dest="command", required=True)
    workspace_default = os.getenv("WORKSPACE_DEFAULT", "demo")
    parser.add_argument("-w", default=workspace_default, help="Workspace key")

    tui_parser = subparsers.add_parser("tui", help="Launch interactive TUI")
    tui_parser.add_argument("route", nargs="?", default=None, help="Initial route")

    print_parser = subparsers.add_parser("print", help="Print view to terminal")
    print_parser.add_argument("route", help="Route to display")

    lighthouse_parser = subparsers.add_parser("lighthouse", help="Run Lighthouse audit")
    lighthouse_parser.add_argument("route", help="Route to audit")

    workspace_key = parser.parse_args(argv).w

    try:
        workspace = load_workspace(workspace_key)
    except Exception as e:
        print(f"Error loading workspace: {e}", file=sys.stderr)
        return 1

    args, remaining = parser.parse_known_args(argv)

    if args.command == "tui":
        return run_tui(workspace, args.route)
    if args.command == "print":
        return run_print(workspace, args.route)
    if args.command == "lighthouse":
        return run_lighthouse(workspace, args.route, remaining)

    return 1


if __name__ == "__main__":
    sys.exit(main())
