"""Sphinx configuration."""
project = "CoffiFilter"
author = "Shishir Jakati"
copyright = "2024, Shishir Jakati"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
