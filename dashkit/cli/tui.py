from ..services.workspaces import load_sites
from ..tui.app import DashkitApp


def run_tui(route: str | None = None) -> int:
    workspace = load_sites("sites.yaml")
    DashkitApp(workspace, initial_route=route).run()
    return 0
