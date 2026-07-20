"""Build an agent-ready data model from a raw Lighthouse report.

Pure functions only — no rendering, no disk I/O. The human-facing pipeline in
``categories.py`` deletes ``audit["details"]`` before rendering; a coding agent
needs exactly that payload (resource URLs, DOM selectors, byte/ms savings), so we
read ``lighthouseResult.audits`` directly and never mutate the source dicts.
"""

from .audits import get_audits_sorted_by_savings, is_audit_relevant
from .widgets.metrics_summary import get_insights_row

_SAVINGS_KEYS = ("wastedBytes", "totalBytes", "wastedPercent", "wastedMs", "responseTime")


def build_page_report(report: dict) -> dict:
    """Return an agent-ready summary: header, scores row, actionable audits.

    Audits are ordered by metric-savings priority (via
    ``get_audits_sorted_by_savings``) and carry a normalized ``items`` list
    extracted from their ``details``.
    """
    lhr = report.get("lighthouseResult", {})
    audits = lhr.get("audits", {}) or {}

    actionable = [
        audit for audit in audits.values() if isinstance(audit, dict) and is_audit_relevant(audit)
    ]
    ordered = get_audits_sorted_by_savings(actionable)

    audit_summaries = [_summarize_audit(audit) for audit in ordered]

    return {
        "url": lhr.get("requestedUrl") or lhr.get("finalUrl"),
        "final_url": lhr.get("finalDisplayedUrl") or lhr.get("finalUrl"),
        "fetch_time": lhr.get("fetchTime"),
        "lighthouse_version": lhr.get("lighthouseVersion"),
        "form_factor": (lhr.get("configSettings") or {}).get("formFactor"),
        "run_warnings": list(lhr.get("runWarnings") or []),
        "scores": get_insights_row(report),
        "audits": audit_summaries,
    }


def _summarize_audit(audit: dict) -> dict:
    return {
        "id": audit.get("id"),
        "title": audit.get("title"),
        "description": audit.get("description"),
        "score": audit.get("score"),
        "display_value": audit.get("displayValue"),
        "metric_savings": _non_zero_savings(audit.get("metricSavings")),
        "items": extract_audit_details(audit),
    }


def _non_zero_savings(metric_savings) -> dict:
    if not isinstance(metric_savings, dict):
        return {}
    return {k: v for k, v in metric_savings.items() if v}


def extract_audit_details(audit: dict) -> list[dict]:
    """Normalize ``audit["details"]["items"]`` into flat, agent-useful rows.

    Pulls the DOM node (selector/snippet) out of ``node`` cells, keeps the
    resource ``url`` and any byte/ms savings, and flattens one level of
    ``subItems`` so per-source breakdowns are visible. Returns ``[]`` when there
    is nothing actionable (e.g. passing audits with empty item lists).
    """
    details = audit.get("details")
    if not isinstance(details, dict):
        return []

    items = details.get("items")
    if not isinstance(items, list):
        return []

    rows: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue

        row = _normalize_item(item)
        if row:
            rows.append(row)

    return rows


def _normalize_item(item: dict) -> dict:
    row: dict = {}

    url = item.get("url")
    if isinstance(url, str) and url:
        row["url"] = url

    for key in ("entity", "groupLabel", "statistic", "reason"):
        value = item.get(key)
        if isinstance(value, str) and value:
            row[key] = value

    node = item.get("node")
    if isinstance(node, dict):
        selector = node.get("selector")
        snippet = node.get("snippet")
        if selector:
            row["selector"] = selector
        if snippet:
            row["snippet"] = snippet

    for key in _SAVINGS_KEYS:
        value = item.get(key)
        if isinstance(value, (int, float)) and value:
            row[key] = value

    sub_reasons = _sub_item_reasons(item.get("subItems"))
    if sub_reasons:
        row["sub_reasons"] = sub_reasons

    return row


def _sub_item_reasons(sub_items) -> list[str]:
    if not isinstance(sub_items, dict):
        return []

    inner = sub_items.get("items")
    if not isinstance(inner, list):
        return []

    reasons: list[str] = []
    for sub in inner:
        if not isinstance(sub, dict):
            continue
        reason = sub.get("reason")
        if isinstance(reason, str) and reason:
            reasons.append(reason)

    return reasons
