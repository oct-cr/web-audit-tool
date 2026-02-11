from dashkit.modules.lighthouse.widgets.metrics_summary import (
    _get_column_average_scores,
    _get_row_average_scores,
)


def test_calculate_row_average_with_categories():
    columns = {
        "label": "Page",
        "performance": "Performance",
        "accessibility": "Accessibility",
        "best-practices": "Best Practices",
        "seo": "SEO",
    }

    row = {
        "label": "Test Page",
        "performance": ("80", 0.8),
        "accessibility": ("90", 0.9),
        "best-practices": ("70", 0.7),
        "seo": ("80", 0.8),
    }

    avg = _get_row_average_scores(row, columns)
    assert avg == 0.8


def test_calculate_column_averages():
    columns = {
        "label": "Page",
        "performance": "Performance",
        "accessibility": "Accessibility",
    }

    rows = [
        {
            "label": "Page 1",
            "performance": ("90", 0.9),
            "accessibility": ("80", 0.8),
        },
        {
            "label": "Page 2",
            "performance": ("80", 0.8),
            "accessibility": ("90", 0.9),
        },
    ]

    averages = _get_column_average_scores(rows, columns)

    assert "label" not in averages
    assert "performance" in averages
    assert "accessibility" in averages
    assert averages["performance"] == 0.85
    assert averages["accessibility"] == 0.85
