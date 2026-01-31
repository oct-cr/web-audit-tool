from textual.widgets import Static

from ..services.workspaces import get_node_by_path
from ..sections.sitesummary.dataprovider import get_site_summary
from ..sections.sitesummary.view import get_site_summary_view
from ..sections.urlsummary.dataprovider import get_url_summary
from ..sections.urlsummary.view import get_url_summary_view


class Body(Static):
    def __init__(self, sites, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sites = sites

    def set_route(self, page: str) -> None:
        node = get_node_by_path(self.sites, page.get("command", ""))

        if not node:
            self.update(f"[bold green]{page}[/bold green]\n\nq to quit")
            return

        if node.get("node_type") == "site":
            site_summary = get_site_summary(node)
            self.update(get_site_summary_view(site_summary))
            return

        if node.get("node_type") == "page":
            url_summary = get_url_summary(node.get("url"))
            self.update(get_url_summary_view(url_summary))
            return
