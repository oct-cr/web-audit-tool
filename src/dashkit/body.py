from time import ctime

from textual.widgets import Static


class Body(Static):
    def set_route(self, route: str) -> None:
        self.update(f"[bold green]{route}[/bold green]\n\n{ctime()}\n\nq to quit")
