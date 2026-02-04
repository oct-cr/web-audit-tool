import argparse
import importlib
import inspect
import pkgutil
from pathlib import Path
from types import ModuleType

from rich.console import CONSOLE_SVG_FORMAT, Console

PLAIN_CODE_FORMAT = CONSOLE_SVG_FORMAT.replace(
    'viewBox="0 0 {width} {height}"',
    'viewBox="{terminal_x} {terminal_y} {terminal_width} {terminal_height}"',
)


def export_console_svg(console: Console, output_file: Path) -> Path:
    svg = console.export_svg(code_format=PLAIN_CODE_FORMAT)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(svg, encoding="utf-8")

    print(f"\n✓ Screenshot saved to {output_file}")

    return output_file


def run_module_screenshots(mod: ModuleType, width: int) -> list[Path]:
    outputs: list[Path] = []

    for name in dir(mod):
        if not name.startswith("screenshot_"):
            continue
        attr = getattr(mod, name)
        if not callable(attr):
            continue

        console = Console(width=width, legacy_windows=False, force_terminal=True, record=True)

        sig = inspect.signature(attr)
        try:
            attr() if len(sig.parameters) == 0 else attr(console)
        except Exception:
            raise

        output_path = Path.cwd() / "docs" / f"{name}.svg"

        export_console_svg(console, output_path)
        outputs.append(output_path)

    return outputs


def discover_modules(module_name: str) -> list[ModuleType]:
    mods: list[ModuleType] = []
    root = importlib.import_module(module_name)
    mods.append(root)
    if hasattr(root, "__path__"):
        for _, name, _ in pkgutil.walk_packages(root.__path__, prefix=root.__name__ + "."):
            try:
                m = importlib.import_module(name)
            except Exception:
                # skip modules that fail to import
                continue
            mods.append(m)
    return mods


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modules",
        nargs="*",
        default=["dashkit.framework.presenters", "dashkit.modules"],
        help="Module paths to scan for screenshot_ functions",
    )
    parser.add_argument("--width", type=int, default=120)
    args = parser.parse_args(argv)

    for mname in args.modules:
        mods = discover_modules(mname)

        for mod in mods:
            run_module_screenshots(mod, args.width)


if __name__ == "__main__":
    main()
