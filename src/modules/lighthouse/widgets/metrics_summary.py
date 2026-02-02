from rich.console import group
from rich.table import Table
from rich.text import Text

from ....framework.status import get_color_from_status
from ..audits import get_audit_display_value, get_score_status
from ..config import get_summary_columns, metrics


def get_metrics_summary_widget(reports: list):
    rows = []
    for report in reports:
        row = _get_insights_row(report)
        if row:
            rows.append(row)

    return rows, lambda input: _get_metrics_summary_view(input)


def _get_insights_row(report: dict) -> dict:
    lhr = report.get("lighthouseResult", {})
    audits = lhr.get("audits", {})
    categories = lhr.get("categories", {})

    row: dict = {
        "url": lhr.get("requestedUrl"),
    }

    for key, category in categories.items():
        score = category.get("score", 0)
        status = get_score_status(score)
        row[key] = (f"{score * 100:.0f}", status)

    for key in metrics:
        audit = audits.get(key)
        if not audit:
            continue

        status = get_score_status(audit.get("score"))
        row[key] = (get_audit_display_value(audit), status)

    return row


def _get_summary_table(rows: list, columns=None) -> Table:
    if columns is None:
        columns = get_summary_columns()

    table = Table(show_header=True, header_style="bold cyan")
    for key, col_label in columns.items():
        if key == "url":
            table.add_column(col_label, overflow="fold", justify="left")
        else:
            table.add_column(col_label, overflow="fold", justify="right")

    for s in rows:
        row = []
        for col_key in columns:
            cell = s.get(col_key, "")

            if isinstance(cell, tuple):
                row.append(Text(cell[0], style=get_color_from_status(cell[1])))
            else:
                row.append(cell)

        table.add_row(*row)

    return table


@group()
def _get_metrics_summary_view(rows: list):
    if not rows:
        return

    yield _get_summary_table(rows)
