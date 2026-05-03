# 🚀 Leet Code Clone - Flask + SQLAlchemy + Supabase

## Instalación rápida (3 pasos)

### 1️⃣ Actualizar `.env` con tus credenciales de Supabase

```env
# Editar este archivo con tus datos reales
SUPABASE_DB_PASSWORD=tu-contraseña-aqui
SUPABASE_DB_HOST=db.tu-proyecto.supabase.co
DATABASE_URL=postgresql://postgres:tu-contraseña@db.tu-proyecto.supabase.co:5432/postgres?sslmode=require
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Crear tablas en la BD

```bash
cd Codigo
python main.py init-db
```

✅ **¡Listo!** Ya tienes conexión a Supabase con ORM.

---

## Uso

### Crear un usuario

```python
from app import create_app
from app.models import Usuario
from app.extensions import db

app = create_app()

with app.app_context():
    usuario = Usuario(
        nombre="Juan",
        email="juan@example.com",
        password_hash="hash123",
        rol="user"
    )
    db.session.add(usuario)
    db.session.commit()
```

### Consultar datos

```python
with app.app_context():
    # Todos
    usuarios = Usuario.query.all()
    
    # Por email
    usuario = Usuario.query.filter_by(email="juan@example.com").first()
    
    # Por ID
    usuario = Usuario.query.get(1)
```

### Ejecutar la app

```bash
cd Codigo
python main.py
```

---

## Comandos útiles

```bash
# Abrir shell interactiva
flask --app Codigo/main shell

# Crear tablas
flask --app Codigo/main init-db

# Eliminar tablas (cuidado!)
flask --app Codigo/main drop-db

# Test de conexión
python test_connection.py
```

---

## Estructura de modelos

| Modelo | Tabla | Descripción |
|--------|-------|-------------|
| **Usuario** | `usuarios` | Usuarios del sistema |
| **Categoría** | `categorias` | Categorías de problemas |
| **Problema** | `problemas` | Problemas de programación |
| **Envío** | `envios` | Envíos de soluciones |

---

## 📚 Documentación

- **CHECKLIST.md** - Verificación paso a paso
- **CONFIGURACION_SUPABASE.md** - Guía completa
- **ARQUITECTURA.md** - Diagrama de arquitectura
- **RESUMEN_CONFIGURACION.md** - Resumen detallado
- **ejemplos_uso.py** - Ejemplos de código

---

## 🔗 Relacionado

- [Supabase](https://supabase.com)
- [Flask](https://flask.palletsprojects.com)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [PostgreSQL](https://www.postgresql.org)

---

**¡Hecho! 🎉 Tu aplicación está lista para usar con Supabase.**
