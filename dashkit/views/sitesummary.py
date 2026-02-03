from dashkit.framework.presenters.occurrences_tables import get_occurrence_table
from dashkit.framework.utils import get_occurrences
from dashkit.modules.lighthouse.config import get_summary_columns
from rich.console import Group
from rich.rule import Rule

from ..modules.lighthouse.widgets import get_metrics_summary_widget, get_third_party_widget
from ..services.reports import get_url_reports, read_report
from ..services.workspaces import get_site_pages


def get_site_summary(site: dict) -> list:
    reports = []
    scripts = []

    page_labels = []

    for page in get_site_pages(site):
        report_urls = get_url_reports(page.get("url"))

        if not report_urls:
            continue

        report = read_report(report_urls[0])
        reports.append(report)

        page_labels.append(page.get("label"))

        url_scripts, _ = get_third_party_widget(report)
        script_labels = [script.get("label") for script in url_scripts]
        scripts.append(script_labels)

    if not reports:
        return []

    script_occurrences = get_occurrences(scripts)
    metrics_data, get_summary_table = get_metrics_summary_widget(reports)

    metrics_data_labeled = []
    for i, data in enumerate(metrics_data):
        label = page_labels[i] if i < len(page_labels) else f"Page {i + 1}"
        metrics_data_labeled.append({"label": label, **data})

    return [
        (metrics_data_labeled, _get_metrics_table_with_labels(get_summary_table)),
        (script_occurrences, _get_renderer_with_title("Third Party Scripts", get_occurrence_table)),
    ]


def _get_metrics_table_with_labels(wrapped_renderer):
    columns = get_summary_columns()
    del columns["url"]
    columns = {"label": "Page", **columns}
    return lambda input: wrapped_renderer(input, columns=columns)


def _get_renderer_with_title(title, wrapped_renderer):
    return lambda input: Group(
        Rule(
            f"[yellow]{title}[/yellow]",
            align="left",
            style="dim",
        ),
        wrapped_renderer(input),
    )
