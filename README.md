# Leet Code Clone


El sistema consiste en una plataforma web inspirada en herramientas como LeetCode, orientada a estudiantes, que permite:

●       Resolver problemas de programación

●       Ejecutar código

●       Validar soluciones mediante datos de prueba

●       Gestionar problemas por parte de administradores

El producto está enfocado en mejorar las habilidades de programación de los estudiantes en un entorno educativo.


## Requisitos previos

Antes de correr el proyecto, necesitas tener instalado:

- Python 3.11 o superior
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — **debe estar abierto y corriendo** antes de ejecutar el programa

Opcionalmente, para persistir envíos en una base real necesitas una base de datos PostgreSQL (o Supabase).

---

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/leetcode-clon.git
cd leetcode-clon
```

### 2. Instala las dependencias de Python

```bash
pip install -r requirements.txt
```

### 3. Descarga las imágenes Docker

Este paso solo se hace una vez. Las imágenes permiten ejecutar código en Python, Java y C++:

```bash
docker pull python:3.11-slim
docker pull eclipse-temurin:17-jdk
docker pull gcc:13


### 4. Variables de entorno (opcional)

El proyecto puede usar Supabase / PostgreSQL para autenticación y persistencia. Si quieres conectar con un servicio real, exporta estas variables (o créalas en tu entorno):

- `DATABASE_URL` — cadena de conexión a la base de datos (postgre)
- `SUPABASE_URL` — URL de Supabase (si usas Supabase)
- `SUPABASE_KEY` — clave de servicio de Supabase
- `FLASK_ENV=development` — activa modo desarrollo

En Windows PowerShell:

```powershell
$env:FLASK_ENV = 'development'
$env:DATABASE_URL = 'postgresql://user:pass@localhost:5432/dbname'
```

En Unix/macOS:

```bash
export FLASK_ENV=development
export DATABASE_URL='postgresql://user:pass@localhost:5432/dbname'
```

## Cómo correr el proyecto

Asegúrate de que **Docker Desktop esté abierto**, luego ejecuta:

```bash
python main.py
```

Abre el navegador en http://127.0.0.1:5000/ y navega a la ruta del problema (por ejemplo `/problems/<id>/ui`).

Si ves errores relacionados con Docker:

- `Cannot connect to the Docker daemon`: asegúrate de abrir Docker Desktop y esperar a que esté listo.
- `image not found`: ejecuta los `docker pull` indicados arriba.

Si prefieres usar un entorno virtual en Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

En macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Solución de problemas

**Error: `Cannot connect to the Docker daemon`**
→ Docker Desktop no está abierto. Ábrelo y espera a que el ícono deje de girar.

**Error: `image not found`**
→ No descargaste las imágenes. Corre los comandos `docker pull` del paso 3.

## Notas de desarrollo

- El ejecutor crea un contenedor Docker por cada ejecución y monta un archivo `solution.py` con el código del usuario. Por ello es importante que Docker esté disponible.
- Para pruebas locales rápidas el proyecto usa almacenes mock (`Codigo/models/envio.py`) — si quieres persistir `Envio` en la base real, configura `DATABASE_URL` y actualiza las funciones `guardar_envio` / `actualizar_resultados` para usar SQLAlchemy (hay un modelo `Envio` en `Codigo/models/envio.py`).
- Si tu código Python solo define funciones, el ejecutor intentará invocar automáticamente la última función definida y hará `print` de su retorno; si prefieres controlar la invocación añade un bloque `if __name__ == '__main__'`.

## Setup avanzado y conexión a BD / Supabase

Si quieres usar la aplicación con persistencia real (PostgreSQL / Supabase) sigue estos pasos rápidos:

1) Actualiza las variables de entorno en un archivo `.env` o en tu entorno:

```env
# Ejemplo .env
SUPABASE_DB_PASSWORD=tu-contraseña-aqui
SUPABASE_DB_HOST=db.tu-proyecto.supabase.co
DATABASE_URL=postgresql://postgres:tu-contraseña@db.tu-proyecto.supabase.co:5432/postgres?sslmode=require
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_KEY=eyJhbGciOiJI...
```

2) Instala dependencias y crea tablas (el proyecto incluye comandos para inicializar la BD):

```bash
pip install -r requirements.txt
cd Codigo
python main.py init-db
```

3) Opcional: crea un usuario de prueba desde la REPL de Flask o un script de ejemplo (ver `README_SETUP.md` para ejemplos de uso).

## Estructura de modelos (resumen)

| Modelo | Tabla | Descripción |
|--------|-------|-------------|
| **Usuario** | `usuarios` | Usuarios del sistema |
| **Categoría** | `categorias` | Categorías de problemas |
| **Problema** | `problemas` | Problemas de programación |
| **Envío** | `envios` | Envíos de soluciones |

## Comandos y utilidades adicionales

- Abrir shell interactiva de Flask:

```bash
flask --app Codigo/main shell
```

- Crear tablas:

```bash
flask --app Codigo/main init-db
```

- Eliminar tablas (cuidado):

```bash
flask --app Codigo/main drop-db
```

- Test de conexión (si existe `test_connection.py`):

```bash
python test_connection.py
```

---

Si prefieres mantener `README_SETUP.md` como documento separado con más ejemplos, lo he dejado intacto en el repositorio.

## Comandos útiles

- Ejecutar tests: `pytest -q`
- Formatear código: `black .` (si tienes Black instalado)



cd "C:\Users\juhor\Documents\GitHub\Leet Code Clone\Codigo"
py main.py
http://127.0.0.1:5000/ejecutar