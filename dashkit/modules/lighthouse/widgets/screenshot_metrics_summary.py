from rich.console import Console

from .metrics_summary import get_metrics_summary_widget

_, presenter = get_metrics_summary_widget([])

columns = {
    "label": "Page",
    "performance": "Performance",
    "accessibility": "Accessibility",
    "best-practices": "Best Practices",
    "seo": "SEO",
    "first-contentful-paint": "FCP",
    "largest-contentful-paint": "LCP",
    "interactive": "TTI",
    "total-blocking-time": "TBT",
    "cumulative-layout-shift": "CLS",
}

metrics_sample = [
    {
        "label": "Frontpage",
        "performance": ("74", 2),
        "accessibility": ("89", 2),
        "best-practices": ("73", 2),
        "seo": ("92", 1),
        "first-contentful-paint": ("0.4\xa0s", 1),
        "largest-contentful-paint": ("1.0\xa0s", 1),
        "interactive": ("4.3\xa0s", 2),
        "total-blocking-time": ("530\xa0ms", 3),
        "cumulative-layout-shift": ("0", 1),
    },
    {
        "label": "Equipment",
        "performance": ("94", 1),
        "accessibility": ("95", 1),
        "best-practices": ("92", 1),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.3\xa0s", 1),
        "largest-contentful-paint": ("0.7\xa0s", 1),
        "interactive": ("3.1\xa0s", 2),
        "total-blocking-time": ("190\xa0ms", 2),
        "cumulative-layout-shift": ("0", 1),
    },
    {
        "label": "Part",
        "performance": ("99", 1),
        "accessibility": ("98", 1),
        "best-practices": ("92", 1),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.3\xa0s", 1),
        "largest-contentful-paint": ("0.7\xa0s", 1),
        "interactive": ("3.0\xa0s", 2),
        "total-blocking-time": ("70\xa0ms", 1),
        "cumulative-layout-shift": ("0", 1),
    },
    {
        "label": "Collection",
        "performance": ("83", 2),
        "accessibility": ("97", 1),
        "best-practices": ("73", 2),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.4\xa0s", 1),
        "largest-contentful-paint": ("0.7\xa0s", 1),
        "interactive": ("4.1\xa0s", 2),
        "total-blocking-time": ("340\xa0ms", 2),
        "cumulative-layout-shift": ("0", 1),
    },
    {
        "label": "Content",
        "performance": ("78", 2),
        "accessibility": ("97", 1),
        "best-practices": ("73", 2),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.5\xa0s", 1),
        "largest-contentful-paint": ("0.7\xa0s", 1),
        "interactive": ("4.3\xa0s", 2),
        "total-blocking-time": ("440\xa0ms", 3),
        "cumulative-layout-shift": ("0", 1),
    },
]


def screenshot_metrics_summary(console: Console):
    table = presenter(metrics_sample, columns)
    console.print("[bold cyan]Lighthouse Metrics Summary[/bold cyan]")

    console.print(table)
