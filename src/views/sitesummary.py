from ..modules.lighthouse.widgets import get_metrics_summary_widget
from ..services.reports import get_url_reports, read_report
from ..services.workspaces import get_site_urls


def get_site_summary(site: dict) -> list:
    reports = []

    for url in get_site_urls(site):
        report_urls = get_url_reports(url)

        if not report_urls:
            continue

        reports.append(read_report(report_urls[0]))

    if not reports:
        return []

    return [
        get_metrics_summary_widget(reports),
    ]
