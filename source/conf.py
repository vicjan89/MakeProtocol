# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'protocol'
copyright = '2023, ООО Электротехнические Решения'
author = 'ООО Электротехнические Решения'
# release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

pris = (('grodno_tec2_devatovka', 'grodno_tec2_devatovka.tex', 'Протокол профвосстановления РЗА ВЛ-110кВ Девятовка Гродненской ТЭЦ-2', '23.09.2023'),
        ('grodno_tec2_jugnaja1', 'grodno_tec2_jugnaja1.tex', 'Протокол профвосстановления РЗА ВЛ-110кВ Южная-1 Гродненской ТЭЦ-2', '16.09.2023'),
        ('grodno_tec2_T-5', '', 'Протокол профилактического контроля РЗА трансформатора Т-5 Гродненской ТЭЦ-2', '02.08.2023'))
num = 1
today = pris[num][3]
root_doc = pris[num][0]
language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
#-- Options for LaTeX output -------------------------------------------------
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',
    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
    'extraclassoptions': 'openany', #'manual',
    'figure_align': 'H', # исключило непопадание рисунков в границы страницы
}
engines = ('pdflatex', 'xelatex', 'lualatex', 'platex', 'uplatex')
latex_engine = engines[2]
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
theme = ('manual', 'howto')[1]
latex_documents = [
    (root_doc, pris[num][0]+'.tex', pris[num][2], 'ООО Электротехнические Решения', theme),
]
latex_table_style = ['standart']

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
latex_logo = '_static/ER.png'

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# If false, no module index is generated.
#
# latex_domain_indices = True
