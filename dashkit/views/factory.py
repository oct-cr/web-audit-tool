from ..services.workspaces import get_node_by_path
from .sitesummary import get_site_summary
from .urlcompare import get_url_compare
from .urlhistory import get_url_history
from .urlsummary import get_url_summary


def get_view_by_route(
    route: str, workspace: dict, compare: bool = False, history: bool = False
) -> list:
    node = get_node_by_path(workspace, route)
    workspace_key = workspace.get("key", "")

    if not node:
        raise ValueError(f"Route {route} not found in workspace")


    if node.get("node_type") == "site":
        return get_site_summary(workspace_key, node)

    if node.get("node_type") == "page":
        if history:
            return get_url_history(workspace_key, node)
        if compare:
            return get_url_compare(workspace_key, node)
        return get_url_summary(workspace_key, node)

    raise ValueError(f"Unknown route type for {route}")
