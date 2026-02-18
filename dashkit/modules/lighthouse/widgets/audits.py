from rich.console import group
from rich.rule import Rule
from rich.text import Text

from ....framework.status import get_color_from_status, get_status_icon
from ..audits import get_audit_display_value, get_audits_sorted_by_savings, get_score_status
from ..categories import get_relevant_category_audits


def get_audits_widget(report: dict):
    audits = _get_relevant_audits(report)

    return audits, _get_audits_view


def _get_relevant_audits(report):
    lr = report.get("lighthouseResult", {})
    audits = lr.get("audits", {})
    categories = lr.get("categories", {})

    relevant_audits = []

    for category in categories.values():
        category_audits = get_relevant_category_audits(audits, category)

        if category.get("id") == "performance":
            category_audits = get_audits_sorted_by_savings(category_audits)

        relevant_audits.append(
            {
                "label": category.get("title"),
                "audits": category_audits,
            }
        )

    return relevant_audits


@group()
def _get_audits_view(audits: list):
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

        last_metric_saving_count = None

        for audit in category_audits:
            metric_savings = audit.get("metricSavings")

            if isinstance(metric_savings, dict):
                filtered_savings = [m for m, v in metric_savings.items() if v != 0]
                metric_saving_count = len(filtered_savings)
            else:
                metric_saving_count = None

            if (
                last_metric_saving_count is not None
                and last_metric_saving_count != 0
                and metric_saving_count != last_metric_saving_count
            ):
                yield Text()

            last_metric_saving_count = metric_saving_count

            yield _get_audit_text(audit, 1 if (metric_saving_count == 1) else 0)

            if metric_saving_count and (metric_saving_count > 1):
                yield Text("  Affects: " + ", ".join(filtered_savings), style="dim")


def _get_audit_text(audit, indent=0):
    if not audit:
        return

    status = get_score_status(audit.get("score"))
    icon = get_status_icon(status)

    title_text = Text("  " * indent)
    title_text.append(icon)
    title_text.append(" ")
    title_text.append(audit.get("title") or "")

    value = get_audit_display_value(audit)

    if value:
        val_text = Text(" " + str(value), style=get_color_from_status(None))
        title_text.append(val_text)
        return title_text

    return title_text
