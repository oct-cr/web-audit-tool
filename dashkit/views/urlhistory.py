from datetime import datetime

from rich.text import Text

from ..modules.lighthouse.config import categories, metrics
from ..modules.lighthouse.widgets import get_metrics_summary_widget
from ..services.snapshots import get_lighthouse_reports


def get_url_history(workspace_key: str, page: dict) -> list:
    page_key = str(page.get("key", ""))
    site_key = str(page.get("site_key", ""))
    snapshots = get_lighthouse_reports(workspace_key, site_key, page_key)

    if not snapshots:
        return [(f"No saved snapshots for {page_key}.", Text)]

    timestamps, reports = zip(*snapshots, strict=True)
    metric_rows, get_summary_table = get_metrics_summary_widget(list(reports))
    history_rows = [
        {"timestamp": _format_timestamp(timestamp), **metric_row}
        for timestamp, metric_row in zip(timestamps, metric_rows, strict=True)
    ]
    columns = {"timestamp": "Date", **categories, **metrics}

    return [
        (f"Performance History: {page_key}", Text),
        (history_rows, lambda rows: get_summary_table(rows, columns=columns)),
    ]


def _format_timestamp(timestamp: str) -> str:
    return datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M")
