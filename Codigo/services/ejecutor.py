#Recibe: el codigo y el lenguaje
#Envia: Resultado de la ejecucion del codigo

import subprocess
import tempfile
import os
import re

#Configuración por lenguaje:
LENGUAJES = {
    "python": {
        "imagen": "python:3.11-slim",
        "archivo": "solution.py",
        "comando": ["python", "solution.py"],
    },
    "java": {
        "imagen": "eclipse-temurin:17-jdk",
        "archivo": "Solution.java",
        "comando": ["sh", "-c", "javac Solution.java && java Solution"],
    },
    "cpp": {
        "imagen": "gcc:13",
        "archivo": "solution.cpp",
        "comando": ["sh", "-c", "g++ solution.cpp -o solution && ./solution"],
    },
}


# Patrones que identifican errores de compilación por lenguaje
PATRONES_COMPILACION = {
    "python": [],
    "java": [
        "error:",
        "cannot find symbol",
        "reached end of file",
        "illegal start of expression",
    ],
    "cpp": [
        "error:",
        "expected",
        "undeclared",
        "no match for",
    ],
}

def es_error_compilacion(stderr: str, lenguaje: str) -> bool:
    
    #identifica si es un error de compilacion

    patrones = PATRONES_COMPILACION.get(lenguaje, [])
    stderr_lower = stderr.lower()
    return any(patron in stderr_lower for patron in patrones)

def limpiar_mensaje_error(stderr: str) -> str:
    lineas = stderr.strip().splitlines()
    limpias = []
    
    for linea in lineas:

        linea = linea.replace("/code/", "")

        if re.match(r"^\s+at\s+\w+", linea):
            continue

        if re.match(r"^\d+ error(s)?$", linea.strip()):
            continue

        if linea.strip():
            limpias.append(linea)

    return "\n".join(limpias)


def ejecutar_codigo(codigo: str, lenguaje: str) -> dict:

    #Recibe el código del usuario y el lenguaje, devuelve un dict con: output, error, y si se acabo el tiempo limite.

    config = LENGUAJES.get(lenguaje)
    if not config:
        return {"error": f"Lenguaje '{lenguaje}' no soportado"}



    with tempfile.TemporaryDirectory() as carpeta_tmp: #crea un directorio temporal

        ruta_archivo = os.path.join(carpeta_tmp, config["archivo"])
        with open(ruta_archivo, "w") as f:
            f.write(codigo)

        comando_docker = [
            "docker", "run",
            "--rm",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            "-v", f"{carpeta_tmp}:/code",
            "-w", "/code",
            config["imagen"],
        ] + config["comando"]

        try:
            resultado = subprocess.run(
                comando_docker,
                capture_output=True,
                text=True,
                timeout=3
            )

            #si hubo errores se clasifica qué tipo de error es
            if resultado.stderr:
                mensaje_limpio = limpiar_mensaje_error(resultado.stderr)

                if es_error_compilacion(resultado.stderr, lenguaje):
                    return {
                        "output": "",
                        "error": mensaje_limpio,
                        "tipo_error": "compilacion",
                        "supero_tiempo_limite": False
                    }
                else:
                    return {
                        "output": resultado.stdout,
                        "error": mensaje_limpio,
                        "tipo_error": "ejecucion",
                        "supero_tiempo_limite": False
                    }

            #sin errores
            return {
                "output": resultado.stdout,
                "error": "",
                "tipo_error": None,
                "supero_tiempo_limite": False
            }

        #se exedio el limite del tiempo
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "error": "Tiempo límite excedido (3 segundos)",
                "supero_tiempo_limite": True
            }
        
        #error al crear el contenedor
        except FileNotFoundError:
            #Docker no está instalado o no está en el PATH
            return {
                "output": "",
                "error": "El sistema de ejecución no está disponible. Contacta al administrador.",
                "tipo_error": "sistema",
                "supero_tiempo_limite": False
            }

        except Exception:
            #Cualquier otro fallo relacionado con el contenedor
            return {
                "output": "",
                "error": "Ocurrió un error al preparar el entorno de ejecución. Intenta de nuevo.",
                "tipo_error": "sistema",
                "supero_tiempo_limite": False
            }
        