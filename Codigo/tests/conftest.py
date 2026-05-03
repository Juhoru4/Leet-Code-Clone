import sys
from pathlib import Path

# Agregar el directorio Codigo al path para que los imports funcionen
codigo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(codigo_dir))
