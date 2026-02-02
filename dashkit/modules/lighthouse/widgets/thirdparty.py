from rich.console import group
from rich.rule import Rule
from rich.text import Text


def get_third_party_widget(report):
    insights = _get_third_party_items(report)

    return insights, lambda input: _get_third_party_view(input)


def _get_third_party_items(report):
    lr = report.get("lighthouseResult", {})
    audits = lr.get("audits", {})
    audit = audits.get("third-parties-insight", {})
    details = audit.get("details", {})
    raw_items = details.get("items", [])

    items = []
    for item in raw_items:
        items.append(
            {
                "label": item.get("entity"),
                "mainThreadTime": item.get("mainThreadTime"),
            }
        )

    return sorted(items, key=lambda x: (x.get("label") or "").lower())


@group()
def _get_third_party_view(items: list):
    if not items:
        return

    yield Rule(
        f"[yellow]3rd-Party Scripts[/yellow] {len(items)}",
        align="left",
        style="dim",
    )

    labels = [f"{item.get('label')}" for item in items]

    yield Text.from_markup(" [dim]|[/dim] ".join(labels))
