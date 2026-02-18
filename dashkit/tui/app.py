from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, ListView, Static

from dashkit.framework.views import get_rendered_view

from ..views.factory import get_view_by_route
from .parsers import get_sidebar_items
from .sidebar import Sidebar


class DashkitApp(App):
    TITLE = "Dashkit"
    CSS = """
    #main { height: 1fr; }

    #sidebar {
        width: 24;
    }

    #body {
        width: 1fr;
        padding: 0 0 0 1;
    }
    """

    def __init__(self, workspace, initial_route: str | None = None, **kwargs) -> None:
        self.workspace = workspace
        self.sidebar_items = get_sidebar_items(self.workspace.get("sites", {}))
        self.initial_route = initial_route

        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Horizontal(id="main"):
            yield Sidebar(items=self.sidebar_items, id="sidebar")
            yield Static(id="body")

    def on_mount(self) -> None:
        self.menu = self.query_one("#sidebar", Sidebar)
        self.body = self.query_one("#body", Static)

        self.menu.select_route(self.initial_route)
        self._sync()

    def _sync(self) -> None:
        route = self.menu.current_route

        try:
            view = get_view_by_route(route, self.workspace)
            self.body.update(get_rendered_view(view))
        except ValueError:
            self.body.update(f"[bold green]{route}[/bold green]\n\nq to quit")

    def on_list_view_highlighted(self, _event: ListView.Highlighted) -> None:
        self._sync()

    def on_key(self, event) -> None:
        match event.key:
            case "q":
                self.exit()
            case "w":
                self.menu.jump_to_site(-1)
            case "s":
                self.menu.jump_to_site(1)
            case "a":
                self.menu.action_cursor_up()
            case "d":
                self.menu.action_cursor_down()
