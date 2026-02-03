from dashkit.framework.presenters.occurrences_tables import get_occurrence_table
from dashkit.framework.utils import get_occurrences
from dashkit.modules.lighthouse.config import get_summary_columns
from rich.console import Group
from rich.rule import Rule
from rich.text import Text

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

    view = [
        (metrics_data_labeled, _get_metrics_table_with_labels(get_summary_table)),
    ]

    if len(script_occurrences["discrepancies"]) > 0:
        view.append(
            (
                script_occurrences["discrepancies"],
                _get_renderer_with_title(
                    f"Third Party Scripts - Discrepancies ["
                    f"{len(script_occurrences['discrepancies'])}]",
                    get_occurrence_table,
                ),
            )
        )

    if len(script_occurrences["common"]) > 0:
        view.append(
            (
                script_occurrences["common"],
                _get_renderer_with_title(
                    f"Third Party Scripts - Common [{len(script_occurrences['common'])}]",
                    _get_inline_list,
                ),
            )
        )

    return view


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


def _get_inline_list(labels):
    return Text.from_markup(" [dim]|[/dim] ".join(labels))
