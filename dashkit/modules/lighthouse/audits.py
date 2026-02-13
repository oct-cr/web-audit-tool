from .config import metrics as CONFIG_METRICS


def is_audit_relevant(audit: dict) -> bool:
    if (  # noqa: SIM103
        get_score_status(audit.get("score")) == 1
        or audit.get("scoreDisplayMode") == "notApplicable"
        or audit.get("scoreDisplayMode") == "manual"
    ):
        return False

    return True


def get_audits_sorted_by_savings(audits: list) -> list:
    if not audits:
        return []

    included = set()
    sorted_audits: list = []

    def append_once(audit: dict) -> None:
        audit_id = audit.get("id")
        if not audit_id or audit_id in included:
            return
        included.add(audit_id)
        sorted_audits.append(audit)

    # 1) Audits that impact more than one metric
    for a in audits:
        ms = a.get("metricSavings") or {}
        non_zero_count = 0
        for v in ms.values():
            try:
                if v:
                    non_zero_count += 1
            except Exception:
                continue
        if non_zero_count > 1:
            append_once(a)

    # 2) For each primary metric, add primary, then audits
    for a in audits:
        if a.get("id") not in CONFIG_METRICS:
            continue

        append_once(a)

        acronym = CONFIG_METRICS[a.get("id")]

        # then add audits that reference this metric with non-zero savings
        for a in audits:
            ms = a.get("metricSavings") or {}
            val = ms.get(acronym)
            try:
                if val:
                    append_once(a)
            except Exception:
                continue

    # 3) Remaining audits in original order
    for a in audits:
        append_once(a)

    return sorted_audits


def get_audit_display_value(audit: dict) -> str | None:
    raw_value = (
        audit.get("overallSavingsBytes") or audit.get("displayValue") or audit.get("numericValue")
    )

    s = str(raw_value) if raw_value is not None else None

    return s


def get_score_status(score: float | None) -> int:
    if score is None:
        return 0

    try:
        s = float(score)
    except Exception:
        return 0

    if s > 1:
        s = s / 100.0

    if s >= 0.9:
        return 1
    if s >= 0.5:
        return 2

    return 3
