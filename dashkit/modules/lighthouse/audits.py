def is_audit_relevant(audit: dict) -> bool:
    if (  # noqa: SIM103
        get_score_status(audit.get("score")) == 1
        or audit.get("scoreDisplayMode") == "notApplicable"
        or audit.get("scoreDisplayMode") == "manual"
    ):
        return False

    return True


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
