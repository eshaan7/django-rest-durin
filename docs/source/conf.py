# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import django

# I've simplified this a little to use append instead of insert.
sys.path.append(os.path.abspath("../../"))

# Specify settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

# Setup Django
django.setup()


# -- Project information -----------------------------------------------------

project = "Django-Rest-Durin"
copyright = "2020, Eshaan Bansal"
author = "Eshaan Bansal"

version = "0.1.0"
# The full version, including alpha/beta/rc tags
release = "v0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
]

source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [
    "_themes",
]

# Custom options

# html_context = {
#     "project_links": [
#         ProjectLink("Donate To The Author", "https://paypal.me/eshaanbansal"),
#         ProjectLink(f"{project} Website", f"https://{project}.readthedocs.io/"),
#         ProjectLink("PyPI releases", f"https://pypi.org/project/{project}/"),
#         ProjectLink("Source Code", f"https://github.com/eshaan7/{project}"),
#         ProjectLink("Issue Tracker", f"https://github.com/eshaan7/{project}/issues"),
#     ]
# }
html_sidebars = {
    "index": ["localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["localtoc.html"]}
html_title = f"{project} Documentation ({release})"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
