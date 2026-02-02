from .utils import get_occurrences


def test_get_occurrences_by_presence():
    assert get_occurrences(
        [
            ["a", "c"],
            ["b", "c"],
            ["a", "b", "c"],
            [],
        ]
    ) == {
        "a": [True, False, True, False],
        "b": [False, True, True, False],
        "c": [True, True, True, False],
    }
