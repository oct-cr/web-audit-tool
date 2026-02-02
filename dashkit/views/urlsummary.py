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

    return [
        get_metrics_summary_widget([report]),
        get_third_party_widget(report),
        get_audits_widget(report),
    ]
