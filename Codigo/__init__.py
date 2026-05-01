"""Paquete principal del proyecto.

Expone aliases para que el proyecto funcione tanto ejecutando scripts desde
la raíz con `Codigo` en `sys.path` como usando Flask CLI con `Codigo.main`.
"""

from importlib import import_module
import sys


app_module = import_module('Codigo.app')
extensions_module = import_module('Codigo.app.extensions')
sys.modules['app'] = app_module
sys.modules['Codigo.app'] = app_module
sys.modules['app.extensions'] = extensions_module
sys.modules['Codigo.app.extensions'] = extensions_module

models_module = import_module('Codigo.models')
sys.modules['models'] = models_module
sys.modules['Codigo.models'] = models_module
