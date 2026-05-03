"""Paquete principal del proyecto.

Expone aliases para que el proyecto funcione tanto ejecutando scripts desde
la raíz con `Codigo` en `sys.path` como usando Flask CLI con `Codigo.main`.
"""

from importlib import import_module
import sys


if 'app' in sys.modules:
	app_module = sys.modules['app']
else:
	app_module = import_module('Codigo.app')

sys.modules.setdefault('app', app_module)
sys.modules['Codigo.app'] = app_module

if 'app.extensions' in sys.modules:
	extensions_module = sys.modules['app.extensions']
else:
	extensions_module = import_module('Codigo.app.extensions')

sys.modules.setdefault('app.extensions', extensions_module)
sys.modules['Codigo.app.extensions'] = extensions_module

if 'models' in sys.modules:
	models_module = sys.modules['models']
else:
	models_module = import_module('Codigo.models')

sys.modules.setdefault('models', models_module)
sys.modules['Codigo.models'] = models_module

if 'routes' in sys.modules:
	routes_module = sys.modules['routes']
else:
	routes_module = import_module('Codigo.routes')

sys.modules.setdefault('routes', routes_module)
sys.modules['Codigo.routes'] = routes_module

if 'services' in sys.modules:
	services_module = sys.modules['services']
else:
	services_module = import_module('Codigo.services')

sys.modules.setdefault('services', services_module)
sys.modules['Codigo.services'] = services_module
