import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../../dashkit"))

project = "Web Audit Tool"
copyright = "2026"
author = "Octavio Coria"

extensions = [
    "sphinx.ext.autodoc",
]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "show-inheritance": True,
}

toc_object_entries_show_parents = "all"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinxdoc"
html_theme_options = {
    "nosidebar": True,
}
html_static_path = ["_static"]
