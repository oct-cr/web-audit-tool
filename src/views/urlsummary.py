from rich.console import group
from rich.rule import Rule
from rich.text import Text

from ..modules.lighthouse.providers import get_insights_row, get_relevant_audits
from ..modules.lighthouse.views import get_audit_text, get_summary_table

from ..services.reports import get_url_reports, read_report


def get_url_summary(url: str) -> dict:
    report_urls = get_url_reports(url)

    if not report_urls:
        return {}

    report = read_report(report_urls[0])

    return {
        "lighthouse_summary_rows": get_insights_row(report),
        "audits": get_relevant_audits(report),
    }


@group()
def get_url_summary_view(url_summary: dict):
    lighthouse_rows = url_summary.get("lighthouse_summary_rows")

    if lighthouse_rows:
        yield get_summary_table([lighthouse_rows])

    audits = url_summary.get("audits", [])
    if audits:
        yield from get_audits_view(audits)


def get_audits_view(audits: list):
    for category in audits:
        category_audits = category.get("audits", [])

        if not category_audits:
            continue

        yield Text()
        yield Rule(
            f"[cyan]{category.get('label')}[/cyan] {len(category_audits)}",
            align="left",
            style="dim",
        )

        for audit in category_audits:
            yield get_audit_text(audit)
