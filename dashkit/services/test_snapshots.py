import json
from pathlib import Path

from . import snapshots


def test_get_lighthouse_reports_returns_snapshots_newest_first(
    monkeypatch, tmp_path: Path
) -> None:
    workspace_key = "test-workspace"
    workspace_path = tmp_path / workspace_key
    workspace_path.mkdir()

    reports = {
        "20261013_090000": {"id": "first"},
        "20261012_090000": {"id": "earlier"},
        "20261014_090000": {"id": "latest"},
    }
    for timestamp, report in reports.items():
        report_path = workspace_path / f"lhr-site-page-mobile-{timestamp}.json"
        report_path.write_text(json.dumps(report), encoding="utf-8")

    monkeypatch.setattr(snapshots, "workspaces_base", str(tmp_path))

    found = snapshots.get_lighthouse_reports(workspace_key, "site", "page")

    assert [timestamp for timestamp, _report in found] == [
        "20261014_090000",
        "20261013_090000",
        "20261012_090000",
    ]
    assert [report["id"] for _timestamp, report in found] == ["latest", "first", "earlier"]
