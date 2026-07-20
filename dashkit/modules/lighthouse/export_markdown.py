"""Render an agent-ready page report (from ``export.build_page_report``) as Markdown.

Pure string building — no Rich, no I/O. Output is deterministic (stable ordering,
no timestamps in the body beyond the report's own fetch time) so re-runs diff
cleanly. The audit order is already prioritized by ``get_audits_sorted_by_savings``;
here we only bucket audits under a metric heading for scannability.

``metricSavings`` values are milliseconds for LCP/FCP/TBT/INP and a 0-1 shift
score for CLS; units are labelled accordingly.
"""

from .config import categories, metrics

_MS_METRICS = {"LCP", "FCP", "TBT", "INP", "TTI"}
_METRIC_ORDER = (*metrics.values(), "INP")
_OTHER_GROUP = "Other"


def render_page_markdown(page_report: dict) -> str:
    lines: list[str] = []

    url = page_report.get("url") or "(unknown URL)"
    lines.append(f"# Lighthouse Report — {url}")
    lines.append("")
    lines.extend(_render_meta(page_report))
    lines.append("")
    lines.extend(_render_scores(page_report.get("scores") or {}))

    audits = page_report.get("audits") or []
    if not audits:
        lines.append("")
        lines.append("No actionable issues found. 🎉")
        return "\n".join(lines) + "\n"

    for group_label, group_audits in _group_by_metric(audits):
        lines.append("")
        lines.append(f"## {group_label}")
        for audit in group_audits:
            lines.extend(_render_audit(audit))

    return "\n".join(lines) + "\n"


def _render_meta(page_report: dict) -> list[str]:
    lines = []

    form_factor = page_report.get("form_factor")
    if form_factor:
        lines.append(f"- **Form factor:** {form_factor}")

    fetch_time = page_report.get("fetch_time")
    if fetch_time:
        lines.append(f"- **Fetched:** {fetch_time}")

    version = page_report.get("lighthouse_version")
    if version:
        lines.append(f"- **Lighthouse:** {version}")

    for warning in page_report.get("run_warnings") or []:
        lines.append(f"- ⚠️ **Warning:** {warning}")

    return lines


def _render_scores(scores: dict) -> list[str]:
    category_cells = _cells(scores, categories)
    metric_cells = _cells(scores, metrics)

    lines = ["## Scores"]
    if category_cells:
        lines.append("| " + " | ".join(label for label, _ in category_cells) + " |")
        lines.append("| " + " | ".join("---" for _ in category_cells) + " |")
        lines.append("| " + " | ".join(value for _, value in category_cells) + " |")

    if metric_cells:
        lines.append("")
        lines.append(
            "**Core Web Vitals:** "
            + "  ".join(f"{label} {value}" for label, value in metric_cells)
        )

    return lines


def _cells(scores: dict, keys: dict) -> list[tuple[str, str]]:
    cells = []
    for key, label in keys.items():
        cell = scores.get(key)
        if isinstance(cell, tuple):
            display = cell[0]
            cells.append((label, str(display) if display is not None else "—"))
    return cells


def _group_by_metric(audits: list[dict]) -> list[tuple[str, list[dict]]]:
    groups: dict[str, list[dict]] = {}
    order: list[str] = []

    for audit in audits:
        group = _primary_metric(audit) or _OTHER_GROUP
        if group not in groups:
            groups[group] = []
            order.append(group)
        groups[group].append(audit)

    def sort_key(label: str) -> tuple[int, int]:
        if label == _OTHER_GROUP:
            return (2, 0)
        if label in _METRIC_ORDER:
            return (0, _METRIC_ORDER.index(label))
        return (1, 0)

    return [(label, groups[label]) for label in sorted(order, key=sort_key)]


def _primary_metric(audit: dict) -> str | None:
    savings = audit.get("metric_savings") or {}
    if not savings:
        return None

    return str(max(savings, key=lambda k: abs(savings[k])))


def _render_audit(audit: dict) -> list[str]:
    lines = ["", f"### {audit.get('title') or audit.get('id')}"]

    impact = _impact_line(audit)
    if impact:
        lines.append(impact)

    description = _clean_description(audit.get("description"))
    if description:
        lines.append(f"> {description}")

    for item in audit.get("items") or []:
        lines.append(_render_item(item))

    return lines


def _impact_line(audit: dict) -> str:
    parts = []

    display_value = audit.get("display_value")
    if display_value:
        parts.append(str(display_value))

    savings = audit.get("metric_savings") or {}
    if savings:
        formatted = ", ".join(_format_saving(metric, value) for metric, value in savings.items())
        parts.append(formatted)

    if not parts:
        return ""

    return "**Impact:** " + " · ".join(parts)


def _format_saving(metric: str, value) -> str:
    if metric in _MS_METRICS:
        return f"{metric} -{round(value)} ms"
    return f"{metric} -{value}"


def _clean_description(description) -> str:
    if not isinstance(description, str) or not description:
        return ""
    return " ".join(description.split())


def _render_item(item: dict) -> str:
    label = (
        item.get("url")
        or item.get("selector")
        or item.get("entity")
        or item.get("groupLabel")
        or item.get("statistic")
        or item.get("reason")
        or "(item)"
    )

    fragments = [f"- `{label}`"]

    metrics_bits = []
    if "wastedBytes" in item:
        metrics_bits.append(f"save {_kib(item['wastedBytes'])}")
    if "wastedMs" in item:
        metrics_bits.append(f"{round(item['wastedMs'])} ms")
    if "responseTime" in item:
        metrics_bits.append(f"{round(item['responseTime'])} ms")
    if metrics_bits:
        fragments.append(" — " + ", ".join(metrics_bits))

    if item.get("reason") and item.get("reason") != label:
        fragments.append(f" ({item['reason']})")

    for reason in item.get("sub_reasons") or []:
        fragments.append(f"\n  - {reason}")

    snippet = item.get("snippet")
    if snippet and not item.get("url"):
        fragments.append(f"\n  - `{snippet}`")

    return "".join(fragments)


def _kib(byte_count) -> str:
    return f"{byte_count / 1024:.1f} KiB"
