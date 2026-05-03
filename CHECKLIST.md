# ✅ CHECKLIST DE CONFIGURACIÓN

Sigue estos pasos para verificar que todo está correctamente configurado.

## PASO 1: Verificar archivos ✓

- [ ] `Codigo/app/__init__.py` - Contiene `create_app()`
- [ ] `Codigo/app/extensions.py` - Contiene `db = SQLAlchemy()`
- [ ] `Codigo/config.py` - Configuración (Dev, Prod, Testing)
- [ ] `Codigo/main.py` - Punto de entrada con CLI commands
- [ ] `Codigo/models/__init__.py` - Importa todos los modelos
- [ ] `Codigo/models/usuario.py` - Modelo Usuario (ORM)
- [ ] `Codigo/models/categoria.py` - Modelo Categoría (ORM)
- [ ] `Codigo/models/problema.py` - Modelo Problema (ORM)
- [ ] `Codigo/models/envio.py` - Modelo Envío (ORM)
- [ ] `.env` - Variables de entorno

## PASO 2: Verificar dependencias ✓

```bash
# Ejecutar en la terminal
pip list | findstr "Flask SQLAlchemy psycopg2"
```

Deberías ver:
- [ ] Flask (version 3.1.0+)
- [ ] Flask-SQLAlchemy (version 3.1.0+)
- [ ] SQLAlchemy (version 2.0.0+)
- [ ] psycopg2-binary (version 2.9.0+)
- [ ] python-dotenv (version 1.0.0+)

## PASO 3: Configurar Supabase ✓

1. [ ] Ir a https://supabase.com/dashboard
2. [ ] Crear o seleccionar un proyecto
3. [ ] Ir a **Settings → Database** (en el proyecto)
4. [ ] Copiar la información:
   - [ ] Host: `db.xxxx.supabase.co`
   - [ ] Password: Tu contraseña de BD
   - [ ] User: `postgres`

## PASO 4: Actualizar .env ✓

Editar `d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone\.env`

```env
# Ejemplo con valores reales
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=TU_CONTRASEÑA  ← REEMPLAZAR
SUPABASE_DB_HOST=db.abcdefgh.supabase.co  ← REEMPLAZAR
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres

DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@db.abcdefgh.supabase.co:5432/postgres?sslmode=require
```

- [ ] URL actualizada con tus credenciales reales
- [ ] No hay espacios en blanco al principio/final
- [ ] `sslmode=require` está presente

## PASO 5: Instalar dependencias ✓

```bash
cd d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone
pip install -r requirements.txt
```

- [ ] Instalación completada sin errores
- [ ] Todas las librerías instaladas correctamente

## PASO 6: Probar conexión ✓

```bash
cd d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone
python test_connection.py
```

Deberías ver:
```
✓ Variables de entorno
✓ Importar modelos
✓ Conexión a base de datos
```

- [ ] Test de variables de entorno ✓
- [ ] Test de importación de modelos ✓
- [ ] Test de conexión a BD ✓

Si falla el test de conexión:
1. [ ] Verifica las credenciales en `.env`
2. [ ] Asegúrate de que el proyecto Supabase está activo
3. [ ] Verifica que la contraseña sea correcta

## PASO 7: Inicializar base de datos ✓

```bash
cd d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone\Codigo
python main.py init-db
```

Deberías ver:
```
✓ Base de datos inicializada correctamente
  Se crearon las tablas: usuarios, categorias, problemas, envios
```

- [ ] Comando ejecutado sin errores
- [ ] Se crearon las 4 tablas

Verifica en Supabase (https://supabase.com/dashboard):
1. [ ] Ir a tu proyecto → **Tables**
2. [ ] [ ] Tabla `usuarios` existe
3. [ ] Tabla `categorias` existe
4. [ ] Tabla `problemas` existe
5. [ ] Tabla `envios` existe

## PASO 8: Probar con datos ✓

```bash
cd d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone
# Abre la shell interactiva
flask --app Codigo/main shell
```

Dentro de la shell, ejecuta:

```python
from app.models import Usuario, Categoria
from app.extensions import db

# Crear una categoría
cat = Categoria(nombre="Arrays", slug="arrays")
db.session.add(cat)
db.session.commit()
print(f"Categoría creada: {cat.id}")

# Crear un usuario
usuario = Usuario(
    nombre="Test",
    email="test@example.com",
    password_hash="hash123",
    rol="user"
)
db.session.add(usuario)
db.session.commit()
print(f"Usuario creado: {usuario.id}")

# Consultar
usuarios = Usuario.query.all()
print(f"Total usuarios: {len(usuarios)}")
```

- [ ] Categoría creada sin errores
- [ ] Usuario creado sin errores
- [ ] Consulta devuelve los datos

Verifica en Supabase (https://supabase.com/dashboard):
1. [ ] Ir a tu proyecto → **Tables**
2. [ ] [ ] Tabla `usuarios` → Ver si aparece el usuario creado
3. [ ] Tabla `categorias` → Ver si aparece la categoría creada

## PASO 9: Probar ejemplos ✓

```bash
cd d:\Universidad\Semestre4\LaboratorioSoftware3\Leet-Code-Clone

# Editar ejemplos_uso.py
# Descomentar las funciones que quieras probar
# Por ejemplo:
# ejemplo_crear_usuario()
# ejemplo_consultar_usuarios()

python ejemplos_uso.py
```

- [ ] Ejemplos ejecutados sin errores

## PASO 10: Estar listo para producción ✓

- [ ] Todos los archivos de configuración creados
- [ ] Todas las dependencias instaladas
- [ ] Conexión a Supabase verificada
- [ ] Tablas creadas en la base de datos
- [ ] Datos de prueba insertados correctamente
- [ ] Consultas funcionando correctamente

## ⚠️ Solución de problemas

### Error: "could not translate host name"
- [ ] Verifica que el host en `.env` sea correcto
- [ ] Verifica que tu proyecto Supabase está activo
- [ ] Intenta hacer ping al host (si tienes permisos)

### Error: "authentication failed for user postgres"
- [ ] Verifica la contraseña en `.env`
- [ ] Ve a Supabase → Settings → Database → Connection String
- [ ] Copia exactamente la contraseña (sin comillas)

### Error: "relation usuarios does not exist"
- [ ] Ejecuta `python main.py init-db` nuevamente
- [ ] Verifica en Supabase que las tablas existan

### Error: "No module named app"
- [ ] Asegúrate de estar en la carpeta correcta
- [ ] Verifica que exista `Codigo/app/__init__.py`
- [ ] Intenta agregar la ruta al PATH:
  ```python
  import sys
  sys.path.insert(0, 'Codigo')
  ```

### Error: "SSL connection failed"
- [ ] Verifica que `sslmode=require` esté en DATABASE_URL
- [ ] Actualiza psycopg2-binary: `pip install --upgrade psycopg2-binary`

## 🎉 ¡Completado!

Si has marcado todos los checkbox, ¡tu aplicación está lista para usar!

### Próximas acciones:
1. Crea más modelos si es necesario
2. Desarrolla tus rutas Flask
3. Agrega validaciones y lógica de negocio
4. Despliega a producción

---

**Documentación útil:**
- RESUMEN_CONFIGURACION.md - Resumen general
- CONFIGURACION_SUPABASE.md - Guía completa
- ARQUITECTURA.md - Diagrama de la arquitectura
- ejemplos_uso.py - Ejemplos de código

¡Buena suerte! 🚀
