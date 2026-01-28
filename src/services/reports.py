import json
import re
import os
from datetime import datetime

from helpers.filenames import get_filename_from_url


report_folder = "reports"


def write_report(url, report):
    name = get_filename_from_url(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(report_folder, f"{name}-{timestamp}.json")

    with open(out_path, "wb") as f:
        f.write(report)

    return out_path


def read_report(filename):
    path = os.path.join(report_folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_url_reports(url):
    latest = {}

    for root, _, files in os.walk(report_folder):
        rel_root = os.path.relpath(root, report_folder)

        for f in files:
            if not f.lower().endswith(".json"):
                continue

            rel_path = os.path.join(rel_root, f) if rel_root != os.curdir else f

            # filename pattern: <base>-YYYYMMDD_HHMMSS.json
            m = re.match(r"^(?P<base>.+)-(?P<ts>\d{8}_\d{6})\.json$", f)

            if not m:
                continue

            base = m.group("base")

            if base != get_filename_from_url(url):
                continue

            ts = m.group("ts")

            # use base plus relative root to avoid collisions across folders
            key = os.path.join(rel_root, base) if rel_root != os.curdir else base

            prev = latest.get(key)
            # choose file with lexicographically greatest timestamp (newer)
            if prev is None or (ts and (not prev[0] or ts > prev[0])):
                latest[key] = (ts, rel_path)

    results = [v[1] for v in latest.values()]

    return results
