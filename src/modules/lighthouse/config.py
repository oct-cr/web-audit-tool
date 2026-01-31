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


def get_summary_columns():
    return {**columns}
