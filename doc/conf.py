# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import inspect
from datetime import date
from importlib import import_module
from typing import Dict, Optional

import whippersnappy

# from sphinx_gallery.sorting import FileNameSortKey


project = "whippersnappy"
author = "Martin Reuter"
copyright = f"{date.today().year}, {author}"
release = whippersnappy.__version__
package = whippersnappy.__name__
gh_url = "https://github.com/Deep-MI/WhipperSnapPy"


# -- general configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "5.0"

# The document name of the “root” document, that is, the document that contains
# the root toctree directive.
root_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "sphinx_design",
    "IPython.sphinxext.ipython_console_highlighting",
    "numpydoc",
]

# Backup extensions
# "sphinxcontrib.napoleon",
#   "sphinx.ext.napoleon",
#  "sphinx_gallery.gen_gallery",


numpydoc_show_class_members = False

# Whether to create a Sphinx table of contents for the lists of class methods and attributes. If a table of contents is made,
# Sphinx expects each entry to have a separate page. True by default.
# numpydoc_class_members_toctree = False


# Napoleon settings
# I added these two lines because i added sphinx.ext.napolon in the extension after
# Commenting out sphinxcontrib.napoleon in the extension
# napoleon_google_docstring = False
# napoleon_numpy_docstring = True

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "tutorials/examples/README.rst",
]

# Sphinx will warn about all references where the target cannot be found.
# nitpicky = True
nitpicky = False
nitpick_ignore = []

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = [f"{package}."]

# The name of a reST role (builtin or Sphinx extension) to use as the default
# role, that is, for text marked up `like this`. This can be set to 'py:obj' to
# make `filter` a cross-reference to the Python function “filter”.
default_role = "py:obj"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_title = project
html_show_sphinx = False


# Documentation to change footer icons:
# https://pradyunsg.me/furo/customisation/footer/#changing-footer-icons
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": gh_url,
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}


# -- autosummary -------------------------------------------------------------
autosummary_generate = True

# -- autodoc -----------------------------------------------------------------
autodoc_typehints = "none"
autodoc_member_order = "groupwise"
autodoc_warningiserror = True
autoclass_content = "class"


# -- intersphinx -------------------------------------------------------------
intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/stable", None),
    "mne": ("https://mne.tools/stable/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}

intersphinx_timeout = 5


# -- sphinx-issues -----------------------------------------------------------
issues_github_path = gh_url.split("https://github.com/")[-1]

# -- autosectionlabels -------------------------------------------------------
autosectionlabel_prefix_document = True

# -- sphinxcontrib-bibtex ----------------------------------------------------
bibtex_bibfiles = ["./references.bib"]

# -- sphinx.ext.linkcode -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html


def linkcode_resolve(domain: str, info: Dict[str, str]) -> Optional[str]:
    """Determine the URL corresponding to a Python object.

    Parameters
    ----------
    domain : str
        One of 'py', 'c', 'cpp', 'javascript'.
    info : dict
        With keys "module" and "fullname".

    Returns
    -------
    url : str | None
        The code URL. If None, no link is added.
    """
    if domain != "py":
        return None  # only document python objects

    # retrieve pyobject and file
    try:
        module = import_module(info["module"])
        pyobject = module
        for elt in info["fullname"].split("."):
            pyobject = getattr(pyobject, elt)
        fname = inspect.getsourcefile(pyobject).replace("\\", "/")
    except Exception:
        # Either the object could not be loaded or the file was not found.
        # For instance, properties will raise.
        return None

    # retrieve start/stop lines
    source, start_line = inspect.getsourcelines(pyobject)
    lines = "L%d-L%d" % (start_line, start_line + len(source) - 1)

    # create URL
    if "dev" in release:
        branch = "main"
    else:
        return None  # alternatively, link to a maint/version branch
    fname = fname.rsplit(f"/{package}/")[1]
    url = f"{gh_url}/blob/{branch}/{package}/{fname}#{lines}"
    return url


# # -- sphinx-gallery ----------------------------------------------------------
# sphinx_gallery_conf = {
#     "backreferences_dir": "generated/backreferences",
#     "doc_module": (f"{package}",),
#     "examples_dirs": ["generated/examples"],
#     "exclude_implicit_doc": {},  # set
#     "filename_pattern": r"\d{2}_",
#     "gallery_dirs": ["generated/examples"],
#     "line_numbers": False,
#     "plot_gallery": True,
#     "reference_url": {f"{package}": None},
#     "remove_config_comments": True,
#     "show_memory": True,
#     "within_subsection_order": FileNameSortKey,
# }


import os

# -- make sure pandoc gets installed -----------------------------------------
from inspect import getsourcefile

# Get path to directory containing this file, conf.py.
DOCS_DIRECTORY = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))


def ensure_pandoc_installed(_):
    import pypandoc

    # Download pandoc if necessary. If pandoc is already installed and on
    # the PATH, the installed version will be used. Otherwise, we will
    # download a copy of pandoc into docs/bin/ and add that to our PATH.
    pandoc_dir = os.path.join(DOCS_DIRECTORY, "bin")
    # Add dir containing pandoc binary to the PATH environment variable
    if pandoc_dir not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + pandoc_dir
    pypandoc.ensure_pandoc_installed(
        targetfolder=pandoc_dir,
        delete_installer=True,
    )


def setup(app):
    app.connect("builder-inited", ensure_pandoc_installed)


# def autodoc_skip_member(app, what, name, obj, skip, options):
#     # List of method names to skip
#     methods_to_skip = [
#         'actions',
#         # Add other method names to skip here
#     ]

#     print("autodoc_skip_member called with:", what, name)

#     # Check if the member is a method and in the list of methods to skip
#     if what == 'method' and name in methods_to_skip:
#         print("Skipping method:", name)
#         return True

#     return None
