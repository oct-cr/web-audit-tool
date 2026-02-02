.PHONY: docs

docs:
	rm -rf docs/_build docs/api
	sphinx-apidoc -f -o docs/api dashkit
	sphinx-build -b html docs docs/_build/html
	@echo "Docs built at: docs/_build/html"

docs-open: docs
	open docs/_build/html/index.html

check: lint test deadcode mypy

lint:
	ruff check dashkit

fix:
	ruff check --fix dashkit

deadcode:
	vulture dashkit/ --min-confidence 60 --ignore-names "TITLE,CSS,compose,on_mount,on_list_view_highlighted,on_key"

docs-deps:
	pydeps dashkit -o docs/dependency-graph.svg --noshow --cluster --max-bacon 2 --reverse --rankdir=RL

mypy:
	mypy dashkit --config-file mypy.ini

test:
	pytest dashkit -q
