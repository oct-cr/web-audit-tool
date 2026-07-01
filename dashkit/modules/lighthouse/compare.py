"""Pure diff logic for comparing two Lighthouse reports.

No rendering here — these functions return plain data structures that the
comparison widgets turn into Rich output.
"""

from .audits import get_score_status, is_audit_relevant
from .config import categories, metrics
from .widgets.metrics_summary import get_insights_row
from .widgets.thirdparty import _get_third_party_items


def diff_metrics(current: dict, baseline: dict) -> dict:
    """Diff category + metric cells between two reports.

    Returns a single row dict keyed by column, where each value is a tuple of
    ``(display, score, delta_score)``. ``delta_score`` is ``None`` when the
    column is missing from either report. The display string is the current
    value; callers colour the delta by ``delta_score`` so that lower-is-better
    metrics (LCP/FCP/...) read correctly.
    """
    cur_row = get_insights_row(current)
    base_row = get_insights_row(baseline)

    diffed: dict = {}

    for key in (*categories.keys(), *metrics.keys()):
        cur_cell = cur_row.get(key)
        base_cell = base_row.get(key)

        if not isinstance(cur_cell, tuple):
            continue

        display, score = cur_cell

        delta_score = None
        if isinstance(base_cell, tuple) and score is not None and base_cell[1] is not None:
            delta_score = round(float(score) - float(base_cell[1]), 2)

        diffed[key] = (display, score, delta_score)

    return diffed


def _audit_map(report: dict) -> dict:
    lr = report.get("lighthouseResult", {})
    return lr.get("audits", {}) or {}


def diff_audits(current: dict, baseline: dict) -> dict:
    """Bucket audits by status transition between two reports.

    Returns ``{"fixed": [...], "regressed": [...], "still_failing": [...]}``.
    Only *actionable* audits move the needle: "failing" means
    ``is_audit_relevant`` (not passing, not notApplicable/manual). Passing means
    a perfect status. ``fixed`` carries the current passing audit; the other
    buckets carry the current failing audit so the title/value reflect the
    latest state.
    """
    cur = _audit_map(current)
    base = _audit_map(baseline)

    fixed = []
    regressed = []
    still_failing = []

    audit_ids = set(cur) | set(base)

    for audit_id in audit_ids:
        cur_audit = cur.get(audit_id)
        base_audit = base.get(audit_id)

        cur_failing = cur_audit is not None and is_audit_relevant(cur_audit)
        base_failing = base_audit is not None and is_audit_relevant(base_audit)

        cur_pass = cur_audit is not None and get_score_status(cur_audit.get("score")) == 1
        base_pass = base_audit is not None and get_score_status(base_audit.get("score")) == 1

        if cur_pass and base_failing:
            fixed.append(cur_audit)
        elif cur_failing and base_pass:
            regressed.append(cur_audit)
        elif cur_failing and base_failing:
            still_failing.append(cur_audit)

    return {
        "fixed": _by_title(fixed),
        "regressed": _by_title(regressed),
        "still_failing": _by_title(still_failing),
    }


def _by_title(audits: list) -> list:
    return sorted(audits, key=lambda a: (a.get("title") or "").lower())


def diff_thirdparty(current: dict, baseline: dict) -> dict:
    """Diff third-party script entities between two reports.

    Returns ``{"added": [...], "removed": [...]}`` entity labels.
    """
    cur_labels = {i.get("label") for i in _get_third_party_items(current) if i.get("label")}
    base_labels = {i.get("label") for i in _get_third_party_items(baseline) if i.get("label")}

    added = sorted(cur_labels - base_labels, key=str.lower)
    removed = sorted(base_labels - cur_labels, key=str.lower)

    return {"added": added, "removed": removed}
