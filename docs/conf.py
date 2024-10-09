# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import pyhepmc
import os

project = "pyhepmc"
copyright = "2022, Hans Dembinski"
author = "Hans Dembinski"
version = release = pyhepmc.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

# templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

# Import and set the theme if we're building docs locally
import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"

# Autodoc options
autodoc_member_order = "groupwise"
autodoc_mock_imports = ["numpy", "particle"]
