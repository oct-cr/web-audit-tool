from modules.lighthouse.insights import get_insights_summary
from services.reports import get_url_reports, read_report
from services.workspaces import get_site_urls


def get_site_summary(site):
    rows = []

    for url in get_site_urls(site):
        report_urls = get_url_reports(url)
        if not report_urls:
            continue

        report = read_report(report_urls[0])
        rows.append(get_insights_summary(report))

    return {"lighthouse_summary_rows": rows}
