from ..dashkit.app import DashkitApp
from ..services.workspaces import load_sites


def run_dashkit(route: str | None = None) -> int:
    workspace = load_sites("sites.yaml")
    DashkitApp(workspace, initial_route=route).run()
    return 0
