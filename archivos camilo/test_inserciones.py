"""
Script de prueba para insertar datos en los modelos ORM
"""
import uuid
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio Codigo al path
sys.path.insert(0, './Codigo')

from app import create_app
from app.extensions import db
from models import Usuario, Categoria, Problema, Envio, ResultadoEnvio, CasoPrueba

# Crear aplicación
app = create_app()

def test_inserciones():
    """Prueba insertando datos en todos los modelos"""
    
    timestamp = str(int(time.time()))
    
    with app.app_context():
        try:
            print("\n" + "="*60)
            print("🧪 PRUEBA DE INSERCIONES DE DATOS")
            print("="*60)
            
            # 1. Crear una Categoría
            print("\n1️⃣ Insertando Categoría...")
            categoria_id = str(uuid.uuid4())
            categoria = Categoria(
                id=categoria_id,
                nombre=f"Algoritmos {timestamp}",
                slug=f"algoritmos-{timestamp}",
                descripcion="Problemas sobre algoritmos y optimización.",
                creado_el=datetime.utcnow()
            )
            db.session.add(categoria)
            db.session.commit()
            print(f"   ✓ Categoría creada: {categoria.nombre} (ID: {categoria.id})")
            
            # 2. Crear un Usuario (Perfil)
            # NOTA: El ID debe ser un UUID válido de Supabase Auth (auth.users.id)
            # Para esta prueba, usamos un UUID existente o generado
            print("\n2️⃣ Insertando Usuario (Perfil)...")
            usuario_id = str(uuid.uuid4())  # En producción, este sería el UUID de auth.users
            usuario = Usuario(
                id=usuario_id,
                nombre_usuario="juan_perez",
                nombre_completo="Juan Carlos Pérez García",
                rol="estudiante",
                creado_el=datetime.utcnow()
            )
            # NOTA: Si sale error de FK, es porque el UUID no existe en auth.users de Supabase
            # En producción, el ID vendría de Supabase Auth después del registro
            try:
                db.session.add(usuario)
                db.session.commit()
                print(f"   ✓ Usuario creado: {usuario.nombre_usuario}")
                print(f"   - ID: {usuario.id}")
                print(f"   - Rol: {usuario.rol}")
            except Exception as e:
                db.session.rollback()
                print(f"   ⚠️  No se pudo crear el usuario (FK a auth.users)")
                print(f"      Esto es normal en pruebas. El ID debe existir en Supabase Auth.")
                print(f"      Continuando con el resto de las pruebas...")
                # Usamos un UUID existente para las siguientes pruebas
                usuario_id = None
            
            # 3. Crear un Problema
            print("\n3️⃣ Insertando Problema...")
            problema_id = str(uuid.uuid4())
            problema = Problema(
                id=problema_id,
                titulo="Invertir una Lista",
                descripcion="Escribe una función que invierta los elementos de una lista sin usar métodos built-in de inversión.",
                dificultad="easy",  # 'easy', 'medium', 'hard' son los valores válidos
                categoria_id=categoria_id,
                restricciones="No puedes usar .reverse() o [::-1]",
                ejemplo_entrada="[1, 2, 3, 4, 5]",
                ejemplo_salida="[5, 4, 3, 2, 1]",
                limite_tiempo_ms=2000,
                limite_memoria_mb=128,
                esta_activo=True,
                creado_por=usuario_id,  # Puede ser None
                creado_el=datetime.utcnow()
            )
            db.session.add(problema)
            db.session.commit()
            print(f"   ✓ Problema creado: {problema.titulo}")
            print(f"   - ID: {problema.id}")
            print(f"   - Dificultad: {problema.dificultad}")
            print(f"   - Categoría: {problema.categoria.nombre}")
            
            # 4. Crear casos de prueba
            print("\n4️⃣ Insertando Casos de Prueba...")
            caso1_id = str(uuid.uuid4())
            caso1 = CasoPrueba(
                id=caso1_id,
                problema_id=problema_id,
                entrada="[1, 2, 3, 4, 5]",
                salida_esperada="[5, 4, 3, 2, 1]",
                descripcion="Caso de prueba básico",
                es_publico=True,
                orden=1,
                creado_el=datetime.utcnow()
            )
            db.session.add(caso1)
            db.session.commit()
            print(f"   ✓ Caso de prueba creado")
            
            # 5. Crear un Envío (solo si tenemos usuario)
            if usuario_id:
                print("\n5️⃣ Insertando Envío...")
                envio_id = str(uuid.uuid4())
                envio = Envio(
                    id=envio_id,
                    usuario_id=usuario_id,
                    problema_id=problema_id,
                    codigo_fuente="def invertir_lista(arr):\n    for i in range(len(arr)//2):\n        arr[i], arr[-(i+1)] = arr[-(i+1)], arr[i]\n    return arr",
                    lenguaje="python",
                    estado="completado",
                    total_casos=1,
                    casos_pasados=1,
                    tiempo_ejecucion_ms=45,
                    memoria_usada_kb=2048,
                    mensaje_error=None,
                    enviado_el=datetime.utcnow()
                )
                db.session.add(envio)
                db.session.commit()
                print(f"   ✓ Envío creado: ID {envio.id}")
                print(f"   - Usuario: {envio.usuario.nombre_usuario}")
                print(f"   - Problema: {envio.problema.titulo}")
                print(f"   - Lenguaje: {envio.lenguaje}")
                print(f"   - Estado: {envio.estado}")
                print(f"   - Casos pasados: {envio.casos_pasados}/{envio.total_casos}")
                
                # 6. Crear Resultados de Envío
                print("\n6️⃣ Insertando Resultados de Envío...")
                resultado1_id = str(uuid.uuid4())
                resultado1 = ResultadoEnvio(
                    id=resultado1_id,
                    envio_id=envio_id,
                    caso_prueba_id=caso1_id,
                    estado="aprobado",
                    salida_real="[5, 4, 3, 2, 1]",
                    tiempo_ejecucion_ms=15,
                    mensaje_error=None,
                    creado_el=datetime.utcnow()
                )
                db.session.add(resultado1)
                db.session.commit()
                print(f"   ✓ Resultado de Envío creado: {resultado1.estado}")
            else:
                print("\n⏭️  Omitiendo Envíos (sin usuario)")
            
            # 7. Consultar datos
            print("\n" + "="*60)
            print("📊 VERIFICANDO DATOS INSERTADOS")
            print("="*60)
            
            print("\n📋 Categorías en BD:")
            categorias = Categoria.query.all()
            for cat in categorias[:3]:  # Mostrar primeras 3
                print(f"  - {cat.nombre} ({cat.slug})")
                print(f"    Descripción: {cat.descripcion}")
            
            print("\n👥 Usuarios en BD:")
            usuarios = Usuario.query.all()
            for user in usuarios[-3:]:  # Mostrar últimos 3
                print(f"  - {user.nombre_usuario} (Rol: {user.rol})")
            
            print("\n📚 Problemas en BD:")
            problemas = Problema.query.all()
            for prob in problemas[-3:]:  # Mostrar últimos 3
                print(f"  - {prob.titulo} ({prob.dificultad})")
                print(f"    Categoría: {prob.categoria.nombre}")
            
            print("\n📝 Casos de Prueba en BD:")
            casos = CasoPrueba.query.all()
            for caso in casos[-3:]:  # Mostrar últimos 3
                print(f"  - Caso ID: {caso.id}")
                print(f"    Entrada: {caso.entrada}")
                print(f"    Salida esperada: {caso.salida_esperada}")
            
            print("\n📤 Envíos en BD:")
            envios = Envio.query.all()
            for env in envios[-3:]:  # Mostrar últimos 3
                print(f"  - Envío ID: {env.id}")
                print(f"    Usuario: {env.usuario.nombre_usuario}")
                print(f"    Problema: {env.problema.titulo}")
                print(f"    Lenguaje: {env.lenguaje}")
                print(f"    Estado: {env.estado}")
            
            print("\n📈 Resultados de Envíos en BD:")
            resultados = ResultadoEnvio.query.all()
            for res in resultados[-3:]:  # Mostrar últimos 3
                print(f"  - Resultado ID: {res.id}")
                print(f"    Envío: {res.envio_id}")
                print(f"    Estado: {res.estado}")
            
            print("\n" + "="*60)
            print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n❌ ERROR DURANTE LA PRUEBA: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == "__main__":
    test_inserciones()
