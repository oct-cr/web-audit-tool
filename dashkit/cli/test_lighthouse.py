import pytest

from .lighthouse import run_lighthouse

_WORKSPACE = {
    "key": "demo",
    "sites": {
        "acme": {"name": "Acme", "pages": {}},
        "example": {"name": "Example", "pages": {}},
    },
}


def test_run_lighthouse_reports_missing_site_with_available_sites(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = run_lighthouse(_WORKSPACE, "missing", ["--dry"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == (
        "Error: Site not found for key: missing\n"
        "Available sites:\n"
        "- acme\n"
        "- example\n"
    )
