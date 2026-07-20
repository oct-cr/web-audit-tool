from .export import build_page_report, extract_audit_details
from .export_markdown import render_page_markdown

# --- extract_audit_details ------------------------------------------------


def test_extract_details_opportunity_item():
    audit = {
        "details": {
            "type": "opportunity",
            "items": [
                {
                    "url": "https://cdn.example.com/app.js",
                    "totalBytes": 456439,
                    "wastedBytes": 317512,
                    "wastedPercent": 69.5,
                }
            ],
        }
    }

    rows = extract_audit_details(audit)

    assert rows == [
        {
            "url": "https://cdn.example.com/app.js",
            "wastedBytes": 317512,
            "totalBytes": 456439,
            "wastedPercent": 69.5,
        }
    ]


def test_extract_details_pulls_node_and_flattens_sub_reasons():
    audit = {
        "details": {
            "type": "table",
            "items": [
                {
                    "url": "https://cdn.example.com/hero.png",
                    "wastedBytes": 11579,
                    "node": {
                        "selector": "div.wrapper > img.featured-product-image",
                        "snippet": '<img class="featured-product-image" src="...">',
                    },
                    "subItems": {
                        "type": "subitems",
                        "items": [{"reason": "Increasing compression could help."}],
                    },
                }
            ],
        }
    }

    rows = extract_audit_details(audit)

    assert rows[0]["selector"] == "div.wrapper > img.featured-product-image"
    assert rows[0]["snippet"].startswith("<img")
    assert rows[0]["sub_reasons"] == ["Increasing compression could help."]


def test_extract_details_empty_or_missing():
    assert extract_audit_details({}) == []
    assert extract_audit_details({"details": {"items": []}}) == []
    assert extract_audit_details({"details": None}) == []


# --- build_page_report ----------------------------------------------------


def _report() -> dict:
    return {
        "lighthouseResult": {
            "requestedUrl": "https://example.test/",
            "finalDisplayedUrl": "https://example.test/",
            "fetchTime": "2026-06-16T12:54:53Z",
            "lighthouseVersion": "12.0.0",
            "configSettings": {"formFactor": "mobile"},
            "runWarnings": [],
            "categories": {
                "performance": {"id": "performance", "score": 0.77},
                "accessibility": {"id": "accessibility", "score": 0.93},
            },
            "audits": {
                "largest-contentful-paint": {
                    "id": "largest-contentful-paint",
                    "title": "Largest Contentful Paint",
                    "score": 0.4,
                    "displayValue": "4.4\xa0s",
                },
                "unused-javascript": {
                    "id": "unused-javascript",
                    "title": "Reduce unused JavaScript",
                    "score": 0,
                    "displayValue": "Est savings of 60 KiB",
                    "metricSavings": {"LCP": 600, "FCP": 600, "CLS": 0},
                    "details": {
                        "type": "opportunity",
                        "items": [
                            {
                                "url": "https://cdn.example.com/app.js",
                                "wastedBytes": 61704,
                                "totalBytes": 150631,
                            }
                        ],
                    },
                },
                "color-contrast": {
                    "id": "color-contrast",
                    "title": "Contrast is sufficient",
                    "score": 1,
                    "scoreDisplayMode": "binary",
                },
            },
        }
    }


def test_build_page_report_filters_and_extracts():
    page = build_page_report(_report())

    assert page["url"] == "https://example.test/"
    assert page["form_factor"] == "mobile"

    audit_ids = [a["id"] for a in page["audits"]]
    assert "unused-javascript" in audit_ids
    assert "color-contrast" not in audit_ids  # passing audit filtered out

    unused = next(a for a in page["audits"] if a["id"] == "unused-javascript")
    assert unused["metric_savings"] == {"LCP": 600, "FCP": 600}  # zero CLS dropped
    assert unused["items"][0]["url"] == "https://cdn.example.com/app.js"


def test_build_page_report_does_not_mutate_source():
    report = _report()
    build_page_report(report)

    assert "details" in report["lighthouseResult"]["audits"]["unused-javascript"]


# --- render_page_markdown -------------------------------------------------


def test_render_markdown_contains_key_agent_data():
    markdown = render_page_markdown(build_page_report(_report()))

    assert "# Lighthouse Report — https://example.test/" in markdown
    assert "## Scores" in markdown
    assert "Reduce unused JavaScript" in markdown
    assert "https://cdn.example.com/app.js" in markdown
    assert "LCP -600 ms" in markdown


def test_render_markdown_is_deterministic():
    page = build_page_report(_report())
    assert render_page_markdown(page) == render_page_markdown(page)


def test_render_markdown_no_actionable_issues():
    report = _report()
    report["lighthouseResult"]["audits"] = {
        "color-contrast": {"id": "color-contrast", "score": 1, "scoreDisplayMode": "binary"}
    }

    markdown = render_page_markdown(build_page_report(report))

    assert "No actionable issues found" in markdown
