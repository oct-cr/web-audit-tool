from ..modules.lighthouse.providers import get_insights_row
from ..modules.lighthouse.views import get_summary_table

from ..services.reports import get_url_reports, read_report
from ..services.workspaces import get_site_urls


def get_site_summary(site: dict) -> dict:
    rows = []

    for url in get_site_urls(site):
        report_urls = get_url_reports(url)
        if not report_urls:
            continue

        report = read_report(report_urls[0])
        rows.append(get_insights_row(report))

    return {"lighthouse_summary_rows": rows}


def get_site_summary_view(site_summary: dict):
    return get_summary_table(site_summary["lighthouse_summary_rows"])
