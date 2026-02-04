from rich.console import Console

from dashkit.framework.presenters.occurrence_tables import get_occurrence_table


def screenshot_get_occurrence_table(console: Console):
    test_data = {
        "Google Fonts": [True, False, False, True, True],
        "YouTube": [True, False, False, True, True],
        "shop.app": [False, False, False, False, True],
    }

    console.print("[bold cyan]3rd Party Scripts[/bold cyan]")
    table = get_occurrence_table(test_data)
    console.print(table)
