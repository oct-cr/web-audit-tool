SPHINXBUILD   ?= sphinx-build
SPHINXAPIDOC  ?= sphinx-apidoc
SOURCEDIR     = .
BUILDDIR      = _build
SRCDIR        = ../dashkit

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile apidoc clean

clean:
	@rm -rf "$(BUILDDIR)" api

apidoc: clean
	@cd "$(SRCDIR)" && $(SPHINXAPIDOC) -f -o "../docs/api" . --implicit-namespaces

%: Makefile apidoc
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
