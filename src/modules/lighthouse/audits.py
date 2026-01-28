def fmt_bytes(n):
    if n is None:
        return "n/a"
    try:
        n = float(n)
    except Exception:
        return str(n)
    units = ["B", "KiB", "MiB", "GiB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024.0
        i += 1
    if units[i] == "B":
        return f"{int(n)}{units[i]}"
    return f"{n:.1f}{units[i]}"


def get_audit_display_value(audit):
    raw_value = (
        audit.get("overallSavingsBytes")
        or audit.get("displayValue")
        or audit.get("numericValue")
    )
    s = str(raw_value) if raw_value is not None else None

    return s


def get_score_status(score):
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
