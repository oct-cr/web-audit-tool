import os
from typing import cast

import yaml

workspaces_base = "workspaces"


def load_workspace(workspace_key: str):
    workspace_path = os.path.join(workspaces_base, f"{workspace_key}.yaml")

    with open(workspace_path) as f:
        workspace = yaml.safe_load(f)

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
