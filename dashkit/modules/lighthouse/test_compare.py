from .compare import diff_audits, diff_metrics, diff_thirdparty


def _report(*, perf, lcp_score, audits=None, third_party=None) -> dict:
    lhr_audits = {
        "largest-contentful-paint": {
            "id": "largest-contentful-paint",
            "displayValue": "2.1\xa0s",
            "score": lcp_score,
        },
    }
    for audit_id, score in (audits or {}).items():
        lhr_audits[audit_id] = {"id": audit_id, "title": audit_id, "score": score}

    if third_party is not None:
        lhr_audits["third-parties-insight"] = {
            "details": {
                "items": [{"entity": e, "mainThreadTime": 10} for e in third_party]
            }
        }

    return {
        "lighthouseResult": {
            "requestedUrl": "https://example.test",
            "categories": {"performance": {"id": "performance", "score": perf}},
            "audits": lhr_audits,
        }
    }


# --- diff_metrics ---------------------------------------------------------


def test_diff_metrics_improvement():
    current = _report(perf=0.81, lcp_score=0.6)
    baseline = _report(perf=0.74, lcp_score=0.6)

    diff = diff_metrics(current, baseline)

    display, _score, delta = diff["performance"]
    assert display == "81"
    assert delta == 0.07  # improved


def test_diff_metrics_regression():
    current = _report(perf=0.70, lcp_score=0.6)
    baseline = _report(perf=0.74, lcp_score=0.6)

    _, _, delta = diff_metrics(current, baseline)["performance"]
    assert delta == -0.04


def test_diff_metrics_flat():
    current = _report(perf=0.74, lcp_score=0.6)
    baseline = _report(perf=0.74, lcp_score=0.6)

    _, _, delta = diff_metrics(current, baseline)["performance"]
    assert delta == 0.0


def test_diff_metrics_lower_is_better_direction():
    # LCP score went up (faster page) -> positive delta, reads as improvement.
    current = _report(perf=0.8, lcp_score=0.9)
    baseline = _report(perf=0.8, lcp_score=0.5)

    _, _, delta = diff_metrics(current, baseline)["largest-contentful-paint"]
    assert delta > 0


# --- diff_audits ----------------------------------------------------------


def test_diff_audits_buckets():
    # lcp_score=1.0 keeps the always-present LCP audit out of the buckets so
    # the test isolates the audits under test.
    current = _report(
        perf=0.8,
        lcp_score=1.0,
        audits={"a-fixed": 1.0, "a-regressed": 0.2, "a-still": 0.1, "a-stable": 1.0},
    )
    baseline = _report(
        perf=0.8,
        lcp_score=1.0,
        audits={"a-fixed": 0.2, "a-regressed": 1.0, "a-still": 0.1, "a-stable": 1.0},
    )

    diff = diff_audits(current, baseline)

    assert [a["id"] for a in diff["fixed"]] == ["a-fixed"]
    assert [a["id"] for a in diff["regressed"]] == ["a-regressed"]
    assert [a["id"] for a in diff["still_failing"]] == ["a-still"]


def test_diff_audits_excludes_unchanged_passing():
    current = _report(perf=0.8, lcp_score=0.6, audits={"a-stable": 1.0})
    baseline = _report(perf=0.8, lcp_score=0.6, audits={"a-stable": 1.0})

    diff = diff_audits(current, baseline)
    ids = [a["id"] for bucket in diff.values() for a in bucket]
    assert "a-stable" not in ids


# --- diff_thirdparty ------------------------------------------------------


def test_diff_thirdparty_add_remove():
    current = _report(perf=0.8, lcp_score=0.6, third_party=["GA", "GTM"])
    baseline = _report(perf=0.8, lcp_score=0.6, third_party=["GA", "Hotjar"])

    diff = diff_thirdparty(current, baseline)
    assert diff["added"] == ["GTM"]
    assert diff["removed"] == ["Hotjar"]


def test_diff_thirdparty_identical():
    current = _report(perf=0.8, lcp_score=0.6, third_party=["GA", "GTM"])
    baseline = _report(perf=0.8, lcp_score=0.6, third_party=["GTM", "GA"])

    diff = diff_thirdparty(current, baseline)
    assert diff["added"] == []
    assert diff["removed"] == []
