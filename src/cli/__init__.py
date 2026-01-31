import argparse
import sys

from .dashkit import run_dashkit
from .lighthouse import run_lighthouse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="webaudit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("dashkit", help="Launch interactive TUI")
    subparsers.add_parser("lighthouse", help="Run Lighthouse audit")

    args, remaining = parser.parse_known_args(argv)

    if args.command == "dashkit":
        return run_dashkit(remaining)
    if args.command == "lighthouse":
        return run_lighthouse(remaining)

    return 1


if __name__ == "__main__":
    sys.exit(main())
