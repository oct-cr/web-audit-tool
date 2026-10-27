from datetime import datetime
from urllib.parse import urlparse

from rich.text import Text

from ..modules.lighthouse.config import get_summary_columns
from ..modules.lighthouse.widgets import (
    get_audits_widget,
    get_metrics_summary_widget,
)
from ..services.snapshots import get_recent_lighthouse_reports


def get_url_summary(workspace_key: str, page: dict) -> list:
    page_key = page.get("key", "")
    site_key = page.get("site_key", "")

    results = get_recent_lighthouse_reports(workspace_key, site_key, page_key, n=1)
    if not results:
        return []

    ts, report = results[0]
    url = _strip_url(report.get("lighthouseResult", {}).get("requestedUrl", ""))
    date = _format_timestamp(ts) if ts else ""

    parts = [f"Snapshot: {page_key}"]
    if url:
        parts.append(url)
    if date:
        parts.append(date)
    header = "  ·  ".join(parts)

    metrics_data, get_summary_table = get_metrics_summary_widget([report])

    return [
        (header, Text),
        (metrics_data, _get_metrics_table_with_labels(get_summary_table)),
        get_audits_widget(report),
    ]


def _strip_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.removeprefix("www.")
    return host + parsed.path.rstrip("/") if parsed.path != "/" else host


def _format_timestamp(timestamp: str) -> str:
    return datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M")


def _get_metrics_table_with_labels(wrapped_renderer):
    columns = get_summary_columns()
    del columns["url"]
    return lambda input: wrapped_renderer(input, columns=columns)
