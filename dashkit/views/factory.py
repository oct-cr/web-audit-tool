from ..services.workspaces import get_node_by_path
from .sitesummary import get_site_summary
from .urlsummary import get_url_summary


def get_view_by_route(route: str, workspace: dict) -> list:
    node = get_node_by_path(workspace, route)
    workspace_key = workspace.get("key", "")

    if not node:
        raise ValueError(f"Route {route} not found in workspace")


    if node.get("node_type") == "site":
        return get_site_summary(workspace_key, node)

    if node.get("node_type") == "page":
        return get_url_summary(workspace_key, node)

    raise ValueError(f"Unknown route type for {route}")
