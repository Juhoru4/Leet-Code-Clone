#!/usr/bin/env python
"""
Script para inicializar la base de datos
Ejecutar desde: python -m Codigo.initialize_db
o desde Codigo/: python initialize_db.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def init_database():
    """Inicializa la base de datos y crea todas las tablas"""
    try:
        from app import create_app
        from app.extensions import db
        from models import Usuario, Categoria, Problema, Envio
        
        print("=" * 60)
        print("INICIALIZACIÓN DE BASE DE DATOS")
        print("=" * 60)
        print()
        
        app = create_app()
        
        with app.app_context():
            print("📊 Creando tablas...")
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            print()
            print("Tablas disponibles:")
            print("  - usuarios")
            print("  - categorias")
            print("  - problemas")
            print("  - envios")
            print()
            print("=" * 60)
            print("✓ Base de datos lista para usar")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
