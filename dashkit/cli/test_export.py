import pytest

from .export import _resolve_targets

_WORKSPACE = {
    "key": "demo",
    "sites": {
        "acme": {
            "name": "Acme",
            "pages": {
                "frontpage": {"url": "https://acme.test/"},
                "product": {"url": "https://acme.test/p"},
            },
        },
    },
}


def test_resolve_targets_single_page():
    targets = _resolve_targets(_WORKSPACE, "acme:product", all_sites=False)

    assert [(sk, p["key"]) for sk, p in targets] == [("acme", "product")]


def test_resolve_targets_site_expands_to_pages():
    targets = _resolve_targets(_WORKSPACE, "acme", all_sites=False)

    assert {p["key"] for _, p in targets} == {"frontpage", "product"}


def test_resolve_targets_all_sites():
    targets = _resolve_targets(_WORKSPACE, None, all_sites=True)

    assert len(targets) == 2


def test_resolve_targets_no_route_is_empty():
    assert _resolve_targets(_WORKSPACE, None, all_sites=False) == []


def test_resolve_targets_bad_page_raises():
    with pytest.raises(ValueError, match="Route not found"):
        _resolve_targets(_WORKSPACE, "acme:nope", all_sites=False)
