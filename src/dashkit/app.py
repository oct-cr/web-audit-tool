from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, ListView

from .body import Body
from .sidebar import Sidebar
from .parsers import get_sidebar_items


class DashkitApp(App):
    TITLE = "Dashkit"
    CSS = """
    #main { height: 1fr; }

    #sidebar {
        width: 30;
    }

    #body {
        width: 1fr;
        padding: 0 0 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Horizontal(id="main"):
            yield Sidebar(items=self.sidebar_items, id="sidebar")
            yield Body(id="body")

        yield Footer()

    def on_mount(self) -> None:
        self.menu = self.query_one("#sidebar", Sidebar)
        self.body = self.query_one("#body", Body)

        self.menu.index = 0
        self._sync()

    def __init__(self, workspace, **kwargs) -> None:
        self.workspace = workspace
        self.sidebar_items = get_sidebar_items(self.workspace)

        super().__init__(**kwargs)

    def _sync(self) -> None:
        idx = self.menu.index or 0
        self.body.set_route(self.sidebar_items[idx])

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self._sync()

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()
