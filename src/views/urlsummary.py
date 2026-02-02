from rich.console import group
from rich.rule import Rule
from rich.text import Text

from ..modules.lighthouse.providers import (
    get_insights_row,
    get_relevant_audits,
)
from ..modules.lighthouse.views import get_audit_text, get_summary_table
from ..modules.lighthouse.widgets import get_third_party_widget
from ..services.reports import get_url_reports, read_report


def get_url_summary(url: str) -> dict:
    report_urls = get_url_reports(url)

    if not report_urls:
        return {}

    report = read_report(report_urls[0])

    return [
        ([get_insights_row(report)], get_summary_table),
        get_third_party_widget(report),
        (get_relevant_audits(report), get_audits_view),
    ]


@group()
def get_url_summary_view(url_summary: list):
    for widget in url_summary:
        data, view_fn = widget
        yield view_fn(data)


@group()
def get_audits_view(audits: list):
    for category in audits:
        category_audits = category.get("audits", [])

        if not category_audits:
            continue

        yield Text()
        yield Rule(
            f"{category.get('label')} {len(category_audits)}",
            align="left",
            style="dim",
        )

        for audit in category_audits:
            yield get_audit_text(audit)
