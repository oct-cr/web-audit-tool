.PHONY: docs

docs:
	rm -rf docs/_build docs/api
	sphinx-apidoc -f -o docs/api src
	sphinx-build -b html docs docs/_build/html
	@echo "Docs built at: docs/_build/html"

docs-open: docs
	open docs/_build/html/index.html

check: lint deadcode

lint:
	ruff check src

fix:
	ruff check --fix src

deadcode:
	vulture src/ --min-confidence 80

docs-deps:
	pydeps src --cluster --max-bacon 3 -o docs/_build/dependencies.svg --noshow