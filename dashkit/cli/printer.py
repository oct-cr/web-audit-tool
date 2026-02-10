from rich.console import Console

from ..framework.views import get_rendered_view
from ..views.factory import get_view_by_route


def run_print(workspace, route: str) -> int:
    console = Console()

    try:
        data = get_view_by_route(route, workspace)
        console.print(get_rendered_view(data))
        return 0
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
