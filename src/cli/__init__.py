import argparse
import sys

from .dashkit import run_dashkit
from .lighthouse import run_lighthouse
from .printer import run_print


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="webaudit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dashkit_parser = subparsers.add_parser("dashkit", help="Launch interactive TUI")
    dashkit_parser.add_argument("route", nargs="?", default=None, help="Initial route")

    print_parser = subparsers.add_parser("print", help="Print view to terminal")
    print_parser.add_argument("route", help="Route to display")

    subparsers.add_parser("lighthouse", help="Run Lighthouse audit")

    args, remaining = parser.parse_known_args(argv)

    if args.command == "dashkit":
        return run_dashkit(args.route)
    if args.command == "print":
        return run_print(args.route)
    if args.command == "lighthouse":
        return run_lighthouse(remaining)

    return 1


if __name__ == "__main__":
    sys.exit(main())
