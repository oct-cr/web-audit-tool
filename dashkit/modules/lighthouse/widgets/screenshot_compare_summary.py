from rich.console import Console

from ..compare import diff_audits, diff_metrics, diff_thirdparty
from .audits import get_audit_changes_widget
from .metrics_summary import get_compare_metrics_widget


def _report(perf, audits, third_party):
    def metric(audit_id, title, value, score):
        return {"id": audit_id, "title": title, "displayValue": value, "score": score}

    lhr_audits = {
        "first-contentful-paint": metric(
            "first-contentful-paint", "First Contentful Paint", "0.5\xa0s", 0.9
        ),
        "largest-contentful-paint": metric(
            "largest-contentful-paint", "Largest Contentful Paint", "1.2\xa0s", 0.85
        ),
        "interactive": metric("interactive", "Time to Interactive", "4.3\xa0s", 0.75),
        "total-blocking-time": metric(
            "total-blocking-time", "Total Blocking Time", "170\xa0ms", 0.8
        ),
        "cumulative-layout-shift": metric(
            "cumulative-layout-shift", "Cumulative Layout Shift", "0", 0.95
        ),
        "third-parties-insight": {
            "details": {"items": [{"entity": e, "mainThreadTime": 30} for e in third_party]}
        },
    }
    for audit_id, (title, score, value) in audits.items():
        lhr_audits[audit_id] = {
            "id": audit_id,
            "title": title,
            "score": score,
            "displayValue": value,
        }

    return {
        "lighthouseResult": {
            "requestedUrl": "https://example.com",
            "categories": {
                "performance": {"id": "performance", "score": perf},
                "accessibility": {"id": "accessibility", "score": 0.97},
                "best-practices": {"id": "best-practices", "score": 0.73},
                "seo": {"id": "seo", "score": 1.0},
            },
            "audits": lhr_audits,
        }
    }


_current = _report(
    perf=0.81,
    audits={
        "uses-text-compression": ("Enable text compression", 1.0, ""),
        "render-blocking-resources": ("Render-blocking requests", 0.2, "Est savings of 760\xa0ms"),
        "unused-javascript": ("Reduce unused JavaScript", 0.3, "Est savings of 1,104\xa0KiB"),
    },
    third_party=["Google Analytics", "Google Tag Manager"],
)

_baseline = _report(
    perf=0.74,
    audits={
        "uses-text-compression": ("Enable text compression", 0.2, "Est savings of 1.2\xa0s"),
        "render-blocking-resources": ("Render-blocking requests", 1.0, ""),
        "unused-javascript": ("Reduce unused JavaScript", 0.3, "Est savings of 1,200\xa0KiB"),
    },
    third_party=["Google Analytics", "Hotjar"],
)


def screenshot_compare_summary(console: Console):
    console.print("[bold steel_blue3]Comparing: content   2026-05-18 13:28 → 2026-06-16 12:54[/]")

    metrics_data, metrics_view = get_compare_metrics_widget(diff_metrics(_current, _baseline))
    console.print(metrics_view(metrics_data))

    audit_data, audit_view = get_audit_changes_widget(diff_audits(_current, _baseline))
    console.print(audit_view(audit_data))

    tp = diff_thirdparty(_current, _baseline)
    console.print("")
    console.print("[dim]3rd-Party Scripts — Changed[/dim]")
    for label in tp["added"]:
        console.print(f"[dark_green]+ {label}[/dark_green]")
    for label in tp["removed"]:
        console.print(f"[deep_pink3]- {label}[/deep_pink3]")
