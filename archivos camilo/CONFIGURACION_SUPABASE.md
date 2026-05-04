# Guía de Configuración: Conectar Flask + SQLAlchemy con Supabase

## 🚀 Pasos para configurar tu aplicación

### 1. Obtener credenciales de Supabase

1. Ve a [https://supabase.com](https://supabase.com) y crea una cuenta
2. Crea un nuevo proyecto
3. Una vez creado, ve a **Settings → Database → Connection String**
4. Copia la cadena de conexión PostgreSQL (URI)

### 2. Actualizar variables de entorno

Edita el archivo `.env` en la raíz del proyecto y reemplaza los valores:

```env
# Configuración de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co  # De Settings → API
SUPABASE_KEY=tu-clave-publica  # De Settings → API
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=tu-contraseña-real  # De Settings → Database
SUPABASE_DB_HOST=db.tu-proyecto.supabase.co  # De Settings → Database
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres

# URL de conexión PostgreSQL para SQLAlchemy
DATABASE_URL=postgresql://postgres:tu-contraseña-real@db.tu-proyecto.supabase.co:5432/postgres?sslmode=require
```

### 3. Estructura de carpetas

```
Leet-Code-Clone/
├── Codigo/
│   ├── __init__.py
│   ├── main.py          # Punto de entrada
│   ├── config.py        # Configuración
│   ├── app/
│   │   ├── __init__.py  # create_app()
│   │   └── extensions.py # db = SQLAlchemy()
│   ├── database/
│   │   └── db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── categoria.py
│   │   ├── problema.py
│   │   └── envio.py
│   ├── services/
│   └── menus/
├── requirements.txt
├── .env
└── test_connection.py
```

## 📦 Modelos disponibles

Tu proyecto ya incluye 4 modelos mapeados con ORM SQLAlchemy:

### 1. **Usuario**
- Usuarios del sistema (estudiantes y administradores)
- Campos: id, nombre, email, password_hash, rol, activo, fechas

### 2. **Categoría**
- Categorías de problemas (Arrays, Strings, etc.)
- Campos: id, nombre, descripción, slug, activa

### 3. **Problema**
- Problemas de codificación
- Campos: id, título, descripción, dificultad, categoría, puntos, casos de prueba

### 4. **Envío**
- Envíos de soluciones por usuarios
- Campos: id, usuario_id, problema_id, código, lenguaje, estado, puntos obtenidos

## 💾 Comandos iniciales

### Crear las tablas en la base de datos:

```bash
# Ir a la carpeta Codigo
cd Codigo

# Ejecutar Flask CLI para inicializar BD
flask --app main init-db
```

### Ejecutar tests de conexión:

```bash
# Desde la raíz del proyecto
python test_connection.py
```

### Acceder a la shell interactiva:

```bash
flask --app main shell
```

Dentro de la shell:
```python
from app.models import Usuario, Categoria
db.create_all()  # Crear todas las tablas
```

## 🔗 Hacer una consulta simple

Ejemplo en Python:

```python
from app import create_app
from app.models import Usuario

app = create_app()

with app.app_context():
    # Obtener todos los usuarios
    usuarios = Usuario.query.all()
    
    # Crear un usuario
    nuevo_usuario = Usuario(
        nombre="Juan",
        email="juan@example.com",
        password_hash="hash_aqui",
        rol="user"
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
```

## 🐛 Solución de problemas

### Error: "could not translate host name"
- Verifica que tus credenciales de Supabase sean correctas en `.env`
- Asegúrate de que tu proyecto Supabase está activo

### Error: "authentication failed"
- Verifica la contraseña de la base de datos en `.env`
- Va a Settings → Database en Supabase y copia la contraseña correcta

### Error: "relation does not exist"
- Ejecuta `flask --app main init-db` para crear las tablas

## 📝 Rutas útiles

**Acceder a los datos en la base de datos:**

```python
# Todos los usuarios
usuarios = Usuario.query.all()

# Usuario por ID
usuario = Usuario.query.get(1)

# Filtrar por email
usuario = Usuario.query.filter_by(email="juan@example.com").first()

# Contar registros
total = Usuario.query.count()
```

## ✅ ¡Estás listo!

Con esta configuración ya tienes:
- ✓ Flask configurado
- ✓ SQLAlchemy conectado a Supabase
- ✓ 4 modelos de base de datos
- ✓ CLI commands para manejar la BD
- ✓ Variables de entorno configuradas

Ahora puedes empezar a desarrollar tu aplicación.
