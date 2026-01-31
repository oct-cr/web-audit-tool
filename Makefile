.PHONY: docs lint fix

docs:
	rm -rf docs/_build docs/api
	sphinx-apidoc -f -o docs/api src
	sphinx-build -b html docs docs/_build/html
	@echo "Docs built at: docs/_build/html"

docs-open: docs
	open docs/_build/html/index.html

lint:
	ruff check src

fix:
	ruff check --fix src
