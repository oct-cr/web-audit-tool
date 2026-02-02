from rich.console import group
from rich.text import Text

from framework.status import get_status_icon


@group()
def get_occurrence_table(dict):
    max_label_width = max(len(label) for label in dict) if dict else 0
    max_count_width = (
        max(len(str(sum(occurrences))) for occurrences in dict.values()) if dict else 0
    )

    for label, occurrences in dict.items():
        count = sum(occurrences)

        padded_label = label.ljust(max_label_width)
        padded_count = str(count).rjust(max_count_width)

        text = Text(f"{padded_label} ")
        text.append(padded_count, style="cyan")
        text.append(" ")

        for occurred in occurrences:
            status = 1 if occurred else 0
            icon = get_status_icon(status)
            text.append("■" if occurred else icon.plain, style=icon.style)

        yield text
