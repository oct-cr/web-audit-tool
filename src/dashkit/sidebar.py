from typing import Iterable

from rich.text import Text
from textual.widgets import ListView, ListItem, Label


class Sidebar(ListView):
    def __init__(self, items: Iterable[dict], **kwargs) -> None:
        children = []

        for item in list(items):
            indentation = item.get("command", "").count(":")

            text = item["label"]

            if indentation == 1:
                styled = Text("  " + text)
            else:
                styled = Text(text, style="cyan bold")

            item = ListItem(Label(styled))

            children.append(item)

        super().__init__(*children, **kwargs)
