import json
import os
import re
from typing import cast

workspaces_base = "workspaces"


def write_snapshot(workspace_key: str, snapshot_key: str, body: bytes) -> str:
    workspace_dir = os.path.join(workspaces_base, workspace_key)
    os.makedirs(workspace_dir, exist_ok=True)
    out_path = os.path.join(workspace_dir, f"{snapshot_key}.json")

    with open(out_path, "wb") as f:
        f.write(body)

    return out_path


def read_report(workspace_key, url_report_path):
    path = os.path.join(workspaces_base, workspace_key, url_report_path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return data


def _walk_matching(workspace_key, regex_pattern):
    """Yield (ts, rel_path) for every JSON file matching regex_pattern."""
    workspace_folder = os.path.join(workspaces_base, workspace_key)

    for root, _, files in os.walk(workspace_folder):
        rel_root = os.path.relpath(root, workspace_folder)

        for f in files:
            if not f.lower().endswith(".json"):
                continue

            m = re.match(regex_pattern, f)
            if not m:
                continue

            rel_path = os.path.join(rel_root, f) if rel_root != os.curdir else f

            yield m.group("ts"), rel_path


def get_url_reports(workspace_key, regex_pattern):
    latest = {}

    for ts, rel_path in _walk_matching(workspace_key, regex_pattern):
        prev = latest.get(rel_path)

        if prev is None or (ts and (not prev[0] or ts > prev[0])):
            latest[rel_path] = (ts, rel_path)

    results = [v[1] for v in latest.values()]

    return results


def _lighthouse_report_pattern(site_key: str, page_key: str) -> str:
    pattern_str = f"^lhr-{re.escape(site_key)}-{re.escape(page_key)}-mobile-"
    pattern_ts = r"(?P<ts>\d{8}_\d{6})\.json$"
    return rf"{pattern_str}{pattern_ts}"


def get_latest_lighthouse_report(
    workspace_key: str, site_key: str, page_key: str
) -> dict:
    regex_pattern = _lighthouse_report_pattern(site_key, page_key)

    report_urls = get_url_reports(workspace_key, regex_pattern)

    if not report_urls:
        return {}

    return cast("dict", read_report(workspace_key, report_urls[0]))


def get_recent_lighthouse_reports(
    workspace_key: str, site_key: str, page_key: str, n: int = 2
) -> list[tuple[str, dict]]:
    """Return up to ``n`` most recent ``(timestamp, report)`` pairs, newest first."""
    regex_pattern = _lighthouse_report_pattern(site_key, page_key)

    matches = sorted(
        _walk_matching(workspace_key, regex_pattern),
        key=lambda m: m[0] or "",
        reverse=True,
    )

    return [
        (ts, cast("dict", read_report(workspace_key, rel_path)))
        for ts, rel_path in matches[:n]
    ]


def get_lighthouse_reports(
    workspace_key: str, site_key: str, page_key: str
) -> list[tuple[str, dict]]:
    regex_pattern = _lighthouse_report_pattern(site_key, page_key)
    matches = sorted(
        _walk_matching(workspace_key, regex_pattern),
        key=lambda match: match[0] or "",
        reverse=True,
    )

    return [
        (timestamp, cast("dict", read_report(workspace_key, relative_path)))
        for timestamp, relative_path in matches
    ]
