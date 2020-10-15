"""
a default sphinx configuration file

This file is execfile()d by Sphinx,
with the current directory set to its containing dir

.. seealso::  

    http://www.sphinx-doc.org/en/master/usage/configuration.html

"""

needs_sphinx = "1.6"

master_doc = "index"

source_suffix = {
    '.rst': 'restructuredtext',
    '.ipynb': 'jupyter_notebook',
    '.md': 'jupyter_notebook'
}

exclude_patterns = ['_build', 'build', '**.ipynb_checkpoints']

extensions = ['ipypublish.sphinx.notebook', 'ipypublish.sphinx.gls', 'sphinx.ext.mathjax', 'sphinxcontrib.bibtex', 'sphinx.ext.todo']

### where to find our custom material
# conf file itself
ipysphinx_config_folders = tuple(['.'])
# preprocessor module
import sys
sys.path.append('.')


# this is the config that ships with ipypublish
# ipysphinx_export_config = 'sphinx_ipypublish_all.ext'
# we added our own notes-outliner preprocessor
ipysphinx_export_config = 'sphinx_ipypublish_all.ext.custom'

ipysphinx_show_prompts = True
ipysphinx_input_prompt = 'In:'
ipysphinx_output_prompt = 'Out:'
ipysphinx_input_toggle = True
ipysphinx_output_toggle = True
html_theme = "sphinx_rtd_theme" 
html_title = "intro à Python" 
project = "Python numérique"
author = "Thierry Parmentelat & Valérie Roy"
html_theme_options = {
    'display_version': False,
}
todo_include_todos = False

numfig = True

numfig_secnum_depth = 2

numfig_format = {'section': 'Section %s', 'figure': 'Fig. %s', 'table': 'Table %s', 'code-block': 'Code Block %s'}

math_numfig = True

math_eqref_format = "eq.{number}"

linkcheck_ignore = ["r'http://localhost:\\d+/'"]

ipysphinx_show_prompts = True

ipysphinx_input_prompt = "[{count}]:"

ipysphinx_output_prompt = "[{count}]:"

