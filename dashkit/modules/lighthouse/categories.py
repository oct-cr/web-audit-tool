from .audits import is_audit_relevant


def get_relevant_category_audits(lhr_audits, category):
    relevant_audits = []
    audit_refs = category.get("auditRefs", [])

    for audit_ref in audit_refs:
        audit_key = audit_ref.get("id")

        audit = lhr_audits.get(audit_key)
        if not audit:
            continue

        if not is_audit_relevant(audit):
            continue

        if "details" in audit:
            del audit["details"]

        relevant_audits.append(
            {
                **audit,
                "weight": audit_ref.get("weight", 0),
            }
        )

    def sort_key(a):
        weight = a.get("weight", 0)
        score = a.get("score") or 0
        if weight:
            return (0, -(weight * (1 - score)))
        return (1, score)

    return sorted(relevant_audits, key=sort_key)
