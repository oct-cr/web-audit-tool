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


def get_url_reports(workspace_key, regex_pattern):
    latest = {}

    workspace_folder = os.path.join(workspaces_base, workspace_key)

    for root, _, files in os.walk(workspace_folder):
        rel_root = os.path.relpath(root, workspace_folder)

        for f in files:
            if not f.lower().endswith(".json"):
                continue

            rel_path = os.path.join(rel_root, f) if rel_root != os.curdir else f

            m = re.match(regex_pattern, f)

            if not m:
                continue

            ts = m.group("ts")

            key = os.path.join(rel_root, f) if rel_root != os.curdir else f

            prev = latest.get(key)

            if prev is None or (ts and (not prev[0] or ts > prev[0])):
                latest[key] = (ts, rel_path)

    results = [v[1] for v in latest.values()]

    return results


def get_latest_lighthouse_report(
    workspace_key: str, site_key: str, page_key: str
) -> dict:
    pattern_str = f"^lhr-{re.escape(site_key)}-{re.escape(page_key)}-mobile-"
    pattern_ts = r"(?P<ts>\d{8}_\d{6})\.json$"
    regex_pattern = rf"{pattern_str}{pattern_ts}"

    report_urls = get_url_reports(workspace_key, regex_pattern)

    if not report_urls:
        return {}

    return cast("dict", read_report(workspace_key, report_urls[0]))
