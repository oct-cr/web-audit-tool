from rich.table import Table
from rich.text import Text

from ....framework.status import get_color_from_status
from ..audits import get_audit_display_value, get_score_status
from ..config import categories, get_summary_columns, metrics


def get_metrics_summary_widget(reports: list):
    rows = []
    for report in reports:
        row = _get_insights_row(report)
        if row:
            rows.append(row)

    return rows, _get_summary_table


def _get_insights_row(report: dict) -> dict:
    lhr = report.get("lighthouseResult", {})
    audits = lhr.get("audits", {})
    categories = lhr.get("categories", {})

    row: dict = {
        "url": lhr.get("requestedUrl"),
    }

    for key, category in categories.items():
        score = category.get("score", 0)
        row[key] = (f"{score * 100:.0f}", score)

    for key in metrics:
        audit = audits.get(key)
        if not audit:
            continue

        row[key] = (get_audit_display_value(audit), audit.get("score"))

    return row


def _get_summary_table(rows: list, columns=None) -> Table:
    if columns is None:
        columns = get_summary_columns()

    col_averages = _get_column_average_scores(rows, columns)

    table = Table(show_header=True, header_style="bold steel_blue3", box=None, padding=(0, 2))
    for key, col_label in columns.items():
        header_style = "bold steel_blue3"
        
        if key in col_averages:
            avg_score = col_averages[key]
            avg_status = get_score_status(avg_score)
            header_style = f"bold {get_color_from_status(avg_status)}"
        
        if (key in metrics) or (key in categories):
            table.add_column(col_label, overflow="fold", justify="right", header_style=header_style)
        else:
            table.add_column(col_label, overflow="fold", justify="left", header_style=header_style)

    for s in rows:
        row_avg = _get_row_average_scores(s, columns)
        row_label_style = "steel_blue3"
        
        if row_avg is not None:
            row_status = get_score_status(row_avg)
            row_label_style = get_color_from_status(row_status)
        
        row = []
        for col_key in columns:
            cell = s.get(col_key, "")

            if isinstance(cell, tuple):
                status = get_score_status(cell[1])
                row.append(Text(cell[0], style=get_color_from_status(status)))
            elif col_key == "label" or col_key == "url":
                row.append(Text(str(cell), style=row_label_style))
            else:
                row.append(cell)

        table.add_row(*row)

    return table


def _get_row_average_scores(row: dict, columns: dict) -> float | None:
    category_scores = []
    
    for cat_key in categories:
        if cat_key in columns:
            cell = row.get(cat_key)
            if isinstance(cell, tuple):
                try:
                    score = float(cell[0]) / 100.0
                    category_scores.append(score)
                except (ValueError, TypeError):
                    pass
    
    if not category_scores:
        return None
    
    return round(sum(category_scores) / len(category_scores), 2)


def _get_column_average_scores(rows: list, columns: dict) -> dict:
    col_averages = {}
    
    for col_key in columns:
        scores = []
        for row in rows:
            cell = row.get(col_key)
            if isinstance(cell, tuple):
                score_value = cell[1]
                scores.append(score_value)
        
        if scores:
            col_averages[col_key] = round(sum(scores) / len(scores), 2)
    
    return col_averages
