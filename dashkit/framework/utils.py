from collections.abc import Iterable


def get_occurrences(items: Iterable[Iterable[str]]) -> dict[str, list[bool]]:
    items_list = list(items)
    all_items = sorted({it for row in items_list for it in row})

    occurrences: dict[str, list[bool]] = {}
    for item in all_items:
        occurrences[item] = [item in row for row in items_list]

    return occurrences
