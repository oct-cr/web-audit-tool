#!/usr/bin/env python3
import ast
import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT_PKG = "dashkit"


DARK_PALETTE: list[str] = [
    "#1e3a5f",  # Dark blue
    "#2d5a3d",  # Dark green
    "#5a2d3d",  # Dark maroon
    "#3d4a5a",  # Dark slate
    "#5a4a2d",  # Dark olive
    "#4a2d5a",  # Dark purple
    "#5a3d2d",  # Dark brown
]


@dataclass(frozen=True)
class ModuleRef:
    dotted: str
    relpath: str

    @property
    def group(self) -> str:
        parts = self.dotted.split(".")
        return parts[1] if len(parts) > 1 else ROOT_PKG

    @property
    def node_id(self) -> str:
        return self.dotted.replace(".", "_")

    @property
    def is_package(self) -> bool:
        return Path(self.relpath).name == "__init__.py"


@dataclass(frozen=True)
class ImportRef:
    module: str | None
    level: int
    names: tuple[str, ...]


def iter_py_files(repo_root: Path) -> Iterable[Path]:
    pkg_dir = repo_root / ROOT_PKG
    yield from pkg_dir.rglob("*.py")


def file_to_module(repo_root: Path, file_path: Path) -> ModuleRef | None:
    try:
        rel = file_path.relative_to(repo_root)
    except ValueError:
        return None

    if rel.parts[0] != ROOT_PKG:
        return None

    parts = list(rel.parts)
    parts[-1] = parts[-1].removesuffix(".py")

    if parts[-1] == "__init__":
        parts = parts[:-1]

    dotted = ".".join(parts) if parts else ROOT_PKG

    if dotted == ROOT_PKG:
        return None

    return ModuleRef(dotted=dotted, relpath=str(rel))


def parse_imports(py_path: Path) -> set[ImportRef]:
    src = py_path.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = ast.parse(src, filename=str(py_path))
    except SyntaxError:
        return set()

    imports: set[ImportRef] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name:
                    imports.add(ImportRef(module=n.name, level=0, names=()))
        elif isinstance(node, ast.ImportFrom):
            imports.add(
                ImportRef(
                    module=node.module,
                    level=node.level,
                    names=tuple(name.name for name in node.names),
                )
            )

    return imports


def resolve_import_base(current: ModuleRef, imported: ImportRef) -> str | None:
    if imported.level == 0:
        return imported.module

    package_parts = current.dotted.split(".")
    if not current.is_package:
        package_parts.pop()

    levels_up = imported.level - 1
    if len(package_parts) < levels_up:
        return None

    base = package_parts[:-levels_up] if levels_up else package_parts
    if imported.module:
        base += imported.module.split(".")
    if not base:
        return None
    return ".".join(base)


def normalize_to_known_module(known: set[str], imported: str) -> str | None:
    """
    Try to map an imported module to a known module in our repo.

    Example:
      known has dashkit.services.http.client
      imported is dashkit.services.http
    We map to dashkit.services.http (package) if it exists, else try longest prefix match.
    """
    if imported in known:
        return imported

    parts = imported.split(".")
    while len(parts) > 1:
        parts.pop()
        candidate = ".".join(parts)
        if candidate in known:
            return candidate

    return None


def build_graph(repo_root: Path) -> tuple[dict[str, ModuleRef], set[tuple[str, str]]]:
    modules: dict[str, ModuleRef] = {}
    for f in iter_py_files(repo_root):
        m = file_to_module(repo_root, f)
        if m:
            modules[m.dotted] = m

    known = set(modules.keys())
    edges: set[tuple[str, str]] = set()

    for dotted, modref in modules.items():
        file_path = repo_root / modref.relpath
        imports = parse_imports(file_path)

        for imported in imports:
            base = resolve_import_base(modref, imported)
            if not base:
                continue

            if not base.startswith(ROOT_PKG + ".") and base != ROOT_PKG:
                continue

            candidates = {base}
            candidates.update(f"{base}.{name}" for name in imported.names)
            for candidate in candidates:
                target = normalize_to_known_module(known, candidate)
                if target and target != dotted:
                    edges.add((dotted, target))

    return modules, edges


def mermaid_escape(label: str) -> str:
    return label.replace('"', "'")


def emit_mermaid(mods: dict[str, ModuleRef], edges: set[tuple[str, str]]) -> str:
    groups: dict[str, list[ModuleRef]] = {}
    for m in mods.values():
        groups.setdefault(m.group, []).append(m)

    for k in groups:
        groups[k].sort(key=lambda x: x.dotted)

    lines: list[str] = []
    lines.append("flowchart LR")
    lines.append("%% Auto-generated from code (utils/deps-chart.py)")
    lines.append("")

    sorted_groups = sorted(groups.keys())

    for idx, group in enumerate(sorted_groups):
        color = DARK_PALETTE[idx % len(DARK_PALETTE)]
        lines.append(f"subgraph {group}[\"<b style='font-size:32px'>{group}</b>\"]")
        lines.append(f"  style {group} fill:{color},color:#fff,stroke:#000,stroke-width:2px")
        for m in groups[group]:
            lines.append(f'  {m.node_id}["{mermaid_escape(m.dotted)}"]')
        lines.append("end")
        lines.append("")

    for src, dst in sorted(edges):
        s = mods[src].node_id
        d = mods[dst].node_id
        lines.append(f"{s} --> {d}")

    lines.append("")
    lines.append("classDef nodeClass font-size:28px;")
    all_nodes = ",".join(m.node_id for m in mods.values())
    lines.append(f"class {all_nodes} nodeClass;")

    return "\n".join(lines)


def main() -> None:
    repo_root = Path(os.getcwd()).resolve()
    mods, edges = build_graph(repo_root)

    out_path = repo_root / "docs" / "arch-code-diagram.mmd"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    mermaid = emit_mermaid(mods, edges)
    out_path.write_text(mermaid, encoding="utf-8")

    print(f"Wrote: {out_path}")
    print(f"Modules: {len(mods)}  Edges: {len(edges)}")


if __name__ == "__main__":
    main()
