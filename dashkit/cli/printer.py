from rich.console import Console

from ..framework.views import get_rendered_view
from ..services.workspaces import load_sites
from ..views.factory import get_view_by_route


def run_print(route: str) -> int:
    workspace = load_sites("sites.yaml")
    console = Console()

    try:
        data = get_view_by_route(route, workspace)
        console.print(get_rendered_view(data))
        return 0
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
