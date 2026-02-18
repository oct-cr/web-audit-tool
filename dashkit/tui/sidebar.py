from rich.text import Text
from textual.widgets import Label, ListItem, ListView


class Sidebar(ListView):
    def __init__(self, items: list[dict], **kwargs) -> None:
        self.items = list(items)
        children = []

        for item in self.items:
            text = item["label"]
            is_page = item.get("type") == "page"
            styled = Text("  " + text) if is_page else Text(text, style="cyan bold")
            children.append(ListItem(Label(styled)))

        super().__init__(*children, **kwargs)

    @property
    def current_route(self) -> str:
        idx = self.index or 0
        return str(self.items[idx].get("command", ""))

    def select_route(self, route: str | None) -> None:
        if not route:
            self.index = 0
            return
        for idx, item in enumerate(self.items):
            if route in item.get("command", ""):
                self.index = idx
                return
        self.index = 0

    def jump_to_site(self, direction: int) -> None:
        current = self.index or 0
        idx = current + direction
        while 0 <= idx < len(self.items):
            if self.items[idx].get("type") == "site":
                self.index = idx
                return
            idx += direction
