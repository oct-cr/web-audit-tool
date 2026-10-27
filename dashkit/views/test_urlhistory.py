from dashkit.views import urlhistory
from rich.console import Console


def _report(performance: float, accessibility: float) -> dict:
    return {
        "lighthouseResult": {
            "requestedUrl": "https://example.test",
            "categories": {
                "performance": {"score": performance},
                "accessibility": {"score": accessibility},
                "best-practices": {"score": 0.9},
                "seo": {"score": 1.0},
            },
            "audits": {},
        }
    }


def test_get_url_history_renders_newest_snapshot_first(monkeypatch) -> None:
    monkeypatch.setattr(
        urlhistory,
        "get_lighthouse_reports",
        lambda _workspace, _site, _page: [
            ("20261013_090000", _report(0.8, 0.9)),
            ("20261012_090000", _report(0.5, 0.6)),
        ],
    )

    view = urlhistory.get_url_history("workspace", {"site_key": "site", "key": "page"})
    table = view[1][1](view[1][0])
    console = Console(record=True, width=200)
    console.print(table)

    output = console.export_text()

    assert "Date" in output
    assert "Performance" in output
    assert "FCP" in output
    assert "LCP" in output
    assert "TTI" in output
    assert "TBT" in output
    assert "CLS" in output
    assert "2026-10-13 09:00" in output
    assert "09:00:00" not in output
    assert output.index("2026-10-13 09:00") < output.index("2026-10-12 09:00")


def test_get_url_history_reports_an_empty_state(monkeypatch) -> None:
    monkeypatch.setattr(urlhistory, "get_lighthouse_reports", lambda *_args: [])

    view = urlhistory.get_url_history("workspace", {"site_key": "site", "key": "page"})

    assert view[0][0] == "No saved snapshots for page."
