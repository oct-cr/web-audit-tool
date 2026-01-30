from rich.console import group
from rich.rule import Rule
from rich.text import Text

from modules.lighthouse.terminal import get_summary_table, get_audit_text


@group()
def get_url_summary_view(url_summary):
    lighthouse_rows = url_summary.get("lighthouse_summary_rows")

    if lighthouse_rows:
        yield get_summary_table([lighthouse_rows])
        
    audits = url_summary.get("audits", [])
    if audits:
        yield from get_audits_view(audits)


def get_audits_view(audits):
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
