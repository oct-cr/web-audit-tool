from .insights import get_score_status


def get_relevant_category_audits(audits, category):
    relevant_audits = []
    audit_refs = category.get("auditRefs", [])

    for audit_ref in audit_refs:
        audit_key = audit_ref.get("id")

        audit = audits.get(audit_key)
        if not audit:
            continue

        if (
            get_score_status(audit.get("score")) == 1
            or audit.get("scoreDisplayMode") == "notApplicable"
            or audit.get("scoreDisplayMode") == "manual"
        ):
            continue

        relevant_audits.append(
            {
                **audit,
                "weight": audit_ref.get("weight", 1),
            }
        )

    return sorted(relevant_audits, key=lambda audit: audit.get("weight", 1))


def get_relevant_audits(report):
    lr = report.get("lighthouseResult", {})
    audits = lr.get("audits", {})
    categories = lr.get("categories", {})

    relevant_audits = []

    for category in categories.values():
        category_audits = get_relevant_category_audits(audits, category)
        relevant_audits.append(
            {
                "label": category.get("title"),
                "audits": category_audits,
            }
        )

    return relevant_audits
