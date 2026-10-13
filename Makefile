PYDEPS_VERSION := 3.0.2
GRAPHVIZ_VERSION := 14.1.2

.PHONY: docs

docs:
	rm -rf _build/docs
	sphinx-apidoc -f -o utils/docs/api dashkit
	sphinx-build -b html utils/docs _build/docs/html
	@echo "Docs built at: _build/docs/html"

docs-open: docs
	open _build/docs/html/index.html

check: lint test deadcode mypy

lint:
	ruff check dashkit

fix:
	ruff check --fix dashkit

deadcode:
	vulture dashkit/ --min-confidence 60 --ignore-names "TITLE,CSS,BINDINGS,compose,on_mount,on_list_view_highlighted,on_key,action_*" --exclude '*/screenshot_*.py'

docs-deps:
	@pydeps --version | grep -Fx "pydeps v$(PYDEPS_VERSION)" >/dev/null || { echo "docs-deps requires pydeps $(PYDEPS_VERSION)" >&2; exit 1; }
	@dot -V 2>&1 | grep -Fq "graphviz version $(GRAPHVIZ_VERSION)" || { echo "docs-deps requires Graphviz $(GRAPHVIZ_VERSION)" >&2; exit 1; }
	pydeps dashkit -o docs/dependency-graph.svg --noshow --cluster --max-bacon 2 --reverse --rankdir=RL --rmprefix dashkit. -x 'dashkit.*.screenshot_*'
	python utils/deps-chart.py

docs-screenshots:
	python utils/screenshot_runner.py

mypy:
	mypy dashkit --config-file mypy.ini

test:
	pytest dashkit utils -q

precommit: check docs-deps docs-screenshots
