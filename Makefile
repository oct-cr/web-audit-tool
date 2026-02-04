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
	vulture dashkit/ --min-confidence 60 --ignore-names "TITLE,CSS,compose,on_mount,on_list_view_highlighted,on_key"

docs-deps:
	pydeps dashkit -o docs/dependency-graph.svg --noshow --cluster --max-bacon 2 --reverse --rankdir=RL --rmprefix dashkit.

mypy:
	mypy dashkit --config-file mypy.ini

test:
	pytest dashkit -q

precommit: check docs-deps
