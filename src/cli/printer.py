from rich.console import Console

from ..views.factory import get_view_by_route
from ..services.workspaces import load_sites


def run_print(route: str) -> int:
    workspace = load_sites("sites.yaml")
    console = Console()

    try:
        data, view_fn = get_view_by_route(route, workspace)
        console.print(view_fn(data))
        return 0
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
