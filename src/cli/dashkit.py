from ..dashkit.app import DashkitApp
from ..services.workspaces import load_sites


def run_dashkit() -> int:
    workspace = load_sites("sites.yaml")
    DashkitApp(workspace).run()
    return 0
