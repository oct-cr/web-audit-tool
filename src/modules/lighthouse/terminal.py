from rich.table import Table
from rich.text import Text

from .audits import get_audit_display_value, get_score_status
from .insights import get_summary_columns


icons = {
    "0": "•",
    "1": "✔",
    "2": "⚠",
    "3": "✖",
}


def get_text_with_status_color(text, status):
    return Text(text, style=get_color_from_status(status))


def get_status_icon(status):
    return get_text_with_status_color(
        icons.get(str(status), "•"),
        status,
    )


def get_color_from_status(status):
    if status is None:
        return "grey50"
    try:
        s = int(status)
    except Exception:
        return "grey50"

    if s == 1:
        return "green"
    if s == 2:
        return "yellow"
    if s == 3:
        return "red"

    return "grey50"


def get_audit_text(audit):
    if not audit:
        return

    status = get_score_status(audit.get("score"))
    icon = get_status_icon(status)

    title_text = Text()
    title_text.append(icon)
    title_text.append(" ")
    title_text.append(audit.get("title") or "")

    value = get_audit_display_value(audit)

    if value:
        val_text = Text(' ' + str(value), style=get_color_from_status(None))
        title_text.append(val_text)
        return title_text

    return title_text


def get_summary_table(rows, columns=None) -> Table:
    if columns is None:
        columns = get_summary_columns()

    table = Table(show_header=True, header_style="bold cyan")
    for key, col_label in columns.items():
        justify = "left" if key == "url" else "right"
        table.add_column(col_label, overflow="fold", justify=justify)

    for s in rows:
        row = []
        for col_key in columns:
            cell = s.get(col_key, None)

            if isinstance(cell, tuple):
                row.append(Text(cell[0], style=get_color_from_status(cell[1])))
            else:
                row.append(cell or "")

        table.add_row(*row)

    return table
