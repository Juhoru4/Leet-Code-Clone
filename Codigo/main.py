from app import create_app
from app.extensions import db
from models import Usuario, Categoria, Problema, Envio, ResultadoEnvio, CasoPrueba
from routes.ejecucion_endpoint import ejecucion_bp
import os

# Crear la aplicación
app = create_app()
app.register_blueprint(ejecucion_bp)


@app.shell_context_processor
def make_shell_context():
    """Contexto para comandos flask shell"""
    return {
        'db': db,
        'Usuario': Usuario,
        'Categoria': Categoria,
        'Problema': Problema,
        'Envio': Envio,
        'ResultadoEnvio': ResultadoEnvio,
        'CasoPrueba': CasoPrueba,
    }


@app.cli.command("init-db")
def init_db_command():
    """Inicializa la base de datos creando todas las tablas"""
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada correctamente")
        print(f"  Se crearon las tablas: usuarios, categorias, problemas, envios")


@app.cli.command("drop-db")
def drop_db_command():
    """Elimina todas las tablas de la base de datos (¡cuidado!)"""
    if input("¿Estás seguro? Esto eliminará todas las tablas (s/n): ").lower() == 's':
        with app.app_context():
            db.drop_all()
            print("✓ Base de datos eliminada")
    else:
        print("Cancelado")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
