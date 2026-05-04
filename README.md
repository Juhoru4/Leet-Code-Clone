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


## Cómo correr el proyecto

Asegúrate de que **Docker Desktop esté abierto**, luego ejecuta:

```bash
python main.py
```

---

## Solución de problemas

**Error: `Cannot connect to the Docker daemon`**
→ Docker Desktop no está abierto. Ábrelo y espera a que el ícono deje de girar.

**Error: `image not found`**
→ No descargaste las imágenes. Corre los comandos `docker pull` del paso 3.


cd "C:\Users\juhor\Documents\GitHub\Leet Code Clone\Codigo"
py main.py
http://127.0.0.1:5000/ejecutar