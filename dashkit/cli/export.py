import argparse
import os

from ..modules.lighthouse.export import build_page_report
from ..modules.lighthouse.export_markdown import render_page_markdown
from ..services.snapshots import get_latest_lighthouse_report, workspaces_base
from ..services.workspaces import get_node_by_path, get_site_pages

reports_dirname = "reports"


def run_export(workspace, route, argv) -> int:
    parser = argparse.ArgumentParser(prog="dashkit export")
    parser.add_argument(
        "--all", dest="all_sites", action="store_true", help="Export all workspace pages"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of writing a file (single page only)",
    )
    args = parser.parse_args(argv)

    workspace_key = workspace.get("key")

    try:
        targets = _resolve_targets(workspace, route, args.all_sites)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if not targets:
        parser.error("Provide a route (site or site:page) or use --all.")

    if args.stdout:
        if len(targets) != 1:
            parser.error("--stdout requires a single site:page route.")
        site_key, page = targets[0]
        markdown = _build_markdown(workspace_key, site_key, page)
        if markdown is None:
            print(f"No report found for {site_key}:{page.get('key')}")
            return 1
        print(markdown, end="")
        return 0

    written = 0
    for site_key, page in targets:
        markdown = _build_markdown(workspace_key, site_key, page)
        if markdown is None:
            print(f"Skipped {site_key}:{page.get('key')} — no report found")
            continue

        out_path = _write_report(workspace_key, site_key, page.get("key"), markdown)
        print(f"Wrote {out_path}")
        written += 1

    return 0 if written else 1


def _resolve_targets(workspace, route, all_sites) -> list[tuple[str, dict]]:
    if all_sites:
        targets = []
        for site_key, site in workspace.get("sites", {}).items():
            for page in get_site_pages({**site, "key": site_key}):
                targets.append((site_key, page))
        return targets

    if not route:
        return []

    node = get_node_by_path(workspace, route)
    if node is None:
        raise ValueError(f"Route not found: {route}")

    if node.get("node_type") == "page":
        return [(node.get("site_key"), node)]

    return [(node.get("key"), page) for page in get_site_pages(node)]


def _build_markdown(workspace_key, site_key, page) -> str | None:
    report = get_latest_lighthouse_report(workspace_key, site_key, page.get("key"))
    if not report:
        return None

    return render_page_markdown(build_page_report(report))


def _write_report(workspace_key, site_key, page_key, markdown) -> str:
    reports_dir = os.path.join(workspaces_base, workspace_key, reports_dirname)
    os.makedirs(reports_dir, exist_ok=True)

    out_path = os.path.join(reports_dir, f"{site_key}-{page_key}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    return out_path
