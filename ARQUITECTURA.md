# 🏗️ Arquitectura - Flask + SQLAlchemy + Supabase

## Flujo de Conexión

```
┌─────────────────────────────────────────────────────────────────┐
│                     TU APLICACIÓN FLASK                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  main.py                                                         │
│  ↓                                                                │
│  create_app() ← app/__init__.py (inicializa Flask)             │
│  ↓                                                                │
│  SQLAlchemy ← app/extensions.py (db = SQLAlchemy())           │
│  ↓                                                                │
│  Modelos ORM                                                     │
│  ├─ Usuario                                                      │
│  ├─ Categoría                                                    │
│  ├─ Problema                                                     │
│  └─ Envío                                                        │
│                                                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ PostgreSQL Driver
                     │ (psycopg2-binary)
                     │
         ┌───────────▼────────────┐
         │   DATABASE_URL (.env)  │
         │ postgresql://user:pass │
         │ @host:port/db          │
         └───────────┬────────────┘
                     │
                     │ SSL Connection
                     │ (sslmode=require)
                     │
         ┌───────────▼────────────────────────┐
         │                                     │
         │   🔒 SUPABASE PostgreSQL DATABASE  │
         │                                     │
         │   ┌──────────────────────────────┐ │
         │   │ usuarios (tabla)             │ │
         │   │ id, nombre, email, rol, ...  │ │
         │   └──────────────────────────────┘ │
         │   ┌──────────────────────────────┐ │
         │   │ categorias (tabla)           │ │
         │   │ id, nombre, slug, ...        │ │
         │   └──────────────────────────────┘ │
         │   ┌──────────────────────────────┐ │
         │   │ problemas (tabla)            │ │
         │   │ id, titulo, dificultad, ...  │ │
         │   └──────────────────────────────┘ │
         │   ┌──────────────────────────────┐ │
         │   │ envios (tabla)               │ │
         │   │ id, usuario_id, codigo, ...  │ │
         │   └──────────────────────────────┘ │
         │                                     │
         └─────────────────────────────────────┘
```

## Componentes principales

### 1. **Configuración inicial (.env)**
```
Archivo: .env
Contiene: DATABASE_URL y credenciales de Supabase
Formato: postgresql://usuario:contraseña@host:puerto/database?sslmode=require
```

### 2. **Aplicación Flask (Codigo/app/)**
```
app/__init__.py      → Crea la aplicación Flask
app/extensions.py    → Inicializa SQLAlchemy
```

### 3. **Modelos ORM (Codigo/models/)**
```
Usuario      ← Usuarios del sistema
Categoría    ← Categorías de problemas
Problema     ← Problemas de programación
Envío        ← Envíos de soluciones
```

### 4. **Base de datos (Supabase PostgreSQL)**
```
5 tablas: usuarios, categorias, problemas, envios
Hospedada en: db.xxxx.supabase.co
```

## Relaciones entre modelos

```
┌─────────────────────────────────────────────────────────┐
│                      USUARIO                           │
│  id (PK) | nombre | email | password_hash | rol       │
└─────────────────┬──────────────────────────────────────┘
                  │
                  │ 1:N
                  │
        ┌─────────▼────────────────────────────────────┐
        │            ENVÍO                             │
        │ id | usuario_id (FK) | problema_id (FK) |   │
        │ codigo | lenguaje | estado | puntos          │
        └─────────┬──────────────────┬────────────────┘
                  │                  │
                  │1:N               │1:N
                  │                  │
    ┌─────────────▼──────────┐     │
    │      CATEGORÍA         │     │
    │ id | nombre | slug     │     │
    └─────────────┬──────────┘     │
                  │                │
                  │1:N             │
                  │                │
            ┌─────▼────────────────────────────────┐
            │          PROBLEMA                    │
            │ id | titulo | dificultad |           │
            │ categoria_id (FK) | puntos           │
            └────────────────────────────────────┘
```

## Ciclo de vida de una solicitud

```
1. Usuario hace una acción
   ↓
2. Flask recibe la solicitud
   ↓
3. Consulta/modifica un modelo ORM
   ↓
4. SQLAlchemy traduce a SQL
   ↓
5. psycopg2 envía SQL a Supabase
   ↓
6. Supabase (PostgreSQL) ejecuta
   ↓
7. Resultado regresa a la aplicación
   ↓
8. Respuesta al usuario
```

## Archivos de configuración

### .env
```env
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres?sslmode=require
```

### Codigo/config.py
```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
```

### Codigo/app/__init__.py
```python
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)
    return app
```

## Flujo de desarrollo

```
┌──────────────────────┐
│  Editar modelos en   │
│  Codigo/models/*.py  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│  Ejecutar init-db para que   │
│  SQLAlchemy cree las tablas  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Las tablas se crean en      │
│  Supabase automáticamente    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Usar los modelos en tu      │
│  aplicación Flask            │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Las consultas se sincronizan│
│  automáticamente con la BD   │
└──────────────────────────────┘
```

## Cómo las consultas se mapean

### Código Python (ORM)
```python
usuario = Usuario.query.filter_by(email="juan@example.com").first()
```

### SQL generado automáticamente
```sql
SELECT * FROM usuarios WHERE email = 'juan@example.com' LIMIT 1;
```

### Resultado
```python
<Usuario juan@example.com>
```

## Seguridad

1. **Conexión SSL**: `sslmode=require` en DATABASE_URL
2. **Variables de entorno**: Las credenciales en `.env` (nunca en el código)
3. **Contraseña hash**: Las contraseñas de usuarios no se guardan planas
4. **Validaciones ORM**: SQLAlchemy previene SQL injection

## Escalabilidad

- **Base de datos**: Supabase maneja automáticamente escalamiento
- **Conexiones**: SQLAlchemy usa un pool de conexiones
- **Queries**: Puedes agregar índices directamente en Supabase para optimizar

---

¡La arquitectura está lista para producción! 🚀
