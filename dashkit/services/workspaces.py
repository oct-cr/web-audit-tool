from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, cast

import yaml

workspaces_base = "workspaces"


def _get_workspace_file(workspace_key: str) -> Path | Traversable:
    workspace_path = Path(workspaces_base, f"{workspace_key}.yaml")
    if workspace_path.is_file() or workspace_key != "demo":
        return workspace_path

    bundled_workspace = files("dashkit").joinpath("workspaces").joinpath("demo.yaml")
    if bundled_workspace.is_file():
        return bundled_workspace

    return Path(__file__).resolve().parents[2] / workspace_path


def load_workspace(workspace_key: str) -> dict[str, Any]:
    workspace_file = _get_workspace_file(workspace_key)
    with workspace_file.open(encoding="utf-8") as workspace_stream:
        workspace = cast("dict[str, Any]", yaml.safe_load(workspace_stream))

    workspace["key"] = workspace_key
    return workspace


def find_site(workspace, key: str) -> dict:
    site = workspace.get("sites", {}).get(key)
    if not site:
        raise ValueError(f"Site not found for key: {key}")

    return cast("dict", site)


def get_site_pages(site) -> list[dict]:
    if not site:
        raise ValueError("Site not found")

    pages_list: list[dict] = []

    pages = site.get("pages", {})
    for page_key, page in pages.items():
        pages_list.append(
            {
                **page,
                "key": page_key,
                "label": page.get("label", str(page_key).capitalize()),
            }
        )

    return pages_list


def get_node_by_path(workspace, path):
    parts = path.split(":", 1)
    site_key = parts[0]
    page_key = parts[1] if len(parts) > 1 else None

    site = find_site(workspace, site_key)
    if site is None:
        return None

    if page_key is None:
        return {
            **site,
            "node_type": "site",
            "key": site_key,
        }

    pages = site.get("pages", {})
    page = pages.get(page_key)

    if page:
        return {
            **page,
            "node_type": "page",
            "key": page_key,
            "site_key": site_key,
        }

    return None
