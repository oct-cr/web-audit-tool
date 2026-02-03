from .utils import get_occurrences


def test_get_occurrences_by_presence():
    result = get_occurrences(
        [
            ["a", "c"],
            ["b", "c"],
            ["a", "b", "c"],
            [],
        ]
    )

    assert result["occurrences"] == {
        "a": [True, False, True, False],
        "b": [False, True, True, False],
        "c": [True, True, True, False],
    }


def test_get_discrepancies_by_presence():
    result = get_occurrences(
        [
            ["a", "c"],
            ["b", "c"],
            ["a", "b", "c"],
        ]
    )

    assert result["discrepancies"] == {
        "a": [True, False, True],
        "b": [False, True, True],
    }


def test_get_common_by_presence():
    result = get_occurrences(
        [
            ["a", "c"],
            ["b", "c"],
            ["a", "b", "c"],
        ]
    )

    assert result["common"] == ["c"]
