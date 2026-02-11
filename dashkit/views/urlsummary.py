from rich.text import Text

from ..modules.lighthouse.config import get_summary_columns
from ..modules.lighthouse.widgets import (
    get_audits_widget,
    get_metrics_summary_widget,
)
from ..services.snapshots import get_latest_lighthouse_report


def get_url_summary(workspace_key: str, page: dict) -> list:
    page_key = page.get("key", "")
    site_key = page.get("site_key", "")

    report = get_latest_lighthouse_report(workspace_key, site_key, page_key)
    if not report:
        return []

    metrics_data, get_summary_table = get_metrics_summary_widget([report])

    return [
        (f"Snapshot: {page_key}", Text),
        (metrics_data, _get_metrics_table_with_labels(get_summary_table)),
        get_audits_widget(report),
    ]


def _get_metrics_table_with_labels(wrapped_renderer):
    columns = get_summary_columns()
    del columns["url"]
    return lambda input: wrapped_renderer(input, columns=columns)
