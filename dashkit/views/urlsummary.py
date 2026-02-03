from rich.text import Text

from ..modules.lighthouse.config import get_summary_columns
from ..modules.lighthouse.widgets import (
    get_audits_widget,
    get_metrics_summary_widget,
    get_third_party_widget,
)
from ..services.reports import get_url_reports, read_report


def get_url_summary(url: str) -> list:
    report_urls = get_url_reports(url)

    if not report_urls:
        return []

    report = read_report(report_urls[0])

    metrics_data, get_summary_table = get_metrics_summary_widget([report])

    return [
        (f"URL: {url}", Text),
        (metrics_data, _get_metrics_table_with_labels(get_summary_table)),
        get_third_party_widget(report),
        get_audits_widget(report),
    ]


def _get_metrics_table_with_labels(wrapped_renderer):
    columns = get_summary_columns()
    del columns["url"]
    return lambda input: wrapped_renderer(input, columns=columns)
