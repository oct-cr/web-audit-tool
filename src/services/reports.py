import json
import os
import re
import urllib.parse

report_folder = "reports"


def write_report(url, key: str, report):
    name = get_filename_from_url(url)
    out_path = os.path.join(report_folder, f"{name}-{key}.json")

    with open(out_path, "wb") as f:
        f.write(report)

    return out_path


def read_report(filename):
    path = os.path.join(report_folder, filename)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_url_reports(url):
    latest = {}

    filebase = get_filename_from_url(url)
    print(filebase)

    for root, _, files in os.walk(report_folder):
        rel_root = os.path.relpath(root, report_folder)

        for f in files:
            if not f.lower().endswith(".json"):
                continue

            rel_path = os.path.join(rel_root, f) if rel_root != os.curdir else f

            pattern = rf"^{re.escape(filebase)}-desktop-(?P<ts>\d{{8}}_\d{{6}})\.json$"
            m = re.match(pattern, f)

            if not m:
                continue

            ts = m.group("ts")

            key = os.path.join(rel_root, filebase) if rel_root != os.curdir else filebase

            prev = latest.get(key)

            if prev is None or (ts and (not prev[0] or ts > prev[0])):
                latest[key] = (ts, rel_path)

    results = [v[1] for v in latest.values()]

    return results


def get_filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    base = (parsed.netloc or "") + (parsed.path or "")

    base = re.sub(r"^https?://", "", base)
    name = re.sub(r"[^A-Za-z0-9_-]+", "-", base).strip("-")

    return name
