from pathlib import Path

import pytest

from .workspaces import get_node_by_path, load_workspace

site_keys = {"sciencenews", "itsfoss"}
page_keys = {"frontpage", "collection", "page"}


def test_demo_workspace_contract() -> None:
    workspace = load_workspace("demo")

    assert workspace["key"] == "demo"
    assert set(workspace["sites"]) == site_keys

    for site_key, site in workspace["sites"].items():
        assert set(site["pages"]) == page_keys
        assert get_node_by_path(workspace, site_key) is not None

        for page_key, page in site["pages"].items():
            assert page["url"].startswith("https://")
            assert get_node_by_path(workspace, f"{site_key}:{page_key}") is not None


def test_demo_workspace_loads_outside_repository(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)

    workspace = load_workspace("demo")

    assert set(workspace["sites"]) == site_keys
