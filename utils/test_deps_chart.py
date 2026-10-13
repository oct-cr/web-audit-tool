import importlib.util
from pathlib import Path
from types import ModuleType


def load_deps_chart() -> ModuleType:
    script_path = Path(__file__).with_name("deps-chart.py")
    spec = importlib.util.spec_from_file_location("deps_chart", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_graph_resolves_package_relative_imports(tmp_path: Path) -> None:
    package = tmp_path / "dashkit" / "modules" / "lighthouse"
    widgets = package / "widgets"
    widgets.mkdir(parents=True)
    (tmp_path / "dashkit" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "dashkit" / "modules" / "__init__.py").write_text("", encoding="utf-8")
    (package / "__init__.py").write_text(
        "from . import widgets\nfrom .runner import run_lighthouse_report\n",
        encoding="utf-8",
    )
    (package / "runner.py").write_text("", encoding="utf-8")
    (widgets / "__init__.py").write_text("", encoding="utf-8")

    _, edges = load_deps_chart().build_graph(tmp_path)

    assert ("dashkit.modules.lighthouse", "dashkit.modules.lighthouse.runner") in edges
    assert ("dashkit.modules.lighthouse", "dashkit.modules.lighthouse.widgets") in edges
    assert ("dashkit.modules.lighthouse", "dashkit.modules") not in edges
