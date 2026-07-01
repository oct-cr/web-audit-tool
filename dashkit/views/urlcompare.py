from rich.console import Group
from rich.rule import Rule
from rich.text import Text

from ..modules.lighthouse.compare import (
    diff_audits,
    diff_metrics,
    diff_thirdparty,
)
from ..modules.lighthouse.widgets import (
    get_audit_changes_widget,
    get_compare_metrics_widget,
)
from ..services.snapshots import get_recent_lighthouse_reports


def get_url_compare(workspace_key: str, page: dict) -> list:
    page_key = page.get("key", "")
    site_key = page.get("site_key", "")

    recent = get_recent_lighthouse_reports(workspace_key, site_key, page_key, n=2)

    if len(recent) < 2:
        return [
            (
                Text(
                    "Only one snapshot — run another audit to compare.",
                    style="dim",
                ),
                lambda input: input,
            )
        ]

    (cur_ts, current), (base_ts, baseline) = recent[0], recent[1]

    header = Text(
        f"Comparing: {page_key}   {_fmt_ts(base_ts)} → {_fmt_ts(cur_ts)}",
        style="bold steel_blue3",
    )

    view = [
        (header, lambda input: input),
        get_compare_metrics_widget(diff_metrics(current, baseline)),
        get_audit_changes_widget(diff_audits(current, baseline)),
    ]

    thirdparty = diff_thirdparty(current, baseline)
    if thirdparty["added"] or thirdparty["removed"]:
        view.append((thirdparty, _get_thirdparty_changes_view))

    return view


def _fmt_ts(ts: str) -> str:
    """Turn '20260616_125453' into '2026-06-16 12:54'."""
    if not ts or len(ts) < 13:
        return ts or ""
    return f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"


def _get_thirdparty_changes_view(diff: dict):
    lines = []
    for label in diff.get("added", []):
        lines.append(Text(f"+ {label}", style="dark_green"))
    for label in diff.get("removed", []):
        lines.append(Text(f"- {label}", style="deep_pink3"))

    return Group(
        Text(),
        Rule("3rd-Party Scripts — Changed", align="left", style="dim"),
        *lines,
    )
