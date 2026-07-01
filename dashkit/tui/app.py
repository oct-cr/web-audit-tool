from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, ListView, Static

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

    BINDINGS: ClassVar = [
        ("c", "toggle_compare", "Compare"),
        ("w", "prev_site", "Prev site"),
        ("s", "next_site", "Next site"),
        ("a", "cursor_up", "Up"),
        ("d", "cursor_down", "Down"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, workspace, initial_route: str | None = None, **kwargs) -> None:
        self.workspace = workspace
        self.sidebar_items = get_sidebar_items(self.workspace.get("sites", {}))
        self.initial_route = initial_route
        self.compare_mode = False

        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Horizontal(id="main"):
            yield Sidebar(items=self.sidebar_items, id="sidebar")
            yield Static(id="body")

        yield Footer()

    def on_mount(self) -> None:
        self.menu = self.query_one("#sidebar", Sidebar)
        self.body = self.query_one("#body", Static)

        self.menu.select_route(self.initial_route)
        self._sync()

    def _sync(self) -> None:
        route = self.menu.current_route
        compare = self.compare_mode and self.menu.current_type == "page"

        try:
            view = get_view_by_route(route, self.workspace, compare=compare)
            self.body.update(get_rendered_view(view))
        except ValueError:
            self.body.update(f"[bold green]{route}[/bold green]\n\nq to quit")

    def on_list_view_highlighted(self, _event: ListView.Highlighted) -> None:
        self._sync()

    def action_toggle_compare(self) -> None:
        self.compare_mode = not self.compare_mode
        self._sync()

    def action_prev_site(self) -> None:
        self.menu.jump_to_site(-1)

    def action_next_site(self) -> None:
        self.menu.jump_to_site(1)

    def action_cursor_up(self) -> None:
        self.menu.action_cursor_up()

    def action_cursor_down(self) -> None:
        self.menu.action_cursor_down()
