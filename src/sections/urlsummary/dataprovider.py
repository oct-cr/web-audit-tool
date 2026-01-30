from modules.lighthouse.categories import get_relevant_audits
from modules.lighthouse.insights import get_insights_summary
from services.reports import get_url_reports, read_report


def get_url_summary(url):
    report_urls = get_url_reports(url)

    if not report_urls:
        return {}

    report = read_report(report_urls[0])

    return {
        "lighthouse_summary_rows": get_insights_summary(report),
        "audits": get_relevant_audits(report),
    }
