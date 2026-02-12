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
        "performance": ("74", .74),
        "accessibility": ("89", .89),
        "best-practices": ("73", .73),
        "seo": ("92", .92),
        "first-contentful-paint": ("0.4\xa0s", .9),
        "largest-contentful-paint": ("1.0\xa0s", .9),
        "interactive": ("4.3\xa0s", .75),
        "total-blocking-time": ("530\xa0ms", .4),
        "cumulative-layout-shift": ("0", .9),
    },
    {
        "label": "Equipment",
        "performance": ("94", .94),
        "accessibility": ("95", .95),
        "best-practices": ("92", .92),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.3\xa0s", .9),
        "largest-contentful-paint": ("0.7\xa0s", .9),
        "interactive": ("3.1\xa0s", .75),
        "total-blocking-time": ("190\xa0ms", .75),
        "cumulative-layout-shift": ("0", .9),
    },
    {
        "label": "Part",
        "performance": ("99", .99),
        "accessibility": ("98", .98),
        "best-practices": ("92", .92),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.3\xa0s", .9),
        "largest-contentful-paint": ("0.7\xa0s", .9),
        "interactive": ("3.0\xa0s", .75),
        "total-blocking-time": ("70\xa0ms", .9),
        "cumulative-layout-shift": ("0", .9),
    },
    {
        "label": "Collection",
        "performance": ("83", .83),
        "accessibility": ("97", .97),
        "best-practices": ("73", .73),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.4\xa0s", .9),
        "largest-contentful-paint": ("0.7\xa0s", .9),
        "interactive": ("4.1\xa0s", .75),
        "total-blocking-time": ("340\xa0ms", .75),
        "cumulative-layout-shift": ("0", .9),
    },
    {
        "label": "Content",
        "performance": ("78", .78),
        "accessibility": ("97", .97),
        "best-practices": ("73", .73),
        "seo": ("100", 1),
        "first-contentful-paint": ("0.5\xa0s", .9),
        "largest-contentful-paint": ("0.7\xa0s", .9),
        "interactive": ("4.3\xa0s", .75),
        "total-blocking-time": ("440\xa0ms", .4),
        "cumulative-layout-shift": ("0", .9),
    },
]


def screenshot_metric_summary(console: Console):
    table = presenter(metrics_sample, columns)
    console.print("[bold cyan]Lighthouse Metric Summary[/bold cyan]")

    console.print(table)
