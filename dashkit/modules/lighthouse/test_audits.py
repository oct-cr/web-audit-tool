from .audits import get_audits_sorted_by_savings

expected = [
    "unused-css-rules",  # Impacts more than one metric
    "largest-contentful-paint",  # Primary metric
    "unused-javascript",  # Impacts only prev Metric
    "first-contentful-paint",  # Primary metric
    "render-blocking-insight",  # Impacts only prev Metric
    "interactive",  # Primary metric, no audits impacting on it
    "forced-reflow-insight",  # Audits impacting no metric
    "lcp-discovery-insight",
    "network-dependency-tree-insight",
    "cache-insight",
    "font-display-insight",
    "max-potential-fid",
]

audits = [
    {
        "id": "largest-contentful-paint",
        "title": "Largest Contentful Paint",
        "score": 0.1,
        "displayValue": "6.3\xa0s",
        "weight": 25,
    },
    {
        "id": "first-contentful-paint",
        "title": "First Contentful Paint",
        "score": 0.81,
        "displayValue": "2.1\xa0s",
        "weight": 10,
    },
    {
        "id": "forced-reflow-insight",
        "title": "Forced reflow",
        "score": 0,
        "weight": 0,
    },
    {
        "id": "lcp-discovery-insight",
        "title": "LCP request discovery",
        "score": 0,
        "metricSavings": {"LCP": 0},
        "weight": 0,
    },
    {
        "id": "network-dependency-tree-insight",
        "title": "Network dependency tree",
        "score": 0,
        "metricSavings": {"LCP": 0},
        "weight": 0,
    },
    {
        "id": "render-blocking-insight",
        "title": "Render blocking requests",
        "score": 0,
        "displayValue": "Est savings of 990\xa0ms",
        "metricSavings": {"LCP": 0, "FCP": 1000},
        "weight": 0,
    },
    {
        "id": "unused-css-rules",
        "title": "Reduce unused CSS",
        "score": 0,
        "displayValue": "Est savings of 21\xa0KiB",
        "metricSavings": {"LCP": 300, "FCP": 300},
        "weight": 0,
    },
    {
        "id": "unused-javascript",
        "title": "Reduce unused JavaScript",
        "score": 0,
        "displayValue": "Est savings of 122\xa0KiB",
        "metricSavings": {"LCP": 350, "FCP": 0},
        "weight": 0,
    },
    {
        "id": "cache-insight",
        "title": "Use efficient cache lifetimes",
        "score": 0.5,
        "displayValue": "Est savings of 37\xa0KiB",
        "metricSavings": {"LCP": 0, "FCP": 0},
        "weight": 0,
    },
    {
        "id": "font-display-insight",
        "title": "Font display",
        "score": 0.5,
        "displayValue": "Est savings of 20\xa0ms",
        "metricSavings": {"FCP": 0, "INP": 0},
        "weight": 0,
    },
    {
        "id": "interactive",
        "title": "Time to Interactive",
        "score": 0.53,
        "displayValue": "7.0\xa0s",
        "weight": 0,
    },
    {
        "id": "max-potential-fid",
        "title": "Max Potential First Input Delay",
        "score": 0.89,
        "displayValue": "130\xa0ms",
        "weight": 0,
    },
]


def test_get_audits_grouped_by_savings():
    grouped_audits = get_audits_sorted_by_savings(audits)

    assert len(grouped_audits) == len(expected)

    for audit, expected_id in zip(grouped_audits, expected, strict=False):
        assert audit.get("id") == expected_id
