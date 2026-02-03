from collections.abc import Iterable


def get_occurrences(items: Iterable[Iterable[str]]):
    items_list = list(items)
    all_items = sorted({it for row in items_list for it in row})

    occurrences: dict[str, list[bool]] = {}
    discrepancies: dict[str, list[bool]] = {}
    common = []

    for item in all_items:
        occurrences[item] = [item in row for row in items_list]

    for item, presence_list in occurrences.items():
        if all(presence_list):
            common.append(item)
            continue

        if any(presence_list):
            discrepancies[item] = presence_list

    return {
        "occurrences": occurrences,
        "discrepancies": discrepancies,
        "common": common,
    }
