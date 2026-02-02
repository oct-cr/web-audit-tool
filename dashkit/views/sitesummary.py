from dashkit.framework.presenters.occurrences_tables import get_occurrence_table
from dashkit.framework.utils import get_occurrences
from rich.console import Group
from rich.rule import Rule

from ..modules.lighthouse.widgets import get_metrics_summary_widget, get_third_party_widget
from ..services.reports import get_url_reports, read_report
from ..services.workspaces import get_site_urls


def get_site_summary(site: dict) -> list:
    reports = []
    scripts = []

    for url in get_site_urls(site):
        report_urls = get_url_reports(url)

        if not report_urls:
            continue

        report = read_report(report_urls[0])
        reports.append(report)

        url_scripts, _ = get_third_party_widget(report)
        script_labels = [script.get("label") for script in url_scripts]

        scripts.append(script_labels)

    if not reports:
        return []

    script_occurrences = get_occurrences(scripts)

    return [
        get_metrics_summary_widget(reports),
        (script_occurrences, _get_renderer_with_title("Third Party Scripts", get_occurrence_table)),
    ]


def _get_renderer_with_title(title, wrapped_renderer):
    return lambda input: Group(
        Rule(
            f"[yellow]{title}[/yellow]",
            align="left",
            style="dim",
        ),
        wrapped_renderer(input),
    )
