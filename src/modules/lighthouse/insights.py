from .audits import get_audit_display_value, get_score_status


categories = {
    "performance": "Performance",
    "accessibility": "Accessibility",
    "best-practices": "Best Practices",
    "seo": "SEO",
}

metrics = {
    "first-contentful-paint": "FCP",
    "largest-contentful-paint": "LCP",
    "interactive": "TTI",
    "total-blocking-time": "TBT",
    "cumulative-layout-shift": "CLS",
}

columns = {
    "url": "URL",
    **categories,
    **metrics,
}


def get_insights_summary(report):
    lhr = report.get("lighthouseResult", {})
    audits = lhr.get("audits", {})
    categories = lhr.get("categories", {})

    cells = {
        "url": lhr.get("requestedUrl"),
    }

    for key, category in categories.items():
        score = category.get("score", 0)
        status = get_score_status(score)
        cells[key] = (f"{score * 100:.0f}", status)

    for key in metrics:
        audit = audits.get(key)
        if not audit:
            continue

        status = get_score_status(audit.get("score"))
        cells[key] = (get_audit_display_value(audit), status)

    return cells


def get_summary_columns():
    return {**columns}
