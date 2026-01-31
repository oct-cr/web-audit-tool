from collections.abc import Callable
from typing import Any

from ..services.workspaces import get_node_by_path
from ..sections.sitesummary.dataprovider import get_site_summary
from ..sections.sitesummary.view import get_site_summary_view
from ..sections.urlsummary.dataprovider import get_url_summary
from ..sections.urlsummary.view import get_url_summary_view


def get_view_by_route(route: str, workspace: dict) -> tuple[Any, Callable]:
    node = get_node_by_path(workspace, route)

    if not node:
        raise ValueError(f"Route {route} not found in workspace")

    if node.get("node_type") == "site":
        return get_site_summary(node), get_site_summary_view

    if node.get("node_type") == "page":
        return get_url_summary(node.get("url")), get_url_summary_view

    raise ValueError(f"Unknown route type for {route}")
