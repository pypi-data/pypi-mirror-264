"""Sphinx configuration file."""

import lod_unit

project = "lod_unit"
copyright = "2024, Corey Spohn"
author = "Corey Spohn"
version = lod_unit.__version__
release = lod_unit.__version__

# -- General configuration ---------------------------------------------------

extensions = ["myst_parser", "autoapi.extension", "sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "Python"

autoapi_dirs = ["../src"]
autoapi_ignore = ["**/version.py"]
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
master_doc = "index"
