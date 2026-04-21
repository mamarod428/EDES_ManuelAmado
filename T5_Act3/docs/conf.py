import os
import sys
# Aseguramos que Sphinx mire en la carpeta superior donde está main.py
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Monitor ISS'
copyright = '2026, Manuel Amado Rodriguez'
author = 'Manuel Amado Rodriguez'

# -- General configuration ---------------------------------------------------
# Añadimos las extensiones necesarias (SOLO UNA VEZ)
extensions = [
    'sphinx.ext.autodoc',     # Para leer los docstrings
    'sphinx.ext.napoleon',    # Para soportar formatos Google/NumPy
    'sphinx.ext.viewcode',    # Opcional: añade enlaces al código fuente
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# Usamos el tema 'sphinx_rtd_theme' que es el más profesional
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']