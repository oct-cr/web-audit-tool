from ..tui.app import DashkitApp


def run_tui(workspace, route: str | None = None) -> int:
    DashkitApp(workspace, initial_route=route).run()
    return 0
