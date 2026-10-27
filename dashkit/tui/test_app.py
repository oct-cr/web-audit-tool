import asyncio
from typing import Any

from .app import DashkitApp


def test_history_binding_toggles_history_mode() -> None:
    asyncio.run(_test_history_binding())


async def _test_history_binding() -> None:
    workspace: dict[str, Any] = {
        "key": "missing",
        "sites": {
            "site": {
                "name": "Site",
                "pages": {"page": {"url": "https://example.test"}},
            }
        },
    }
    app = DashkitApp(workspace, initial_route="site:page")

    async with app.run_test() as pilot:
        await pilot.press("h")
        assert app.history_mode

        await pilot.press("escape")
        assert not app.history_mode
